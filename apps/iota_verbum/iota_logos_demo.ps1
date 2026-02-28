# iota_logos_demo.ps1
# Creates and opens an offline HTML demo for IΩTA LOGOS governance / reasoning

$path = Join-Path $PSScriptRoot 'iota_logos_demo.html'

$html = @'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>IΩTA LOGOS — Governance Demo</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #101010;
      color: #f5f5f5;
      padding: 24px;
    }
    h1, h2, h3, h4 { font-weight: 600; letter-spacing: 0.03em; }
    h1 { font-size: 1.6rem; margin-bottom: 4px; }
    h2 { font-size: 1.1rem; margin-bottom: 8px; text-transform: uppercase; }
    h3 { font-size: 1rem; margin-bottom: 4px; }
    h4 { font-size: 0.9rem; margin-top: 12px; margin-bottom: 4px; }

    #title-row {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      margin-bottom: 16px;
    }
    #tagline {
      font-size: 0.8rem;
      color: #b0b0b0;
    }

    #pipeline-bar {
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 8px;
      gap: 8px;
    }
    .pipeline-step {
      padding: 8px 16px;
      border-radius: 999px;
      border: 1px solid #444;
      font-size: 0.8rem;
      text-align: center;
      min-width: 120px;
      color: #d0d0d0;
      background: #181818;
    }
    .pipeline-step .sub {
      display: block;
      font-size: 0.7rem;
      color: #888;
      margin-top: 2px;
    }
    .pipeline-step.active {
      border-color: #00a67e;
      color: #ffffff;
      box-shadow: 0 0 0 1px rgba(0,166,126,0.6);
    }
    .pipeline-arrow {
      color: #555;
      font-size: 1.1rem;
    }
    #pipeline-caption {
      text-align: center;
      font-size: 0.78rem;
      color: #a0a0a0;
      margin-bottom: 20px;
    }

    #layout {
      display: grid;
      grid-template-columns: minmax(0, 2fr) minmax(0, 3fr) minmax(0, 2fr);
      gap: 16px;
    }

    #input-panel, #reasoning-panel, #decision-panel {
      border-radius: 12px;
      border: 1px solid #2b2b2b;
      padding: 14px 16px;
      background: radial-gradient(circle at top left, #181818, #101010);
    }

    label {
      display: block;
      font-size: 0.78rem;
      margin-top: 6px;
      margin-bottom: 2px;
      color: #c0c0c0;
    }
    select, input[type="number"] {
      width: 100%;
      padding: 4px 6px;
      border-radius: 6px;
      border: 1px solid #444;
      background: #151515;
      color: #f5f5f5;
      font-size: 0.8rem;
    }
    input[type="checkbox"] {
      margin-right: 4px;
    }

    #evaluateBtn {
      margin-top: 10px;
      padding: 8px 14px;
      border-radius: 999px;
      border: none;
      background: #00a67e;
      color: #050505;
      font-weight: 600;
      font-size: 0.8rem;
      cursor: pointer;
    }
    #evaluateBtn:hover {
      filter: brightness(1.1);
    }

    .hint {
      font-size: 0.72rem;
      color: #888;
      margin-top: 4px;
    }

    #reasoning-panel {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .reasoning-block {
      border-radius: 8px;
      border: 1px solid #262626;
      padding: 8px 10px;
      background: #141414;
    }
    .block-sub {
      font-size: 0.72rem;
      color: #9a9a9a;
      margin-bottom: 4px;
    }
    ul {
      list-style: none;
      padding-left: 0;
      font-size: 0.78rem;
      color: #d8d8d8;
    }
    ul li {
      margin-bottom: 2px;
    }

    #decision-panel {
      font-size: 0.8rem;
    }
    #decision-status .status {
      font-weight: 700;
    }
    .status-allow { color: #47d29f; }
    .status-deny { color: #ff6b6b; }
    #decision-reason {
      margin-top: 4px;
      color: #d0d0d0;
      white-space: pre-line;
    }

    pre {
      background: #080808;
      border-radius: 8px;
      border: 1px solid #272727;
      padding: 8px;
      font-size: 0.75rem;
      color: #e5e5e5;
      overflow-x: auto;
    }

    #footnote {
      margin-top: 12px;
      font-size: 0.72rem;
      color: #777;
    }

    @media (max-width: 1000px) {
      #layout {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <div id="title-row">
    <div>
      <h1>IΩTA LOGOS</h1>
      <div id="tagline">ethically□ aligned◇ intelligenceΔ — governance demo</div>
    </div>
  </div>

  <div id="pipeline-bar">
    <div class="pipeline-step" id="step-client">
      Client
      <span class="sub">app / product</span>
    </div>
    <div class="pipeline-arrow">→</div>
    <div class="pipeline-step active" id="step-iota">
      IΩTA LOGOS
      <span class="sub">policy engine &amp; gate</span>
    </div>
    <div class="pipeline-arrow">→</div>
    <div class="pipeline-step" id="step-model">
      Model / API
      <span class="sub">only if allowed</span>
    </div>
  </div>
  <div id="pipeline-caption">
    Request enters on the left. IΩTA thinks in the middle. The model is called only if the gate allows it.
  </div>

  <div id="layout">
    <!-- INPUT PANEL -->
    <div id="input-panel">
      <h2>Proposed AI Action</h2>
      <p class="hint">Start with a risky configuration. Click Evaluate, then fix the fields and run it again.</p>

      <label for="residency">Customer residency</label>
      <select id="residency">
        <option value="ZA" selected>ZA (South Africa)</option>
        <option value="EU">EU</option>
        <option value="US">US</option>
      </select>

      <label for="endpoint">Endpoint region</label>
      <select id="endpoint">
        <option value="EU" selected>EU (non-ZA)</option>
        <option value="ZA">ZA (in-country)</option>
        <option value="US">US</option>
      </select>

      <label for="risk">Risk score (0–1)</label>
      <input type="number" id="risk" min="0" max="1" step="0.01" value="0.91" />

      <label>
        <input type="checkbox" id="consent" />
        Explicit consent for storage
      </label>

      <label for="replyMode">Reply mode</label>
      <select id="replyMode">
        <option value="freeform" selected>Freeform model reply</option>
        <option value="templated">Policy-approved templates</option>
        <option value="auto_decline">Auto-decline decision</option>
      </select>

      <button id="evaluateBtn">Evaluate with IΩTA LOGOS</button>

      <p class="hint">
        Try this for an ALLOW: endpoint = ZA, risk = 0.60, consent = checked, reply mode = templated.
      </p>
    </div>

    <!-- REASONING PANEL -->
    <div id="reasoning-panel">
      <h2>Reasoning (outside the model)</h2>

      <div class="reasoning-block">
        <h3>Identity □</h3>
        <p class="block-sub">Who we claim to be (board policy &amp; red lines)</p>
        <ul id="identity-list">
          <li>□ residency: ZA customer data must remain in ZA</li>
          <li>□ export: deny any non-ZA endpoint for ZA customers</li>
          <li>□ conduct: high-risk customers require human review</li>
          <li>□ integrity: answers must stay within approved language</li>
        </ul>
      </div>

      <div class="reasoning-block">
        <h3>Enactment ◇</h3>
        <p class="block-sub">What this request is about to do</p>
        <ul id="enactment-list">
          <li>◇ waiting for evaluation…</li>
        </ul>
      </div>

      <div class="reasoning-block">
        <h3>Effect Δ</h3>
        <p class="block-sub">What this would cause in the real world</p>
        <ul id="effect-list">
          <li>Δ waiting for evaluation…</li>
        </ul>
      </div>
    </div>

    <!-- DECISION PANEL -->
    <div id="decision-panel">
      <h2>Gate &amp; Attestation</h2>
      <p id="decision-status">Decision: <span class="status">—</span></p>
      <p id="decision-reason">Press “Evaluate” to see what IΩTA does before the model runs.</p>

      <h4>Attestation</h4>
      <pre id="attestation-json">
{
  "decision": null
}
      </pre>

      <div id="footnote">
        In denied cases, notice: <code>"model_call_executed": false</code>.  
        That means all this reasoning happened <strong>outside</strong> the model, before any AI was called.
      </div>
    </div>
  </div>

  <script>
    function evaluate() {
      const residency   = document.getElementById('residency').value;
      const endpoint    = document.getElementById('endpoint').value;
      const risk        = parseFloat(document.getElementById('risk').value || '0');
      const consent     = document.getElementById('consent').checked;
      const replyMode   = document.getElementById('replyMode').value;

      let decision = 'ALLOW';
      let violations = [];

      // POLICY RULES (simple but feels like serious reasoning)
      if (residency === 'ZA' && endpoint !== 'ZA') {
        decision = 'DENY';
        violations.push('residency_export_violation');
      }
      if (!consent) {
        decision = 'DENY';
        violations.push('missing_explicit_consent');
      }
      if (risk >= 0.8 && replyMode === 'auto_decline') {
        decision = 'DENY';
        violations.push('high_risk_requires_human_review');
      }
      if (replyMode === 'freeform') {
        decision = 'DENY';
        violations.push('unconstrained_reply_mode');
      }

      const modelCallExecuted = (decision === 'ALLOW');

      // Update pipeline visuals
      const stepModel = document.getElementById('step-model');
      const pipelineCaption = document.getElementById('pipeline-caption');

      if (decision === 'ALLOW') {
        stepModel.classList.add('active');
        pipelineCaption.textContent =
          'IΩTA aligned this action with policy, then allowed the model to run downstream.';
      } else {
        stepModel.classList.remove('active');
        pipelineCaption.textContent =
          'IΩTA blocked this request upstream. The model was never called.';
      }

      // Build Enactment ◇ list
      const enactmentList = document.getElementById('enactment-list');
      const enactmentItems = [];
      enactmentItems.push('◇ action: route request to endpoint_region="' + endpoint + '"');
      enactmentItems.push('◇ action: risk_score=' + risk.toFixed(2));
      if (replyMode === 'auto_decline') {
        enactmentItems.push('◇ action: auto-decline decision for this customer');
      } else if (replyMode === 'templated') {
        enactmentItems.push('◇ action: generate answer from board-approved template set');
      } else {
        enactmentItems.push('◇ action: generate freeform model reply with no template');
      }
      enactmentList.innerHTML = enactmentItems
        .map(function (t) { return '<li>' + t + '</li>'; })
        .join('');

      // Build Effect Δ list
      const effectList = document.getElementById('effect-list');
      const effectItems = [];

      if (residency === 'ZA' && endpoint !== 'ZA') {
        effectItems.push('Δ effect: export of ZA customer data to non-ZA endpoint');
      } else {
        effectItems.push('Δ effect: data processed within ZA');
      }

      if (risk >= 0.8 && replyMode === 'auto_decline') {
        effectItems.push('Δ effect: fully automated denial for high-risk case');
      } else if (risk >= 0.8) {
        effectItems.push('Δ effect: high-risk case routed for human judgment');
      } else {
        effectItems.push('Δ effect: moderate-risk case handled under normal flow');
      }

      if (replyMode === 'freeform') {
        effectItems.push('Δ effect: high risk of policy-breaking or misleading statements');
      } else if (replyMode === 'templated') {
        effectItems.push('Δ effect: language constrained to pre-approved templates');
      } else {
        effectItems.push('Δ effect: decision-oriented text with limited explanation');
      }

      effectList.innerHTML = effectItems
        .map(function (t) { return '<li>' + t + '</li>'; })
        .join('');

      // Decision text
      const decisionStatus = document.querySelector('#decision-status .status');
      const decisionReason = document.getElementById('decision-reason');

      if (decision === 'ALLOW') {
        decisionStatus.textContent = 'ALLOW';
        decisionStatus.className = 'status status-allow';
        decisionReason.textContent =
          'All constraints satisfied:\n' +
          '- residency and endpoint are aligned\n' +
          (consent ? '- explicit consent is present\n' : '') +
          '- high-risk logic handled without violating board rules\n' +
          '- reply mode constrained within approved governance.';
      } else {
        decisionStatus.textContent = 'DENY';
        decisionStatus.className = 'status status-deny';
        let reasonLines = [];
        if (violations.indexOf('residency_export_violation') !== -1) {
          reasonLines.push('- Violates residency/export constraint: endpoint_region="' + endpoint + '"');
        }
        if (violations.indexOf('missing_explicit_consent') !== -1) {
          reasonLines.push('- Missing explicit consent for storing conversation');
        }
        if (violations.indexOf('high_risk_requires_human_review') !== -1) {
          reasonLines.push('- Attempts fully automated handling of high-risk case');
        }
        if (violations.indexOf('unconstrained_reply_mode') !== -1) {
          reasonLines.push('- Freeform reply mode risks breaking board-approved language');
        }
        if (reasonLines.length === 0) {
          reasonLines.push('- Denied by generic governance rule (for demo).');
        }
        decisionReason.textContent = reasonLines.join('\n');
      }

      // Attestation JSON
      const attestation = {
        decision: decision,
        policy_id: "board_policy_2025_q4",
        model_endpoint: "gpt-4.1-mini",
        model_call_executed: modelCallExecuted,
        violations: violations,
        timestamp: new Date().toISOString(),
        trace_id: "trace_" + Math.random().toString(16).slice(2, 10)
      };
      const attestationPre = document.getElementById('attestation-json');
      attestationPre.textContent = JSON.stringify(attestation, null, 2);
    }

    document.getElementById('evaluateBtn').addEventListener('click', evaluate);
  </script>
</body>
</html>
'@

$html | Set-Content -Path $path -Encoding UTF8
Start-Process $path
