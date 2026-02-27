/**
 * Iota Verbum (IV) - Deterministic AI Reasoning API
 * Provides reproducible, verifiable AI analysis with modal logic enhancement
 */

import { NextRequest, NextResponse } from 'next/server';
import { modalEngine, ModalOperatorType, MODAL_SYMBOLS, MODAL_INTERPRETATIONS } from '@/lib/modal-engine';
import { ethicsEngine } from '@/lib/ethics-engine';
import { z } from 'zod';
import ZAI from 'z-ai-web-dev-sdk';

const ReasonRequestSchema = z.object({
  query: z.string().min(1),
  context: z.string().optional(),
  modalOperators: z.array(z.string()).optional(),
  temperature: z.number().min(0).max(1).default(0),
  maxTokens: z.number().min(100).max(2000).default(800),
  includeEthicsReview: z.boolean().default(true),
});

interface ReasoningResult {
  query: string;
  analysis: string;
  modalContext: {
    operators: ModalOperatorType[];
    primaryOperator: ModalOperatorType | null;
    interpretation: string;
  };
  ethicsReview?: {
    passed: boolean;
    score: number;
    recommendation: string;
  };
  metadata: {
    deterministic: boolean;
    temperature: number;
    tokenCount?: number;
    processingTime: number;
  };
}

// GET - Available modal operators and their meanings
export async function GET() {
  return NextResponse.json({
    operators: Object.entries(MODAL_SYMBOLS).map(([type, symbol]) => ({
      type,
      symbol,
      ...MODAL_INTERPRETATIONS[type as ModalOperatorType]
    })),
    inferenceRules: [
      { name: 'Necessitation', premise: '⊢ P', conclusion: '⊢ □P' },
      { name: 'Dual', premise: '□P', conclusion: '¬◇¬P' },
      { name: 'T-Axiom', premise: '□P', conclusion: 'P' },
      { name: 'Witness-Formation', premise: '□P ∧ ◇Q', conclusion: 'W(P,Q)' },
    ]
  });
}

// POST - Perform deterministic reasoning
export async function POST(request: NextRequest) {
  const startTime = Date.now();
  
  try {
    const body = await request.json();
    const { 
      query, 
      context, 
      modalOperators, 
      temperature, 
      maxTokens,
      includeEthicsReview 
    } = ReasonRequestSchema.parse(body);

    // Analyze the query for modal operators
    const modalAnalysis = modalEngine.analyzePassage(query, 'query');
    
    // Determine which modal operators to emphasize
    const relevantOperators: ModalOperatorType[] = modalOperators?.length 
      ? modalOperators as ModalOperatorType[]
      : [modalAnalysis.primaryOperator];

    // Build modal-enhanced system prompt
    const modalContextStr = relevantOperators
      .map(op => `${MODAL_SYMBOLS[op]}: ${MODAL_INTERPRETATIONS[op].description}`)
      .join('\n');

    // Create deterministic AI prompt
    const systemPrompt = `You are the Iota Verbum (IV) Reasoning Engine - a deterministic AI system for theological and philosophical analysis.

You operate using modal logic operators:
${modalContextStr}

Key principles:
1. □ (Necessity) represents divine decree, unchangeable truths
2. ◇ (Possibility) represents human agency, contingent events
3. W (Witness) bridges divine truth and human understanding
4. σ (Separation) distinguishes essence from accident
5. π (Staying) represents faithfulness and perseverance

Provide precise, scholarly analysis that is:
- Theologically sound and biblically grounded
- Logically rigorous with clear reasoning chains
- Deterministic and reproducible (same input → same output)
- Transparent in methodology

Format your response with clear sections when appropriate.`;

    // Call AI with deterministic settings
    const zai = await ZAI.create();
    const completion = await zai.chat.completions.create({
      messages: [
        { role: 'system', content: systemPrompt },
        ...(context ? [{ role: 'user' as const, content: `Context: ${context}` }] : []),
        { role: 'user', content: query }
      ],
      temperature,
      max_tokens: maxTokens,
    });

    const analysis = completion.choices[0]?.message?.content || 'No analysis generated.';

    // Perform ethics review if requested
    let ethicsReview;
    if (includeEthicsReview) {
      const report = await ethicsEngine.reviewContent({
        text: analysis,
        category: 'generated',
      });
      ethicsReview = {
        passed: report.overallPassed,
        score: report.overallScore,
        recommendation: report.recommendation,
      };
    }

    const processingTime = Date.now() - startTime;

    const result: ReasoningResult = {
      query,
      analysis,
      modalContext: {
        operators: relevantOperators,
        primaryOperator: modalAnalysis.primaryOperator,
        interpretation: MODAL_INTERPRETATIONS[modalAnalysis.primaryOperator].description,
      },
      ethicsReview,
      metadata: {
        deterministic: temperature === 0,
        temperature,
        tokenCount: completion.usage?.total_tokens,
        processingTime,
      }
    };

    // Save analysis session to database
    try {
      await prisma.analysisSession.create({
        data: {
          input: query,
          output: analysis,
          modalContext: JSON.stringify(result.modalContext),
          deterministic: temperature === 0,
          temperature,
          tokenCount: result.metadata.tokenCount,
        }
      });
    } catch {
      // Continue if database save fails
    }

    return NextResponse.json(result);
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Validation failed', details: error.errors },
        { status: 400 }
      );
    }
    console.error('Reasoning error:', error);
    return NextResponse.json(
      { error: 'Reasoning failed', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}

// Import prisma for session saving
import prisma from '@/lib/db';
