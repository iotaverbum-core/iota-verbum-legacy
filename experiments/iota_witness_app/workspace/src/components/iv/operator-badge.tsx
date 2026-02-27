'use client';

import { Badge } from '@/components/ui/badge';
import { MODAL_SYMBOLS, MODAL_INTERPRETATIONS, ModalOperatorType, getOperatorGradient } from '@/lib/modal-engine';
import { cn } from '@/lib/utils';

interface OperatorBadgeProps {
  operator: ModalOperatorType;
  showLabel?: boolean;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

const sizeClasses = {
  sm: 'text-xs px-2 py-0.5',
  md: 'text-sm px-3 py-1',
  lg: 'text-base px-4 py-1.5',
};

const symbolSizeClasses = {
  sm: 'text-sm',
  md: 'text-lg',
  lg: 'text-xl',
};

export function OperatorBadge({ 
  operator, 
  showLabel = true, 
  size = 'md',
  className 
}: OperatorBadgeProps) {
  const symbol = MODAL_SYMBOLS[operator];
  const interpretation = MODAL_INTERPRETATIONS[operator];
  const gradient = getOperatorGradient(operator);

  return (
    <Badge 
      className={cn(
        'bg-gradient-to-r text-white font-medium shadow-sm',
        gradient,
        sizeClasses[size],
        className
      )}
    >
      <span className={cn('mr-1.5', symbolSizeClasses[size])}>{symbol}</span>
      {showLabel && <span>{interpretation.divine}</span>}
    </Badge>
  );
}

interface OperatorBadgeSmallProps {
  operator: ModalOperatorType;
  className?: string;
}

export function OperatorBadgeSmall({ operator, className }: OperatorBadgeSmallProps) {
  const symbol = MODAL_SYMBOLS[operator];
  const gradient = getOperatorGradient(operator);

  return (
    <span 
      className={cn(
        'inline-flex items-center justify-center w-7 h-7 rounded-full bg-gradient-to-r text-white font-bold text-sm shadow-sm',
        gradient,
        className
      )}
      title={MODAL_INTERPRETATIONS[operator].description}
    >
      {symbol}
    </span>
  );
}

interface OperatorLegendProps {
  className?: string;
}

export function OperatorLegend({ className }: OperatorLegendProps) {
  const operators = Object.keys(MODAL_SYMBOLS) as ModalOperatorType[];

  return (
    <div className={cn('flex flex-wrap gap-2', className)}>
      {operators.map((op) => (
        <div key={op} className="flex items-center gap-2">
          <OperatorBadgeSmall operator={op} />
          <span className="text-sm text-muted-foreground">
            {MODAL_INTERPRETATIONS[op].human}
          </span>
        </div>
      ))}
    </div>
  );
}
