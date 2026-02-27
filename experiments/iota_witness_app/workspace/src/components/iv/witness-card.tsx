'use client';

import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { OperatorBadge } from './operator-badge';
import { EthicsBadge } from './ethics-panel';
import { ModalGraph } from './modal-graph';
import { ModalOperatorType } from '@/lib/modal-engine';
import { cn } from '@/lib/utils';
import { BookOpen, Hash, Clock, Download, FileText, Share2, Sparkles } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { toast } from 'sonner';

interface WitnessCardData {
  id: string;
  title: string;
  summary: string;
  modalAnalysis: string;
  themes: string;
  ethicsCheck: string;
  proofHash: string;
  verified: boolean;
  createdAt: string;
  passage?: {
    book: string;
    chapter: number;
    verseStart: number;
    textEn: string;
    textOriginal?: string | null;
    originalLanguage?: string | null;
  };
  ethicsReviews?: Array<{
    principle: string;
    passed: boolean;
    score: number;
  }>;
}

interface WitnessCardProps {
  card: WitnessCardData;
  aiAnalysis?: string | null;
  showGraph?: boolean;
  className?: string;
}

export function WitnessCard({ card, aiAnalysis, showGraph = true, className }: WitnessCardProps) {
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

  // Export as JSON
  const exportJSON = () => {
    const dataStr = JSON.stringify({
      card,
      aiAnalysis,
      exportedAt: new Date().toISOString(),
    }, null, 2);
    
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `witness-card-${card.id}.json`;
    a.click();
    URL.revokeObjectURL(url);
    
    toast.success('Witness card exported as JSON!');
  };

  // Export as HTML (printable as PDF)
  const exportPDF = async () => {
    try {
      const response = await fetch('/api/export-pdf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          cardId: card.id,
          includeAIAnalysis: !!aiAnalysis,
        }),
      });

      if (!response.ok) throw new Error('Export failed');

      const html = await response.text();
      const blob = new Blob([html], { type: 'text/html' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `witness-card-${card.id}.html`;
      a.click();
      URL.revokeObjectURL(url);

      toast.success('Witness card exported! Open in browser and print to PDF.');
    } catch (error) {
      console.error('Export failed:', error);
      toast.error('Failed to export witness card');
    }
  };

  return (
    <Card className={cn('overflow-hidden border-2 hover:border-primary/50 transition-colors', className)}>
      {/* Header with gradient */}
      <div className="bg-gradient-to-r from-[#1a1f3c] to-[#2a3050] text-white">
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between">
            <div>
              <CardTitle className="text-xl font-bold text-white">{card.title}</CardTitle>
              <CardDescription className="text-white/70 flex items-center gap-2 mt-1">
                <BookOpen className="h-4 w-4" />
                {reference}
              </CardDescription>
            </div>
            <div className="flex flex-col items-end gap-2">
              {card.verified && (
                <Badge className="bg-green-500/20 text-green-300 border-green-500/30">
                  <Sparkles className="h-3 w-3 mr-1" />
                  Verified
                </Badge>
              )}
              {ethicsCheck?.overallScore && (
                <EthicsBadge passed={ethicsCheck.overallPassed} score={ethicsCheck.overallScore} />
              )}
            </div>
          </div>
        </CardHeader>
      </div>

      <CardContent className="pt-4 space-y-4">
        {/* Scripture Text */}
        {card.passage?.textEn && (
          <div className="p-4 bg-muted/30 rounded-lg border-l-4 border-amber-500">
            <p className="text-sm italic text-foreground/90 leading-relaxed">
              &ldquo;{card.passage.textEn}&rdquo;
            </p>
            {card.passage.textOriginal && (
              <p className="text-xs text-muted-foreground mt-2 font-serif">
                {card.passage.textOriginal}
              </p>
            )}
          </div>
        )}

        {/* Modal Operators */}
        {modalAnalysis?.encodings?.length > 0 && (
          <div className="space-y-2">
            <h4 className="text-sm font-semibold text-muted-foreground uppercase tracking-wide">
              Modal Operators
            </h4>
            <div className="flex flex-wrap gap-2">
              {modalAnalysis.encodings.map((encoding: { operatorType: ModalOperatorType; formula: string }, i: number) => (
                <OperatorBadge key={i} operator={encoding.operatorType} size="sm" />
              ))}
            </div>
          </div>
        )}

        {/* Modal Graph */}
        {showGraph && modalAnalysis?.encodings?.length > 0 && (
          <div className="border rounded-lg p-2 bg-muted/10">
            <ModalGraph encodings={modalAnalysis.encodings} />
          </div>
        )}

        {/* Themes */}
        {themes?.length > 0 && (
          <div className="space-y-2">
            <h4 className="text-sm font-semibold text-muted-foreground uppercase tracking-wide">
              Themes
            </h4>
            <div className="flex flex-wrap gap-1.5">
              {themes.map((theme: string, i: number) => (
                <Badge key={i} variant="outline" className="text-xs">
                  {theme}
                </Badge>
              ))}
            </div>
          </div>
        )}

        {/* Summary */}
        <div className="space-y-2">
          <h4 className="text-sm font-semibold text-muted-foreground uppercase tracking-wide">
            Analysis
          </h4>
          <p className="text-sm text-foreground/80 leading-relaxed">
            {card.summary}
          </p>
        </div>

        {/* AI Analysis */}
        {aiAnalysis && (
          <div className="space-y-2">
            <h4 className="text-sm font-semibold text-muted-foreground uppercase tracking-wide flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-amber-500" />
              AI Insight
            </h4>
            <div className="prose prose-sm dark:prose-invert max-w-none">
              <ReactMarkdown>{aiAnalysis}</ReactMarkdown>
            </div>
          </div>
        )}
      </CardContent>

      {/* Footer */}
      <CardFooter className="border-t bg-muted/20 flex items-center justify-between py-3">
        <div className="flex items-center gap-4 text-xs text-muted-foreground">
          <span className="flex items-center gap-1">
            <Hash className="h-3 w-3" />
            {card.proofHash.substring(0, 12)}...
          </span>
          <span className="flex items-center gap-1">
            <Clock className="h-3 w-3" />
            {new Date(card.createdAt).toLocaleDateString()}
          </span>
        </div>
        <div className="flex gap-2">
          <Button variant="ghost" size="sm" className="h-8 px-2" onClick={exportPDF} title="Export as HTML/PDF">
            <FileText className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="sm" className="h-8 px-2" onClick={exportJSON} title="Export as JSON">
            <Download className="h-4 w-4" />
          </Button>
        </div>
      </CardFooter>
    </Card>
  );
}

// Compact card for lists
interface WitnessCardCompactProps {
  card: WitnessCardData;
  onClick?: () => void;
  className?: string;
}

export function WitnessCardCompact({ card, onClick, className }: WitnessCardCompactProps) {
  const modalAnalysis = typeof card.modalAnalysis === 'string' 
    ? JSON.parse(card.modalAnalysis) 
    : card.modalAnalysis;
  const themes = typeof card.themes === 'string' 
    ? JSON.parse(card.themes) 
    : card.themes;

  const reference = card.passage 
    ? `${card.passage.book} ${card.passage.chapter}:${card.passage.verseStart}`
    : 'Unknown';

  return (
    <div 
      className={cn(
        'p-4 rounded-lg border bg-card hover:border-primary/50 cursor-pointer transition-all',
        className
      )}
      onClick={onClick}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <h4 className="font-medium text-sm truncate">{card.title}</h4>
          <p className="text-xs text-muted-foreground mt-0.5">{reference}</p>
        </div>
        <div className="flex items-center gap-1.5">
          {modalAnalysis?.encodings?.slice(0, 3).map((e: { operatorType: ModalOperatorType }, i: number) => (
            <OperatorBadgeSmall key={i} operator={e.operatorType} />
          ))}
        </div>
      </div>
      {themes?.length > 0 && (
        <div className="flex flex-wrap gap-1 mt-2">
          {themes.slice(0, 3).map((theme: string, i: number) => (
            <Badge key={i} variant="secondary" className="text-xs">
              {theme}
            </Badge>
          ))}
        </div>
      )}
    </div>
  );
}

// Operator badge small for compact view
function OperatorBadgeSmall({ operator }: { operator: ModalOperatorType }) {
  const symbols: Record<ModalOperatorType, string> = {
    NECESSITY: '□',
    POSSIBILITY: '◇',
    WITNESS: 'W',
    SEPARATION: 'σ',
    STAYING: 'π',
  };

  const gradients: Record<ModalOperatorType, string> = {
    NECESSITY: 'from-amber-500 to-yellow-600',
    POSSIBILITY: 'from-blue-400 to-indigo-500',
    WITNESS: 'from-purple-500 to-violet-600',
    SEPARATION: 'from-emerald-500 to-teal-600',
    STAYING: 'from-red-500 to-rose-600',
  };

  return (
    <span 
      className={cn(
        'inline-flex items-center justify-center w-7 h-7 rounded-full bg-gradient-to-r text-white font-bold text-sm shadow-sm',
        gradients[operator]
      )}
      title={operator}
    >
      {symbols[operator]}
    </span>
  );
}
