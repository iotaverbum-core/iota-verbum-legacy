/**
 * Iota Verbum (IV) - Witness Card Generator API
 * Creates comprehensive analysis cards for scripture passages
 */

import { NextRequest, NextResponse } from 'next/server';
import prisma from '@/lib/db';
import { modalEngine, ModalAnalysis } from '@/lib/modal-engine';
import { ethicsEngine, EthicsReport } from '@/lib/ethics-engine';
import { z } from 'zod';
import ZAI from 'z-ai-web-dev-sdk';

const CreateWitnessCardSchema = z.object({
  passageId: z.string().min(1),
  title: z.string().optional(),
  includeAIAnalysis: z.boolean().default(true),
});

// Sample scripture data for demo purposes
const SAMPLE_PASSAGES = [
  {
    id: 'demo-1',
    book: 'John',
    chapter: 1,
    verseStart: 1,
    textEn: 'In the beginning was the Word, and the Word was with God, and the Word was God.',
    textOriginal: 'Ἐν ἀρχῇ ἦν ὁ Λόγος, καὶ ὁ Λόγος ἦν πρὸς τὸν Θεόν, καὶ Θεὸς ἦν ὁ Λόγος.',
    originalLanguage: 'Greek',
  },
  {
    id: 'demo-2',
    book: 'Genesis',
    chapter: 1,
    verseStart: 1,
    textEn: 'In the beginning, God created the heavens and the earth.',
    textOriginal: 'בְּרֵאשִׁית בָּרָא אֱלֹהִים אֵת הַשָּׁמַיִם וְאֵת הָאָרֶץ',
    originalLanguage: 'Hebrew',
  },
  {
    id: 'demo-3',
    book: 'Matthew',
    chapter: 5,
    verseStart: 3,
    textEn: 'Blessed are the poor in spirit, for theirs is the kingdom of heaven.',
    textOriginal: 'Μακάριοι οἱ πτωχοὶ τῷ πνεύματι, ὅτι αὐτῶν ἐστιν ἡ βασιλεία τῶν οὐρανῶν.',
    originalLanguage: 'Greek',
  },
  {
    id: 'demo-4',
    book: 'Psalm',
    chapter: 23,
    verseStart: 1,
    textEn: 'The LORD is my shepherd; I shall not want.',
    textOriginal: 'יְהוָה רֹעִי לֹא אֶחְסָר',
    originalLanguage: 'Hebrew',
  },
  {
    id: 'demo-5',
    book: 'Romans',
    chapter: 8,
    verseStart: 28,
    textEn: 'And we know that for those who love God all things work together for good, for those who are called according to his purpose.',
    textOriginal: 'οἴδαμεν δὲ ὅτι τοῖς ἀγαπῶσιν τὸν Θεὸν πάντα συνεργεῖ εἰς ἀγαθόν, τοῖς κατὰ πρόθεσιν κλητοῖς οὖσιν.',
    originalLanguage: 'Greek',
  },
];

// GET - List witness cards
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const passageId = searchParams.get('passageId');
    const limit = parseInt(searchParams.get('limit') || '20');

    const where = passageId ? { passageId } : {};

    const cards = await prisma.witnessCard.findMany({
      where,
      orderBy: { createdAt: 'desc' },
      take: limit,
      include: {
        passage: true,
        ethicsReviews: true,
      }
    });

    return NextResponse.json({ cards });
  } catch (error) {
    console.error('Error fetching witness cards:', error);
    return NextResponse.json(
      { error: 'Failed to fetch witness cards' },
      { status: 500 }
    );
  }
}

// POST - Generate a new witness card
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { passageId, title, includeAIAnalysis } = CreateWitnessCardSchema.parse(body);

    // Get the passage
    let passage = await prisma.scripturePassage.findUnique({
      where: { id: passageId }
    });

    // Use sample passage for demo if not found
    if (!passage) {
      const samplePassage = SAMPLE_PASSAGES.find(p => p.id === passageId);
      if (samplePassage) {
        passage = {
          ...samplePassage,
          verseEnd: null,
          translation: 'ESV',
          createdAt: new Date(),
          updatedAt: new Date(),
        } as typeof passage;
      }
    }

    if (!passage) {
      return NextResponse.json(
        { error: 'Passage not found' },
        { status: 404 }
      );
    }

    // Perform modal analysis
    const reference = `${passage.book} ${passage.chapter}:${passage.verseStart}`;
    const modalAnalysis = modalEngine.analyzePassage(passage.textEn, reference);

    // Perform ethics review
    const ethicsReport = await ethicsEngine.reviewContent({
      text: passage.textEn,
      source: reference,
      category: 'scripture'
    });

    // Generate AI-enhanced analysis if requested
    let aiAnalysis = null;
    if (includeAIAnalysis) {
      try {
        const zai = await ZAI.create();
        const completion = await zai.chat.completions.create({
          messages: [
            {
              role: 'system',
              content: `You are a theological analysis assistant for the Iota Verbum system. 
              Provide structured analysis of scripture passages using modal logic operators:
              - □ (Necessity): Divine decrees, God's unchangeable will
              - ◇ (Possibility): Human agency, contingent events
              - W (Witness): Connection between divine and human
              - σ (Separation): Distinction of essence/accident
              - π (Staying): Faithfulness and perseverance
              
              Be precise, scholarly, and theologically sound.`
            },
            {
              role: 'user',
              content: `Analyze ${reference}: "${passage.textEn}"
              
              Provide:
              1. Brief theological summary (2-3 sentences)
              2. Key modal operators present (with justification)
              3. Primary theme
              4. Ethical implications`
            }
          ],
          temperature: 0.3, // Lower temperature for more deterministic output
          max_tokens: 500,
        });
        
        aiAnalysis = completion.choices[0]?.message?.content || null;
      } catch (aiError) {
        console.error('AI analysis failed:', aiError);
        // Continue without AI analysis
      }
    }

    // Generate proof hash
    const proofHash = modalEngine.generateProofHash(modalAnalysis, passageId);

    // Create card title
    const cardTitle = title || `Witness: ${reference}`;

    // Save to database (or return demo card)
    let savedCard;
    try {
      savedCard = await prisma.witnessCard.create({
        data: {
          passageId: passage.id,
          title: cardTitle,
          summary: modalAnalysis.reasoning,
          modalAnalysis: JSON.stringify(modalAnalysis),
          themes: JSON.stringify(modalAnalysis.themes),
          ethicsCheck: JSON.stringify(ethicsReport),
          proofHash,
          verified: ethicsReport.overallPassed,
        }
      });

      // Create ethics reviews
      for (const review of ethicsReport.reviews) {
        await prisma.ethicsReview.create({
          data: {
            witnessCardId: savedCard.id,
            principle: review.principle,
            passed: review.passed,
            score: review.score,
            reasoning: review.reasoning,
            concerns: JSON.stringify(review.concerns),
          }
        });
      }
    } catch {
      // Return demo card if database save fails
      savedCard = {
        id: `demo-card-${Date.now()}`,
        passageId: passage.id,
        title: cardTitle,
        summary: modalAnalysis.reasoning,
        modalAnalysis: JSON.stringify(modalAnalysis),
        themes: JSON.stringify(modalAnalysis.themes),
        ethicsCheck: JSON.stringify(ethicsReport),
        proofHash,
        verified: ethicsReport.overallPassed,
        createdAt: new Date(),
        updatedAt: new Date(),
      };
    }

    return NextResponse.json({
      card: savedCard,
      passage,
      modalAnalysis,
      ethicsReport,
      aiAnalysis,
    }, { status: 201 });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Validation failed', details: error.errors },
        { status: 400 }
      );
    }
    console.error('Error creating witness card:', error);
    return NextResponse.json(
      { error: 'Failed to create witness card' },
      { status: 500 }
    );
  }
}
