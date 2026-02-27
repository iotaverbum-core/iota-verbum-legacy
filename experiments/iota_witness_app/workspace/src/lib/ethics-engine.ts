/**
 * Iota Verbum (IV) - Ethics Engine
 * 
 * A principled ethics review system grounded in Christian ethics
 * for evaluating AI outputs and ensuring alignment with moral principles.
 */

import { createHash } from 'crypto';

// Core Ethical Principles
export type EthicsPrinciple = 
  | 'SANCTITY_OF_LIFE'
  | 'TRUTHFULNESS'
  | 'STEWARDSHIP'
  | 'LOVE'
  | 'JUSTICE'
  | 'HONOR'
  | 'PURITY';

// Principle Definitions
export const PRINCIPLE_DEFINITIONS: Record<EthicsPrinciple, {
  name: string;
  description: string;
  biblicalBasis: string;
  keyQuestions: string[];
}> = {
  SANCTITY_OF_LIFE: {
    name: "Sanctity of Life",
    description: "Human life is sacred, created in God's image, and must be protected and valued.",
    biblicalBasis: "Genesis 1:27, Psalm 139:13-16, Jeremiah 1:5",
    keyQuestions: [
      "Does this content promote the protection of human life?",
      "Could this content be interpreted as devaluing human dignity?",
      "Does this content support or encourage harm to others?"
    ]
  },
  TRUTHFULNESS: {
    name: "Truthfulness",
    description: "Honesty and accuracy in communication, reflecting God's nature as truth.",
    biblicalBasis: "Exodus 20:16, John 14:6, Ephesians 4:25",
    keyQuestions: [
      "Is the content factually accurate to the best of our knowledge?",
      "Are there any misleading statements or half-truths?",
      "Does this content promote honesty and integrity?"
    ]
  },
  STEWARDSHIP: {
    name: "Stewardship",
    description: "Responsible care for God's creation and the resources entrusted to us.",
    biblicalBasis: "Genesis 2:15, Psalm 24:1, 1 Peter 4:10",
    keyQuestions: [
      "Does this content encourage responsible use of resources?",
      "Is there consideration for environmental impact?",
      "Does this promote generosity over greed?"
    ]
  },
  LOVE: {
    name: "Love",
    description: "Selfless concern for others' well-being, following Christ's example.",
    biblicalBasis: "Matthew 22:37-39, John 13:34-35, 1 Corinthians 13",
    keyQuestions: [
      "Does this content promote love for others?",
      "Could this content cause unnecessary harm or offense?",
      "Does this reflect Christ's love for all people?"
    ]
  },
  JUSTICE: {
    name: "Justice",
    description: "Fairness, equity, and standing against oppression and exploitation.",
    biblicalBasis: "Micah 6:8, Isaiah 1:17, James 1:27",
    keyQuestions: [
      "Does this content promote fairness and equity?",
      "Could this content enable discrimination or bias?",
      "Does this speak up for the marginalized?"
    ]
  },
  HONOR: {
    name: "Honor",
    description: "Respect for God, authority, and the dignity of all persons.",
    biblicalBasis: "Exodus 20:12, Romans 13:7, 1 Peter 2:17",
    keyQuestions: [
      "Does this content show appropriate respect?",
      "Are there any disrespectful or demeaning elements?",
      "Does this honor God and reflect His character?"
    ]
  },
  PURITY: {
    name: "Purity",
    description: "Moral and sexual purity, guarding the heart and mind.",
    biblicalBasis: "Matthew 5:8, Philippians 4:8, 1 Thessalonians 4:3-7",
    keyQuestions: [
      "Is this content free from inappropriate or harmful material?",
      "Does this promote wholesome thoughts and actions?",
      "Could this content lead others into temptation?"
    ]
  }
};

// Ethics Review Result
export interface EthicsReview {
  principle: EthicsPrinciple;
  passed: boolean;
  score: number;
  reasoning: string;
  concerns: string[];
  suggestions: string[];
}

// Comprehensive Ethics Report
export interface EthicsReport {
  reviews: EthicsReview[];
  overallPassed: boolean;
  overallScore: number;
  summary: string;
  recommendation: 'APPROVED' | 'NEEDS_REVIEW' | 'REJECTED';
  hash: string;
  timestamp: Date;
}

// Content Analysis Context
export interface ContentContext {
  text: string;
  source?: string;
  category?: 'scripture' | 'commentary' | 'analysis' | 'generated';
  targetAudience?: string;
}

/**
 * Ethics Engine Class
 */
export class EthicsEngine {
  private criticalPrinciples: EthicsPrinciple[] = ['SANCTITY_OF_LIFE', 'TRUTHFULNESS', 'LOVE'];
  private passingThreshold = 0.7;
  private criticalThreshold = 0.8;

  /**
   * Perform comprehensive ethics review
   */
  async reviewContent(context: ContentContext): Promise<EthicsReport> {
    const reviews: EthicsReview[] = [];

    // Review against each principle
    for (const principle of Object.keys(PRINCIPLE_DEFINITIONS) as EthicsPrinciple[]) {
      const review = await this.reviewAgainstPrinciple(context, principle);
      reviews.push(review);
    }

    // Calculate overall metrics
    const overallScore = this.calculateOverallScore(reviews);
    const overallPassed = this.determineOverallPass(reviews);
    const recommendation = this.determineRecommendation(reviews, overallScore);

    // Generate summary
    const summary = this.generateSummary(reviews, overallScore, recommendation);

    // Generate hash for verification
    const hash = this.generateReportHash(reviews, context.text);

    return {
      reviews,
      overallPassed,
      overallScore,
      summary,
      recommendation,
      hash,
      timestamp: new Date()
    };
  }

  /**
   * Review content against a specific principle
   */
  private async reviewAgainstPrinciple(
    context: ContentContext, 
    principle: EthicsPrinciple
  ): Promise<EthicsReview> {
    const definition = PRINCIPLE_DEFINITIONS[principle];
    const textLower = context.text.toLowerCase();
    
    let score = 1.0; // Start with perfect score
    const concerns: string[] = [];
    const suggestions: string[] = [];

    // Analyze content based on principle
    switch (principle) {
      case 'SANCTITY_OF_LIFE':
        const lifeAnalysis = this.analyzeSanctityOfLife(textLower);
        score = lifeAnalysis.score;
        concerns.push(...lifeAnalysis.concerns);
        break;
      
      case 'TRUTHFULNESS':
        const truthAnalysis = this.analyzeTruthfulness(textLower, context);
        score = truthAnalysis.score;
        concerns.push(...truthAnalysis.concerns);
        break;
      
      case 'STEWARDSHIP':
        const stewardAnalysis = this.analyzeStewardship(textLower);
        score = stewardAnalysis.score;
        concerns.push(...stewardAnalysis.concerns);
        break;
      
      case 'LOVE':
        const loveAnalysis = this.analyzeLove(textLower);
        score = loveAnalysis.score;
        concerns.push(...loveAnalysis.concerns);
        break;
      
      case 'JUSTICE':
        const justiceAnalysis = this.analyzeJustice(textLower);
        score = justiceAnalysis.score;
        concerns.push(...justiceAnalysis.concerns);
        break;
      
      case 'HONOR':
        const honorAnalysis = this.analyzeHonor(textLower);
        score = honorAnalysis.score;
        concerns.push(...honorAnalysis.concerns);
        break;
      
      case 'PURITY':
        const purityAnalysis = this.analyzePurity(textLower);
        score = purityAnalysis.score;
        concerns.push(...purityAnalysis.concerns);
        break;
    }

    // Generate suggestions for concerns
    for (const concern of concerns) {
      suggestions.push(this.generateSuggestion(principle, concern));
    }

    const passed = this.isCriticalPrinciple(principle) 
      ? score >= this.criticalThreshold 
      : score >= this.passingThreshold;

    return {
      principle,
      passed,
      score,
      reasoning: this.generateReasoning(principle, score, concerns),
      concerns,
      suggestions
    };
  }

  // Principle-specific analyzers

  private analyzeSanctityOfLife(text: string): { score: number; concerns: string[] } {
    const concerns: string[] = [];
    let score = 1.0;

    // Check for harmful content
    const harmPatterns = ['kill', 'murder', 'suicide', 'abort', 'euthanasia', 'destroy'];
    for (const pattern of harmPatterns) {
      if (text.includes(pattern)) {
        // Context matters - scripture may reference these without endorsing
        if (!text.includes('shall not') && !text.includes('command') && !text.includes('sin')) {
          concerns.push(`Content references '${pattern}' - verify context`);
          score -= 0.15;
        }
      }
    }

    // Check for positive life-affirming content
    const affirmingPatterns = ['life', 'live', 'born', 'create', 'protect', 'save', 'heal'];
    let affirmingCount = 0;
    for (const pattern of affirmingPatterns) {
      if (text.includes(pattern)) affirmingCount++;
    }
    score = Math.min(1.0, score + (affirmingCount * 0.05));

    return { score: Math.max(0, Math.min(1, score)), concerns };
  }

  private analyzeTruthfulness(text: string, context: ContentContext): { score: number; concerns: string[] } {
    const concerns: string[] = [];
    let score = 1.0;

    // Check for uncertainty markers (good for honesty)
    const uncertaintyMarkers = ['perhaps', 'may', 'might', 'possibly', 'some interpret'];
    
    // Check for false certainty
    const certaintyPatterns = ['definitely', 'certainly', 'without doubt', 'clearly'];
    let hasCertainty = false;
    for (const pattern of certaintyPatterns) {
      if (text.includes(pattern)) {
        hasCertainty = true;
        break;
      }
    }

    // Scripture is generally trustworthy
    if (context.category === 'scripture') {
      score = 0.95;
    }

    // Check for qualification in analysis
    if (context.category === 'analysis' || context.category === 'commentary') {
      const hasQualification = uncertaintyMarkers.some(m => text.includes(m));
      if (!hasQualification && hasCertainty) {
        concerns.push('Strong certainty claims without qualification');
        score -= 0.1;
      }
    }

    return { score: Math.max(0, Math.min(1, score)), concerns };
  }

  private analyzeStewardship(text: string): { score: number; concerns: string[] } {
    const concerns: string[] = [];
    let score = 0.85; // Default good score

    // Check for positive stewardship themes
    const positivePatterns = ['care', 'tend', 'keep', 'preserve', 'manage', 'responsible'];
    for (const pattern of positivePatterns) {
      if (text.includes(pattern)) score += 0.03;
    }

    // Check for potential misuse
    const concernPatterns = ['exploit', 'waste', 'destroy', 'consume excess'];
    for (const pattern of concernPatterns) {
      if (text.includes(pattern)) {
        concerns.push(`Content may relate to '${pattern}' - verify context`);
        score -= 0.1;
      }
    }

    return { score: Math.max(0, Math.min(1, score)), concerns };
  }

  private analyzeLove(text: string): { score: number; concerns: string[] } {
    const concerns: string[] = [];
    let score = 0.9;

    // Check for love-affirming content
    const lovePatterns = ['love', 'care', 'compassion', 'mercy', 'kindness', 'forgive'];
    for (const pattern of lovePatterns) {
      if (text.includes(pattern)) score += 0.02;
    }

    // Check for potentially harmful content
    const harmPatterns = ['hate', 'enemy', 'destroy', 'curse'];
    for (const pattern of harmPatterns) {
      if (text.includes(pattern)) {
        // Context matters
        if (!text.includes('love your') && !text.includes('pray for')) {
          concerns.push(`Content contains '${pattern}' - verify it doesn't promote hatred`);
          score -= 0.1;
        }
      }
    }

    return { score: Math.max(0, Math.min(1, score)), concerns };
  }

  private analyzeJustice(text: string): { score: number; concerns: string[] } {
    const concerns: string[] = [];
    let score = 0.85;

    // Check for justice-affirming content
    const justicePatterns = ['justice', 'fair', 'righteous', 'equity', 'oppressed', 'widow', 'orphan'];
    for (const pattern of justicePatterns) {
      if (text.includes(pattern)) score += 0.02;
    }

    // Check for potential bias indicators
    const biasPatterns = ['those people', 'all [group]', 'typical', 'always', 'never'];
    for (const pattern of biasPatterns) {
      if (text.includes(pattern)) {
        concerns.push('Potential stereotyping language detected');
        score -= 0.15;
      }
    }

    return { score: Math.max(0, Math.min(1, score)), concerns };
  }

  private analyzeHonor(text: string): { score: number; concerns: string[] } {
    const concerns: string[] = [];
    let score = 0.9;

    // Check for honor-affirming content
    const honorPatterns = ['honor', 'respect', 'glory', 'praise', 'worship', 'bless'];
    for (const pattern of honorPatterns) {
      if (text.includes(pattern)) score += 0.02;
    }

    // Check for dishonoring content
    const dishonorPatterns = ['shame', 'disgrace', 'mock', 'ridicule', 'blaspheme'];
    for (const pattern of dishonorPatterns) {
      if (text.includes(pattern)) {
        concerns.push(`Content contains '${pattern}' - verify context`);
        score -= 0.1;
      }
    }

    return { score: Math.max(0, Math.min(1, score)), concerns };
  }

  private analyzePurity(text: string): { score: number; concerns: string[] } {
    const concerns: string[] = [];
    let score = 0.95;

    // Scripture passages are assumed pure
    // Check for concerning content
    const concernPatterns = ['sexual immorality', 'adultery', 'fornication', 'lust'];
    for (const pattern of concernPatterns) {
      if (text.includes(pattern)) {
        concerns.push(`Content references '${pattern}' - ensure appropriate handling`);
        score -= 0.1;
      }
    }

    return { score: Math.max(0, Math.min(1, score)), concerns };
  }

  // Helper methods

  private isCriticalPrinciple(principle: EthicsPrinciple): boolean {
    return this.criticalPrinciples.includes(principle);
  }

  private calculateOverallScore(reviews: EthicsReview[]): number {
    if (reviews.length === 0) return 0;
    
    // Weight critical principles more heavily
    let totalWeight = 0;
    let weightedSum = 0;
    
    for (const review of reviews) {
      const weight = this.isCriticalPrinciple(review.principle) ? 2 : 1;
      weightedSum += review.score * weight;
      totalWeight += weight;
    }
    
    return weightedSum / totalWeight;
  }

  private determineOverallPass(reviews: EthicsReview[]): boolean {
    // Must pass all critical principles
    for (const review of reviews) {
      if (this.isCriticalPrinciple(review.principle) && !review.passed) {
        return false;
      }
    }
    
    // Must have overall score above threshold
    return this.calculateOverallScore(reviews) >= this.passingThreshold;
  }

  private determineRecommendation(
    reviews: EthicsReview[], 
    overallScore: number
  ): 'APPROVED' | 'NEEDS_REVIEW' | 'REJECTED' {
    // Check for any rejected critical principles
    for (const review of reviews) {
      if (this.isCriticalPrinciple(review.principle) && review.score < 0.5) {
        return 'REJECTED';
      }
    }

    // Check overall score
    if (overallScore >= 0.9) return 'APPROVED';
    if (overallScore >= 0.7) return 'NEEDS_REVIEW';
    return 'REJECTED';
  }

  private generateSummary(
    reviews: EthicsReview[], 
    overallScore: number, 
    recommendation: string
  ): string {
    const passedCount = reviews.filter(r => r.passed).length;
    const totalConcerns = reviews.reduce((sum, r) => sum + r.concerns.length, 0);
    
    let summary = `Ethics review complete. ${passedCount}/${reviews.length} principles passed. `;
    summary += `Overall score: ${(overallScore * 100).toFixed(1)}%. `;
    
    if (totalConcerns > 0) {
      summary += `${totalConcerns} concern(s) identified. `;
    }
    
    summary += `Recommendation: ${recommendation}.`;
    
    return summary;
  }

  private generateReasoning(
    principle: EthicsPrinciple, 
    score: number, 
    concerns: string[]
  ): string {
    const definition = PRINCIPLE_DEFINITIONS[principle];
    
    if (concerns.length === 0) {
      return `${definition.name} principle satisfied with score ${(score * 100).toFixed(1)}%. ` +
             `Content aligns with ${definition.description.toLowerCase()}`;
    }
    
    return `${definition.name} review identified ${concerns.length} concern(s). ` +
           `Score: ${(score * 100).toFixed(1)}%. Please review the concerns and verify context.`;
  }

  private generateSuggestion(principle: EthicsPrinciple, concern: string): string {
    return `Consider reviewing: ${concern}. Verify that content appropriately addresses ${PRINCIPLE_DEFINITIONS[principle].name.toLowerCase()} concerns.`;
  }

  private generateReportHash(reviews: EthicsReview[], text: string): string {
    const data = JSON.stringify({
      reviews: reviews.map(r => ({
        p: r.principle,
        s: r.score,
        c: r.concerns.length
      })),
      textLength: text.length,
      timestamp: Date.now()
    });
    
    return createHash('sha256').update(data).digest('hex').substring(0, 16);
  }
}

// Export singleton instance
export const ethicsEngine = new EthicsEngine();

// Utility functions
export function getPrincipleColor(principle: EthicsPrinciple): string {
  const colors: Record<EthicsPrinciple, string> = {
    SANCTITY_OF_LIFE: '#dc2626',
    TRUTHFULNESS: '#2563eb',
    STEWARDSHIP: '#16a34a',
    LOVE: '#ec4899',
    JUSTICE: '#9333ea',
    HONOR: '#ea580c',
    PURITY: '#0891b2'
  };
  return colors[principle];
}

export function getPrincipleGradient(principle: EthicsPrinciple): string {
  const gradients: Record<EthicsPrinciple, string> = {
    SANCTITY_OF_LIFE: 'from-red-500 to-rose-600',
    TRUTHFULNESS: 'from-blue-500 to-indigo-600',
    STEWARDSHIP: 'from-green-500 to-emerald-600',
    LOVE: 'from-pink-500 to-rose-500',
    JUSTICE: 'from-purple-500 to-violet-600',
    HONOR: 'from-orange-500 to-amber-600',
    PURITY: 'from-cyan-500 to-teal-600'
  };
  return gradients[principle];
}
