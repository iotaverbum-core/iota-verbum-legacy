/**
 * Iota Verbum (IV) - Bible API Routes
 * Scripture passage management and retrieval
 */

import { NextRequest, NextResponse } from 'next/server';
import prisma from '@/lib/db';
import { z } from 'zod';

// Validation schema for creating passages
const CreatePassageSchema = z.object({
  book: z.string().min(1),
  chapter: z.number().int().positive(),
  verseStart: z.number().int().positive(),
  verseEnd: z.number().int().positive().optional(),
  textEn: z.string().min(1),
  textOriginal: z.string().optional(),
  originalLanguage: z.enum(['Greek', 'Hebrew', 'Aramaic']).optional().nullable(),
  translation: z.string().default('ESV'),
});

// GET - List all passages with optional filtering
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const book = searchParams.get('book');
    const chapter = searchParams.get('chapter');
    const limit = parseInt(searchParams.get('limit') || '50');
    const offset = parseInt(searchParams.get('offset') || '0');

    const where: Record<string, unknown> = {};
    if (book) where.book = book;
    if (chapter) where.chapter = parseInt(chapter);

    const passages = await prisma.scripturePassage.findMany({
      where,
      orderBy: [
        { book: 'asc' },
        { chapter: 'asc' },
        { verseStart: 'asc' },
      ],
      take: limit,
      skip: offset,
      include: {
        _count: {
          select: { witnessCards: true, modalEncodings: true }
        }
      }
    });

    const total = await prisma.scripturePassage.count({ where });

    return NextResponse.json({
      passages,
      pagination: {
        total,
        limit,
        offset,
        hasMore: offset + passages.length < total
      }
    });
  } catch (error) {
    console.error('Error fetching passages:', error);
    return NextResponse.json(
      { error: 'Failed to fetch passages' },
      { status: 500 }
    );
  }
}

// POST - Create a new passage
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const validated = CreatePassageSchema.parse(body);

    // Check for existing passage
    const existing = await prisma.scripturePassage.findFirst({
      where: {
        book: validated.book,
        chapter: validated.chapter,
        verseStart: validated.verseStart,
      }
    });

    if (existing) {
      return NextResponse.json(
        { error: 'Passage already exists', passage: existing },
        { status: 409 }
      );
    }

    const passage = await prisma.scripturePassage.create({
      data: validated
    });

    return NextResponse.json({ passage }, { status: 201 });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Validation failed', details: error.errors },
        { status: 400 }
      );
    }
    console.error('Error creating passage:', error);
    return NextResponse.json(
      { error: 'Failed to create passage' },
      { status: 500 }
    );
  }
}
