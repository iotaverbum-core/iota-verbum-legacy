/**
 * Iota Verbum (IV) - Bible Passage by ID
 */

import { NextRequest, NextResponse } from 'next/server';
import prisma from '@/lib/db';
import { z } from 'zod';

const UpdatePassageSchema = z.object({
  textEn: z.string().min(1).optional(),
  textOriginal: z.string().optional().nullable(),
  originalLanguage: z.enum(['Greek', 'Hebrew', 'Aramaic']).optional().nullable(),
  translation: z.string().optional(),
});

// GET - Fetch a specific passage
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;

    const passage = await prisma.scripturePassage.findUnique({
      where: { id },
      include: {
        modalEncodings: {
          orderBy: { createdAt: 'desc' }
        },
        witnessCards: {
          orderBy: { createdAt: 'desc' },
          take: 5,
        }
      }
    });

    if (!passage) {
      return NextResponse.json(
        { error: 'Passage not found' },
        { status: 404 }
      );
    }

    return NextResponse.json({ passage });
  } catch (error) {
    console.error('Error fetching passage:', error);
    return NextResponse.json(
      { error: 'Failed to fetch passage' },
      { status: 500 }
    );
  }
}

// PUT - Update a passage
export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const body = await request.json();
    const validated = UpdatePassageSchema.parse(body);

    const passage = await prisma.scripturePassage.update({
      where: { id },
      data: validated
    });

    return NextResponse.json({ passage });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Validation failed', details: error.errors },
        { status: 400 }
      );
    }
    console.error('Error updating passage:', error);
    return NextResponse.json(
      { error: 'Failed to update passage' },
      { status: 500 }
    );
  }
}

// DELETE - Remove a passage
export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;

    await prisma.scripturePassage.delete({
      where: { id }
    });

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Error deleting passage:', error);
    return NextResponse.json(
      { error: 'Failed to delete passage' },
      { status: 500 }
    );
  }
}
