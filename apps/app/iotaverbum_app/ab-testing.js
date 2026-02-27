/*
 * Simple A/B testing framework for evaluating interventions. Experiments
 * are defined with control and treatment groups, basin configurations and
 * intervention toggles. Metrics can be recorded on a per‑conversation
 * basis and results computed via Welch’s t‑test approximation.
 */

class ABTestingFramework {
  constructor() {
    this.experiments = new Map();
  }

  createExperiment(config) {
    const experiment = {
      id: config.id,
      name: config.name,
      hypothesis: config.hypothesis,
      control: {
        name: 'control',
        basinConfig: config.controlBasinConfig,
        interventionsEnabled: false,
        users: []
      },
      treatment: {
        name: 'treatment',
        basinConfig: config.treatmentBasinConfig,
        interventionsEnabled: true,
        users: []
      },
      metrics: {
        avgDriftScore: { control: [], treatment: [] },
        userSatisfaction: { control: [], treatment: [] },
        conversationLength: { control: [], treatment: [] }
      },
      startDate: null,
      endDate: null,
      status: 'draft',
      sampleSize: config.sampleSize || 1000,
      splitRatio: config.splitRatio || 0.5
    };
    this.experiments.set(experiment.id, experiment);
    return experiment;
  }

  hashCode(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = ((hash << 5) - hash) + str.charCodeAt(i);
      hash |= 0;
    }
    return Math.abs(hash);
  }

  assignUserToGroup(experimentId, userId) {
    const exp = this.experiments.get(experimentId);
    if (!exp || exp.status !== 'running') return null;
    const hash = this.hashCode(userId);
    const groupName = (hash % 100) < (exp.splitRatio * 100) ? 'control' : 'treatment';
    const group = exp[groupName];
    if (!group.users.includes(userId)) group.users.push(userId);
    return { group: groupName, config: group };
  }

  recordMetric(experimentId, userId, metricName, value) {
    const exp = this.experiments.get(experimentId);
    if (!exp) return;
    const groupName = this.getUserGroup(experimentId, userId);
    if (!groupName) return;
    exp.metrics[metricName][groupName].push(value);
  }

  getUserGroup(experimentId, userId) {
    const exp = this.experiments.get(experimentId);
    if (!exp) return null;
    if (exp.control.users.includes(userId)) return 'control';
    if (exp.treatment.users.includes(userId)) return 'treatment';
    return null;
  }

  mean(arr) {
    return arr.reduce((a, b) => a + b, 0) / (arr.length || 1);
  }

  std(arr) {
    const avg = this.mean(arr);
    const sqDiffs = arr.map(v => Math.pow(v - avg, 2));
    return Math.sqrt(this.mean(sqDiffs));
  }

  normalCDF(x) {
    const sign = x < 0 ? -1 : 1;
    const absX = Math.abs(x) / Math.sqrt(2);
    const t = 1 / (1 + 0.3275911 * absX);
    const a1 = 0.254829592;
    const a2 = -0.284496736;
    const a3 = 1.421413741;
    const a4 = -1.453152027;
    const a5 = 1.061405429;
    const erf = 1 - (((((a5 * t + a4) * t + a3) * t + a2) * t + a1) * t) * Math.exp(-absX * absX);
    return 0.5 * (1 + sign * erf);
  }

  tTest(arr1, arr2) {
    const mean1 = this.mean(arr1);
    const mean2 = this.mean(arr2);
    const std1 = this.std(arr1);
    const std2 = this.std(arr2);
    const n1 = arr1.length || 1;
    const n2 = arr2.length || 1;
    const t = (mean1 - mean2) / Math.sqrt((std1 * std1 / n1) + (std2 * std2 / n2));
    return 2 * (1 - this.normalCDF(Math.abs(t)));
  }

  getResults(experimentId) {
    const exp = this.experiments.get(experimentId);
    if (!exp) return null;
    const results = {};
    Object.entries(exp.metrics).forEach(([metric, groups]) => {
      const controlVals = groups.control;
      const treatmentVals = groups.treatment;
      const controlMean = this.mean(controlVals);
      const treatmentMean = this.mean(treatmentVals);
      const controlStd = this.std(controlVals);
      const treatmentStd = this.std(treatmentVals);
      const pValue = this.tTest(controlVals, treatmentVals);
      const effect = treatmentMean - controlMean;
      const percentChange = controlMean ? (effect / controlMean) * 100 : 0;
      results[metric] = {
        control: { mean: controlMean, std: controlStd, n: controlVals.length },
        treatment: { mean: treatmentMean, std: treatmentStd, n: treatmentVals.length },
        pValue,
        significant: pValue < 0.05,
        effect,
        percentChange
      };
    });
    return {
      experimentId: exp.id,
      name: exp.name,
      hypothesis: exp.hypothesis,
      sampleSizes: { control: exp.control.users.length, treatment: exp.treatment.users.length },
      results
    };
  }
}

module.exports = ABTestingFramework;