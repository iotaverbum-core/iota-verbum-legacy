'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { EthicsReview, EthicsPrinciple, PRINCIPLE_DEFINITIONS, getPrincipleGradient } from '@/lib/ethics-engine';
import { cn } from '@/lib/utils';
import { Check, AlertTriangle, X, Shield } from 'lucide-react';

interface EthicsPanelProps {
  reviews: EthicsReview[];
  overallScore: number;
  recommendation: 'APPROVED' | 'NEEDS_REVIEW' | 'REJECTED';
  className?: string;
}

export function EthicsPanel({ reviews, overallScore, recommendation, className }: EthicsPanelProps) {
  const getRecommendationIcon = () => {
    switch (recommendation) {
      case 'APPROVED':
        return <Check className="h-5 w-5 text-green-500" />;
      case 'NEEDS_REVIEW':
        return <AlertTriangle className="h-5 w-5 text-amber-500" />;
      case 'REJECTED':
        return <X className="h-5 w-5 text-red-500" />;
    }
  };

  const getRecommendationColor = () => {
    switch (recommendation) {
      case 'APPROVED':
        return 'text-green-600 bg-green-50 border-green-200';
      case 'NEEDS_REVIEW':
        return 'text-amber-600 bg-amber-50 border-amber-200';
      case 'REJECTED':
        return 'text-red-600 bg-red-50 border-red-200';
    }
  };

  return (
    <Card className={cn('overflow-hidden', className)}>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2 text-lg">
            <Shield className="h-5 w-5 text-primary" />
            Ethics Review
          </CardTitle>
          <div className={cn(
            'flex items-center gap-2 px-3 py-1 rounded-full border',
            getRecommendationColor()
          )}>
            {getRecommendationIcon()}
            <span className="text-sm font-medium">{recommendation}</span>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Overall Score */}
        <div className="flex items-center gap-4">
          <div className="flex-1">
            <div className="flex justify-between text-sm mb-1">
              <span className="text-muted-foreground">Overall Score</span>
              <span className="font-medium">{(overallScore * 100).toFixed(1)}%</span>
            </div>
            <Progress value={overallScore * 100} className="h-2" />
          </div>
        </div>

        {/* Principle Reviews */}
        <div className="space-y-3">
          {reviews.map((review) => (
            <EthicsReviewItem key={review.principle} review={review} />
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

interface EthicsReviewItemProps {
  review: EthicsReview;
}

function EthicsReviewItem({ review }: EthicsReviewItemProps) {
  const definition = PRINCIPLE_DEFINITIONS[review.principle];
  const gradient = getPrincipleGradient(review.principle);

  return (
    <div className="flex items-start gap-3 p-3 rounded-lg bg-muted/30">
      <div className={cn(
        'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-white bg-gradient-to-r',
        gradient
      )}>
        {review.passed ? (
          <Check className="h-4 w-4" />
        ) : (
          <AlertTriangle className="h-4 w-4" />
        )}
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between gap-2">
          <h4 className="text-sm font-medium">{definition.name}</h4>
          <Badge variant={review.passed ? 'default' : 'secondary'} className="text-xs">
            {(review.score * 100).toFixed(0)}%
          </Badge>
        </div>
        <p className="text-xs text-muted-foreground mt-1 line-clamp-2">
          {review.reasoning}
        </p>
        {review.concerns.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-1">
            {review.concerns.slice(0, 2).map((concern, i) => (
              <Badge key={i} variant="outline" className="text-xs text-amber-600 border-amber-200">
                {concern.substring(0, 30)}...
              </Badge>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

// Compact version for cards
interface EthicsBadgeProps {
  passed: boolean;
  score: number;
  className?: string;
}

export function EthicsBadge({ passed, score, className }: EthicsBadgeProps) {
  return (
    <div className={cn(
      'flex items-center gap-1.5 px-2 py-1 rounded-full text-xs font-medium',
      passed 
        ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' 
        : 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400',
      className
    )}>
      {passed ? (
        <Check className="h-3 w-3" />
      ) : (
        <AlertTriangle className="h-3 w-3" />
      )}
      <span>Ethics: {(score * 100).toFixed(0)}%</span>
    </div>
  );
}
