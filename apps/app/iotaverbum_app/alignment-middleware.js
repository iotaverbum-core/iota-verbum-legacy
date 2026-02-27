/*
 * AlignmentMiddleware orchestrates chat interactions with the OpenAI API,
 * monitors drift using ConversationTrajectory, applies interventions
 * when risk thresholds are reached and triggers alerts. It also
 * supports simple function calling to run batch attestations or
 * adjust basin strengths on the fly.
 */

require('dotenv').config();
const OpenAI = require('openai');
const { ConversationTrajectory, setBasins, getBasins } = require('./alignment-core');
const AlertSystem = require('./alert-system');
const ABTestingFramework = require('./ab-testing');
const BatchAttestation = require('./batch-attestation');

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

class AlignmentMiddleware {
  constructor(config = {}) {
    this.activeConversations = new Map();
    this.interventionLog = [];
    this.alertSystem = new AlertSystem(config.alertConfig || {});
    this.abTesting = new ABTestingFramework();
    this.config = {
      defaultBasins: config.defaultBasins || getBasins(),
      defaultInterventionsEnabled: config.defaultInterventionsEnabled ?? true
    };
  }

  getOrCreateTrajectory(conversationId, basinConfig) {
    let trajectory = this.activeConversations.get(conversationId);
    if (!trajectory) {
      trajectory = new ConversationTrajectory(conversationId, basinConfig);
      this.activeConversations.set(conversationId, trajectory);
    }
    return trajectory;
  }

  getFleetStats() {
    const convs = Array.from(this.activeConversations.values());
    const withDrift = convs.filter(c => c.driftMetrics);
    const total = convs.length;
    const high = withDrift.filter(c => c.driftMetrics.riskLevel === 'high').length;
    const med = withDrift.filter(c => c.driftMetrics.riskLevel === 'medium').length;
    const basinDist = {};
    withDrift.forEach(c => {
      const b = c.driftMetrics.dominantBasin;
      basinDist[b] = (basinDist[b] || 0) + 1;
    });
    return { total, highRisk: high, mediumRisk: med, basinDist };
  }

  async handleRequest(userId, conversationId, messages, options = {}) {
    // Determine assignment via experiment if provided
    let interventionsEnabled = this.config.defaultInterventionsEnabled;
    let basinConfig = this.config.defaultBasins;
    if (options.experimentId) {
      const assign = this.abTesting.assignUserToGroup(options.experimentId, userId);
      if (assign) {
        basinConfig = assign.config.basinConfig || basinConfig;
        interventionsEnabled = assign.config.interventionsEnabled;
      }
    }
    const traj = this.getOrCreateTrajectory(conversationId, basinConfig);
    const drift = traj.driftMetrics;
    let systemPrompt = this.getBaseSystemPrompt();
    if (interventionsEnabled && drift && drift.riskScore >= 0.45) {
      systemPrompt = this.modifySystemPrompt(systemPrompt, drift);
      this.interventionLog.unshift({
        id: `int-${Date.now()}-${Math.random().toString(36).slice(2)}`,
        conversationId,
        userId,
        timestamp: Date.now(),
        driftScore: drift.riskScore,
        driftLevel: drift.riskLevel,
        interventionType: 'system_prompt_modification'
      });
    }
    // Prepare OpenAI request with function definitions
    const openaiMessages = [ { role: 'system', content: systemPrompt }, ...messages ];
    const functions = [
      {
        name: 'run_attestation',
        description: 'Run a batch attestation over a comma‑separated list of files',
        parameters: {
          type: 'object',
          properties: {
            files: { type: 'string', description: 'Comma‑separated list of file paths' }
          },
          required: ['files']
        }
      },
      {
        name: 'update_basin_strength',
        description: 'Modify the strength of a named basin',
        parameters: {
          type: 'object',
          properties: {
            basin: { type: 'string' },
            value: { type: 'number' }
          },
          required: ['basin', 'value']
        }
      }
    ];
    // Send request to OpenAI with function calling and streaming disabled (we gather full response)
    const response = await openai.chat.completions.create({
      model: process.env.OPENAI_MODEL || 'gpt-5.1',
      messages: openaiMessages,
      functions,
      max_tokens: 2048,
      temperature: 0.7
    });
    const choice = response.choices[0];
    if (choice.finish_reason === 'function_call') {
      const fc = choice.message.function_call;
      const args = JSON.parse(fc.arguments || '{}');
      if (fc.name === 'run_attestation') {
        const files = args.files.split(',').map(f => f.trim());
        const results = await BatchAttestation.run(files);
        return { response: { content: JSON.stringify(results, null, 2) }, metadata: { tool: 'run_attestation' } };
      }
      if (fc.name === 'update_basin_strength') {
        const updated = getBasins().map(b => b.name === args.basin ? { ...b, strength: args.value } : b);
        setBasins(updated);
        return { response: { content: `Updated ${args.basin} strength to ${args.value}` }, metadata: { tool: 'update_basin_strength' } };
      }
    }
    const text = choice.message.content;
    traj.addResponse(text);
    const newDrift = traj.driftMetrics;
    if (newDrift && newDrift.riskScore >= 0.7) {
      await this.alertSystem.checkAndAlert(conversationId, userId, newDrift);
    }
    return {
      response: { content: text },
      metadata: {
        driftScore: newDrift ? newDrift.riskScore : 0,
        driftLevel: newDrift ? newDrift.riskLevel : 'none',
        dominantBasin: newDrift ? newDrift.dominantBasin : null,
        interventionApplied: Boolean(interventionsEnabled && drift && drift.riskScore >= 0.45)
      }
    };
  }

  modifySystemPrompt(base, drift) {
    const mods = [];
    if (drift.loopiness > 0.7) {
      if (drift.dominantBasin === 'Harmlessness') {
        mods.push('IMPORTANT: Recent responses have been overly cautious. Balance safety with practical guidance.');
      } else if (drift.dominantBasin === 'Helpfulness') {
        mods.push('IMPORTANT: Responses are too detailed. Add safety caveats and prompt the user to verify information.');
      }
    }
    if (drift.lamentFraction > 0.6) {
      mods.push('NOTE: You are balancing competing values. Make trade‑offs explicit.');
    }
    if (drift.dominantBasin === 'Helpfulness' && drift.stability > 0.7) {
      mods.push('REMINDER: Emphasise user agency. Offer input, not commands.');
    }
    return base + '\n\n' + mods.join('\n');
  }

  getBaseSystemPrompt() {
    return `You are ChatGPT, running model GPT‑5.1.\n\nYour responses must balance:\n- Helpfulness (clarity, completeness, actionable guidance)\n- Harmlessness (safety, respect, appropriate boundaries)\n- Honesty (accuracy, transparency about uncertainty)\n- Agency Respect (support user autonomy, avoid dependency)\n\nMaintain this balance across the entire conversation.`;
  }
}

module.exports = AlignmentMiddleware;