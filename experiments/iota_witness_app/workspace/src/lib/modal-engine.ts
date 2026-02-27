/**
 * Iota Verbum (IV) - Modal Logic Engine
 * 
 * Core modal operators for computational theology:
 * - □ (Necessity) - God's Decree / Divine Sovereignty
 * - ◇ (Possibility) - Human Agency / Contingency  
 * - W (Witness) - Connection between divine and human
 * - σ (Separation) - Distinguishing essence from accident
 * - π (Staying) - God's faithfulness / Human perseverance
 */

import { createHash } from 'crypto';

// Modal Operator Types
export type ModalOperatorType = 
  | 'NECESSITY' 
  | 'POSSIBILITY' 
  | 'WITNESS' 
  | 'SEPARATION' 
  | 'STAYING';

// Modal Operator Symbols
export const MODAL_SYMBOLS: Record<ModalOperatorType, string> = {
  NECESSITY: '□',
  POSSIBILITY: '◇',
  WITNESS: 'W',
  SEPARATION: 'σ',
  STAYING: 'π',
};

// Theological interpretations
export const MODAL_INTERPRETATIONS: Record<ModalOperatorType, {
  divine: string;
  human: string;
  description: string;
}> = {
  NECESSITY: {
    divine: "God's Decree",
    human: "Divine Sovereignty",
    description: "That which must be, by divine ordinance. Represents God's eternal purpose that cannot be thwarted."
  },
  POSSIBILITY: {
    divine: "Divine Permission",
    human: "Human Agency",
    description: "That which may be, contingent on creaturely response. Represents the space for human freedom within divine providence."
  },
  WITNESS: {
    divine: "Divine Testimony",
    human: "Human Testimony",
    description: "The bridge between divine truth and human understanding. Through witness, eternal truth becomes accessible to finite minds."
  },
  SEPARATION: {
    divine: "Holy Distinction",
    human: "Discernment",
    description: "The act of distinguishing essence from accident, sacred from profane, eternal from temporal."
  },
  STAYING: {
    divine: "Divine Faithfulness",
    human: "Perseverance",
    description: "The covenantal endurance that maintains relationship across time. God's steadfast love meets human faithfulness."
  }
};

// Interface for Modal Encoding
export interface ModalEncoding {
  operatorType: ModalOperatorType;
  symbol: string;
  formula: string;
  interpretation: string;
  scope: string;
  confidence: number;
  theologicalContext?: string;
}

// Interface for Modal Analysis Result
export interface ModalAnalysis {
  encodings: ModalEncoding[];
  themes: string[];
  primaryOperator: ModalOperatorType;
  confidence: number;
  reasoning: string;
}

// Interface for Inference Rule
export interface InferenceRule {
  name: string;
  premise: string;
  conclusion: string;
  description: string;
}

// Modal Logic Inference Rules
export const INFERENCE_RULES: InferenceRule[] = [
  {
    name: "Necessitation",
    premise: "⊢ P",
    conclusion: "⊢ □P",
    description: "If P is a theorem, then necessarily P"
  },
  {
    name: "Dual",
    premise: "□P",
    conclusion: "¬◇¬P",
    description: "Necessity is equivalent to the impossibility of the contrary"
  },
  {
    name: "T-Axiom",
    premise: "□P",
    conclusion: "P",
    description: "What is necessary is actual (reflexivity)"
  },
  {
    name: "4-Axiom",
    premise: "□P",
    conclusion: "□□P",
    description: "Necessity implies necessary necessity (transitivity)"
  },
  {
    name: "5-Axiom",
    premise: "◇P",
    conclusion: "□◇P",
    description: "Possibility implies necessary possibility (euclidean)"
  },
  {
    name: "Witness-Formation",
    premise: "□P ∧ ◇Q",
    conclusion: "W(P,Q)",
    description: "Divine necessity and human possibility form a witness"
  },
  {
    name: "Separation-Principle",
    premise: "W(P,Q)",
    conclusion: "σ(P,essence) ∧ σ(Q,accident)",
    description: "Witness enables separation of essence and accident"
  },
  {
    name: "Staying-Condition",
    premise: "□F ∧ ◇H",
    conclusion: "π(F,H)",
    description: "Divine faithfulness and human hope enable staying"
  }
];

/**
 * Modal Logic Engine Class
 */
export class ModalEngine {
  private hashAlgorithm = 'sha256';

  /**
   * Analyze a text passage for modal operators
   */
  analyzePassage(text: string, reference: string): ModalAnalysis {
    const encodings: ModalEncoding[] = [];
    const themes: string[] = [];
    const textLower = text.toLowerCase();

    // Detect necessity patterns (□)
    if (this.detectNecessity(textLower)) {
      encodings.push(this.createNecessityEncoding(text, reference));
      themes.push('Divine Sovereignty', 'God\'s Decree', 'Eternal Purpose');
    }

    // Detect possibility patterns (◇)
    if (this.detectPossibility(textLower)) {
      encodings.push(this.createPossibilityEncoding(text, reference));
      if (!themes.includes('Human Agency')) {
        themes.push('Human Agency', 'Contingency', 'Free Will');
      }
    }

    // Detect witness patterns (W)
    if (this.detectWitness(textLower)) {
      encodings.push(this.createWitnessEncoding(text, reference));
      themes.push('Testimony', 'Revelation', 'Faith');
    }

    // Detect separation patterns (σ)
    if (this.detectSeparation(textLower)) {
      encodings.push(this.createSeparationEncoding(text, reference));
      themes.push('Holiness', 'Discernment', 'Sacred/Profane');
    }

    // Detect staying patterns (π)
    if (this.detectStaying(textLower)) {
      encodings.push(this.createStayingEncoding(text, reference));
      themes.push('Faithfulness', 'Perseverance', 'Covenant');
    }

    // Determine primary operator
    const primaryOperator = this.determinePrimaryOperator(encodings);
    
    // Calculate overall confidence
    const confidence = encodings.length > 0 
      ? encodings.reduce((sum, e) => sum + e.confidence, 0) / encodings.length 
      : 0.5;

    return {
      encodings,
      themes: [...new Set(themes)],
      primaryOperator,
      confidence,
      reasoning: this.generateReasoning(encodings, reference)
    };
  }

  /**
   * Apply inference rules
   */
  applyInference(encodings: ModalEncoding[]): {
    derived: ModalEncoding[];
    rules: string[];
  } {
    const derived: ModalEncoding[] = [];
    const rules: string[] = [];

    for (const rule of INFERENCE_RULES) {
      const applicable = this.checkRuleApplicability(rule, encodings);
      if (applicable) {
        const newEncoding = this.deriveEncoding(rule, encodings);
        if (newEncoding) {
          derived.push(newEncoding);
          rules.push(rule.name);
        }
      }
    }

    return { derived, rules };
  }

  /**
   * Generate proof hash for verification
   */
  generateProofHash(analysis: ModalAnalysis, passageId: string): string {
    const data = JSON.stringify({
      passageId,
      encodings: analysis.encodings.map(e => ({
        op: e.operatorType,
        formula: e.formula,
        confidence: e.confidence
      })),
      themes: analysis.themes,
      timestamp: Date.now()
    });

    return createHash(this.hashAlgorithm).update(data).digest('hex');
  }

  /**
   * Create a modal formula string
   */
  createFormula(operator: ModalOperatorType, proposition: string): string {
    const symbol = MODAL_SYMBOLS[operator];
    switch (operator) {
      case 'NECESSITY':
        return `${symbol}${proposition}`;
      case 'POSSIBILITY':
        return `${symbol}${proposition}`;
      case 'WITNESS':
        return `W(divine, human)`;
      case 'SEPARATION':
        return `σ(${proposition}, essence)`;
      case 'STAYING':
        return `π(faithfulness, hope)`;
      default:
        return `${symbol}${proposition}`;
    }
  }

  // Private helper methods

  private detectNecessity(text: string): boolean {
    const patterns = [
      'must', 'necessarily', 'certainly', 'surely', 'indeed',
      'god said', 'it is written', 'declares the lord', 'thus says',
      'shall', 'will surely', 'will certainly', 'i am', 'i will be'
    ];
    return patterns.some(p => text.includes(p));
  }

  private detectPossibility(text: string): boolean {
    const patterns = [
      'may', 'might', 'could', 'perhaps', 'if', 'unless',
      'choose', 'voluntary', 'free', 'option', 'whether',
      'whoever', 'whosoever', 'anyone who'
    ];
    return patterns.some(p => text.includes(p));
  }

  private detectWitness(text: string): boolean {
    const patterns = [
      'testify', 'witness', 'bear witness', 'testimony',
      'proclaim', 'declare', 'announce', 'preach', 'speak',
      'tell', 'report', 'record', 'remember', 'memorial'
    ];
    return patterns.some(p => text.includes(p));
  }

  private detectSeparation(text: string): boolean {
    const patterns = [
      'separate', 'set apart', 'holy', 'sanctify', 'clean', 'unclean',
      'pure', 'impure', 'sacred', 'profane', 'dedicate', 'consecrate',
      'distinguish', 'discern', 'difference', 'divide'
    ];
    return patterns.some(p => text.includes(p));
  }

  private detectStaying(text: string): boolean {
    const patterns = [
      'remain', 'abide', 'stay', 'continue', 'endure', 'persevere',
      'faithful', 'steadfast', 'keep', 'hold fast', 'stand firm',
      'patient', 'wait', 'trust', 'believe', 'covenant', 'forever'
    ];
    return patterns.some(p => text.includes(p));
  }

  private createNecessityEncoding(text: string, reference: string): ModalEncoding {
    return {
      operatorType: 'NECESSITY',
      symbol: MODAL_SYMBOLS.NECESSITY,
      formula: this.createFormula('NECESSITY', 'P'),
      interpretation: MODAL_INTERPRETATIONS.NECESSITY.description,
      scope: 'Divine decree or sovereign will',
      confidence: 0.85,
      theologicalContext: 'Represents God\'s unchangeable purpose and eternal decree'
    };
  }

  private createPossibilityEncoding(text: string, reference: string): ModalEncoding {
    return {
      operatorType: 'POSSIBILITY',
      symbol: MODAL_SYMBOLS.POSSIBILITY,
      formula: this.createFormula('POSSIBILITY', 'Q'),
      interpretation: MODAL_INTERPRETATIONS.POSSIBILITY.description,
      scope: 'Human response or contingent circumstance',
      confidence: 0.80,
      theologicalContext: 'Represents the space for genuine human freedom and choice'
    };
  }

  private createWitnessEncoding(text: string, reference: string): ModalEncoding {
    return {
      operatorType: 'WITNESS',
      symbol: MODAL_SYMBOLS.WITNESS,
      formula: this.createFormula('WITNESS', 'testimony'),
      interpretation: MODAL_INTERPRETATIONS.WITNESS.description,
      scope: 'Bridge between divine truth and human understanding',
      confidence: 0.82,
      theologicalContext: 'The means by which eternal truth becomes accessible to finite minds'
    };
  }

  private createSeparationEncoding(text: string, reference: string): ModalEncoding {
    return {
      operatorType: 'SEPARATION',
      symbol: MODAL_SYMBOLS.SEPARATION,
      formula: this.createFormula('SEPARATION', 'P'),
      interpretation: MODAL_INTERPRETATIONS.SEPARATION.description,
      scope: 'Distinction between essence and accident',
      confidence: 0.78,
      theologicalContext: 'God\'s act of making holy, setting apart for divine purpose'
    };
  }

  private createStayingEncoding(text: string, reference: string): ModalEncoding {
    return {
      operatorType: 'STAYING',
      symbol: MODAL_SYMBOLS.STAYING,
      formula: this.createFormula('STAYING', 'faithfulness'),
      interpretation: MODAL_INTERPRETATIONS.STAYING.description,
      scope: 'Covenantal endurance and perseverance',
      confidence: 0.80,
      theologicalContext: 'The covenantal faithfulness that sustains relationship'
    };
  }

  private determinePrimaryOperator(encodings: ModalEncoding[]): ModalOperatorType {
    if (encodings.length === 0) return 'NECESSITY';
    
    // Priority order for primary operator
    const priority: ModalOperatorType[] = ['WITNESS', 'NECESSITY', 'POSSIBILITY', 'SEPARATION', 'STAYING'];
    
    for (const op of priority) {
      if (encodings.some(e => e.operatorType === op)) {
        return op;
      }
    }
    
    return encodings[0].operatorType;
  }

  private generateReasoning(encodings: ModalEncoding[], reference: string): string {
    if (encodings.length === 0) {
      return `No modal operators detected in ${reference}. Consider manual analysis.`;
    }

    const operators = encodings.map(e => `${e.symbol} (${e.operatorType.toLowerCase()})`).join(', ');
    return `Analysis of ${reference} reveals the following modal operators: ${operators}. ` +
           `The primary operator is ${encodings[0].operatorType.toLowerCase()}, indicating ` +
           `${encodings[0].interpretation}`;
  }

  private checkRuleApplicability(rule: InferenceRule, encodings: ModalEncoding[]): boolean {
    switch (rule.name) {
      case 'Witness-Formation':
        return encodings.some(e => e.operatorType === 'NECESSITY') &&
               encodings.some(e => e.operatorType === 'POSSIBILITY');
      case 'Separation-Principle':
        return encodings.some(e => e.operatorType === 'WITNESS');
      case 'Staying-Condition':
        return encodings.some(e => e.operatorType === 'NECESSITY');
      default:
        return encodings.length > 0;
    }
  }

  private deriveEncoding(rule: InferenceRule, encodings: ModalEncoding[]): ModalEncoding | null {
    switch (rule.name) {
      case 'Witness-Formation':
        return {
          operatorType: 'WITNESS',
          symbol: 'W',
          formula: 'W(□P, ◇Q)',
          interpretation: 'Derived: Divine necessity and human possibility form a witness',
          scope: 'Inferred from modal combination',
          confidence: 0.75
        };
      case 'Separation-Principle':
        return {
          operatorType: 'SEPARATION',
          symbol: 'σ',
          formula: 'σ(W, essence)',
          interpretation: 'Derived: Witness enables separation of essence and accident',
          scope: 'Inferred from witness formation',
          confidence: 0.72
        };
      case 'Staying-Condition':
        return {
          operatorType: 'STAYING',
          symbol: 'π',
          formula: 'π(□F, ◇H)',
          interpretation: 'Derived: Divine faithfulness meets human hope',
          scope: 'Inferred from necessity',
          confidence: 0.70
        };
      default:
        return null;
    }
  }
}

// Export singleton instance
export const modalEngine = new ModalEngine();

// Utility functions
export function formatModalFormula(encoding: ModalEncoding): string {
  return `${encoding.symbol} ${encoding.formula}`;
}

export function getOperatorColor(operator: ModalOperatorType): string {
  const colors: Record<ModalOperatorType, string> = {
    NECESSITY: '#c9a227', // Gold
    POSSIBILITY: '#4a90d9', // Blue
    WITNESS: '#8b5cf6', // Purple
    SEPARATION: '#059669', // Emerald
    STAYING: '#dc2626' // Red
  };
  return colors[operator];
}

export function getOperatorGradient(operator: ModalOperatorType): string {
  const gradients: Record<ModalOperatorType, string> = {
    NECESSITY: 'from-amber-500 to-yellow-600',
    POSSIBILITY: 'from-blue-400 to-indigo-500',
    WITNESS: 'from-purple-500 to-violet-600',
    SEPARATION: 'from-emerald-500 to-teal-600',
    STAYING: 'from-red-500 to-rose-600'
  };
  return gradients[operator];
}
