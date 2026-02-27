/**
 * Iota Verbum (IV) - PDF Export API
 * Generates professional PDF witness cards for download
 */

import { NextRequest, NextResponse } from 'next/server';
import { MODAL_SYMBOLS, MODAL_INTERPRETATIONS, ModalOperatorType } from '@/lib/modal-engine';
import { PRINCIPLE_DEFINITIONS, EthicsPrinciple } from '@/lib/ethics-engine';
import prisma from '@/lib/db';

interface PDFOptions {
  cardId: string;
  includeAIAnalysis?: boolean;
}

// Generate a simple HTML-based PDF content
function generatePDFHTML(data: {
  card: {
    id: string;
    title: string;
    summary: string;
    modalAnalysis: string;
    themes: string;
    ethicsCheck: string;
    proofHash: string;
    verified: boolean;
    createdAt: Date;
    passage?: {
      book: string;
      chapter: number;
      verseStart: number;
      textEn: string;
      textOriginal?: string | null;
      originalLanguage?: string | null;
    };
  };
  aiAnalysis?: string | null;
}): string {
  const { card, aiAnalysis } = data;
  
  // Parse JSON fields
  const modalAnalysis = typeof card.modalAnalysis === 'string' 
    ? JSON.parse(card.modalAnalysis) 
    : card.modalAnalysis;
  const themes = typeof card.themes === 'string' 
    ? JSON.parse(card.themes) 
    : card.themes;
  const ethicsCheck = typeof card.ethicsCheck === 'string' 
    ? JSON.parse(card.ethicsCheck) 
    : card.ethicsCheck;

  const reference = card.passage 
    ? `${card.passage.book} ${card.passage.chapter}:${card.passage.verseStart}`
    : 'Unknown Passage';

  const operators = modalAnalysis?.encodings?.map((e: { operatorType: ModalOperatorType }) => {
    const symbol = MODAL_SYMBOLS[e.operatorType];
    const interp = MODAL_INTERPRETATIONS[e.operatorType];
    return `<span style="margin-right: 8px; padding: 4px 12px; background: linear-gradient(135deg, #1a1f3c, #2a3050); color: white; border-radius: 20px; font-size: 12px;">
      <strong>${symbol}</strong> ${interp.divine}
    </span>`;
  }).join('') || '';

  const themesList = themes?.map((t: string) => 
    `<span style="margin: 2px 4px; padding: 2px 8px; background: #f0f0f0; border-radius: 12px; font-size: 11px;">${t}</span>`
  ).join('') || '';

  const ethicsItems = ethicsCheck?.reviews?.map((r: { principle: EthicsPrinciple; passed: boolean; score: number }) => {
    const def = PRINCIPLE_DEFINITIONS[r.principle];
    const statusColor = r.passed ? '#22c55e' : '#f59e0b';
    const statusText = r.passed ? '✓' : '⚠';
    return `<div style="display: flex; align-items: center; margin: 6px 0; padding: 8px; background: #fafafa; border-radius: 6px; border-left: 3px solid ${statusColor};">
      <span style="color: ${statusColor}; font-weight: bold; margin-right: 8px;">${statusText}</span>
      <span style="flex: 1; font-size: 12px;">${def.name}</span>
      <span style="font-size: 11px; color: #666;">${(r.score * 100).toFixed(0)}%</span>
    </div>`;
  }).join('') || '';

  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Witness Card - ${reference}</title>
  <style>
    @page {
      size: A4;
      margin: 20mm;
    }
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      color: #1a1a1a;
      line-height: 1.6;
      max-width: 800px;
      margin: 0 auto;
      padding: 20px;
    }
    .header {
      background: linear-gradient(135deg, #1a1f3c 0%, #2a3050 100%);
      color: white;
      padding: 30px;
      border-radius: 12px;
      margin-bottom: 24px;
    }
    .header h1 {
      margin: 0 0 8px 0;
      font-size: 24px;
    }
    .header .reference {
      font-size: 16px;
      opacity: 0.9;
    }
    .header .badges {
      margin-top: 16px;
    }
    .scripture {
      background: linear-gradient(to right, #fef3c7, #fef9c3);
      border-left: 4px solid #d97706;
      padding: 20px;
      margin: 24px 0;
      border-radius: 0 8px 8px 0;
      font-style: italic;
    }
    .scripture .original {
      font-size: 12px;
      color: #666;
      margin-top: 8px;
    }
    .section {
      margin: 24px 0;
    }
    .section-title {
      font-size: 14px;
      font-weight: 600;
      color: #1a1f3c;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 12px;
      padding-bottom: 8px;
      border-bottom: 2px solid #e5e7eb;
    }
    .operators {
      margin: 12px 0;
    }
    .themes {
      line-height: 2;
    }
    .ethics-box {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 16px;
    }
    .ethics-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }
    .summary {
      font-size: 14px;
      line-height: 1.7;
      color: #374151;
    }
    .ai-analysis {
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      border-radius: 8px;
      padding: 16px;
      font-size: 13px;
      line-height: 1.7;
    }
    .footer {
      margin-top: 40px;
      padding-top: 20px;
      border-top: 1px solid #e5e7eb;
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      color: #6b7280;
    }
    .hash {
      font-family: monospace;
      background: #f3f4f6;
      padding: 4px 8px;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="header">
    <h1>□◇ Iota Verbum</h1>
    <div class="reference">${reference}</div>
    <div class="badges">
      ${card.verified ? '<span style="background: #22c55e; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; margin-right: 8px;">✓ Verified</span>' : ''}
      <span style="background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 20px; font-size: 12px;">
        Ethics: ${ethicsCheck?.overallScore ? (ethicsCheck.overallScore * 100).toFixed(0) : 'N/A'}%
      </span>
    </div>
  </div>

  ${card.passage?.textEn ? `
  <div class="scripture">
    "${card.passage.textEn}"
    ${card.passage.textOriginal ? `<div class="original">${card.passage.textOriginal}</div>` : ''}
    ${card.passage.originalLanguage ? `<div class="original" style="font-weight: 500;">Original: ${card.passage.originalLanguage}</div>` : ''}
  </div>
  ` : ''}

  <div class="section">
    <div class="section-title">Modal Operators</div>
    <div class="operators">${operators}</div>
  </div>

  ${themes?.length > 0 ? `
  <div class="section">
    <div class="section-title">Themes</div>
    <div class="themes">${themesList}</div>
  </div>
  ` : ''}

  <div class="section">
    <div class="section-title">Analysis</div>
    <div class="summary">${card.summary}</div>
  </div>

  ${aiAnalysis ? `
  <div class="section">
    <div class="section-title">✨ AI Insight</div>
    <div class="ai-analysis">${aiAnalysis.replace(/\n/g, '<br>')}</div>
  </div>
  ` : ''}

  ${ethicsCheck ? `
  <div class="section">
    <div class="section-title">Ethics Review</div>
    <div class="ethics-box">
      <div class="ethics-header">
        <span>Overall Score: <strong>${(ethicsCheck.overallScore * 100).toFixed(1)}%</strong></span>
        <span style="padding: 4px 12px; border-radius: 20px; font-size: 12px; background: ${ethicsCheck.overallPassed ? '#dcfce7' : '#fef3c7'}; color: ${ethicsCheck.overallPassed ? '#166534' : '#92400e'};">
          ${ethicsCheck.recommendation}
        </span>
      </div>
      ${ethicsItems}
    </div>
  </div>
  ` : ''}

  <div class="footer">
    <div>
      <strong>Witness Card ID:</strong> ${card.id}<br>
      <strong>Generated:</strong> ${new Date(card.createdAt).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
    </div>
    <div style="text-align: right;">
      <strong>Proof Hash:</strong><br>
      <span class="hash">${card.proofHash}</span>
    </div>
  </div>
</body>
</html>
`;
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { cardId, includeAIAnalysis } = body as PDFOptions;

    if (!cardId) {
      return NextResponse.json({ error: 'Card ID is required' }, { status: 400 });
    }

    // Fetch the witness card
    const card = await prisma.witnessCard.findUnique({
      where: { id: cardId },
      include: {
        passage: true,
        ethicsReviews: true,
      }
    });

    if (!card) {
      return NextResponse.json({ error: 'Witness card not found' }, { status: 404 });
    }

    // Generate HTML for PDF
    const html = generatePDFHTML({
      card: {
        ...card,
        createdAt: card.createdAt,
        passage: card.passage ? {
          book: card.passage.book,
          chapter: card.passage.chapter,
          verseStart: card.passage.verseStart,
          textEn: card.passage.textEn,
          textOriginal: card.passage.textOriginal,
          originalLanguage: card.passage.originalLanguage,
        } : undefined,
      },
      aiAnalysis: includeAIAnalysis ? null : null,
    });

    // Return HTML with appropriate headers for download
    return new NextResponse(html, {
      headers: {
        'Content-Type': 'text/html',
        'Content-Disposition': `attachment; filename="witness-card-${cardId}.html"`,
      },
    });
  } catch (error) {
    console.error('PDF generation error:', error);
    return NextResponse.json(
      { error: 'Failed to generate PDF' },
      { status: 500 }
    );
  }
}
