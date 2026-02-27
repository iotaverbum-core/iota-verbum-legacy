'use client';

import { useMemo } from 'react';
import { ModalOperatorType, MODAL_SYMBOLS, getOperatorColor } from '@/lib/modal-engine';

interface GraphNode {
  id: string;
  label: string;
  operator: ModalOperatorType;
  x: number;
  y: number;
}

interface GraphEdge {
  source: string;
  target: string;
  label: string;
  type: 'inference' | 'witness' | 'separation';
}

interface ModalGraphProps {
  encodings: Array<{
    operatorType: ModalOperatorType;
    formula: string;
    interpretation: string;
  }>;
  className?: string;
}

const nodeRadius = 35;
const svgWidth = 600;
const svgHeight = 350;

export function ModalGraph({ encodings, className }: ModalGraphProps) {
  const { nodes, edges } = useMemo(() => {
    if (!encodings || encodings.length === 0) {
      return { nodes: [], edges: [] };
    }

    const uniqueOperators = [...new Set(encodings.map(e => e.operatorType))];
    const centerX = svgWidth / 2;
    const centerY = svgHeight / 2;
    const radius = 110;

    // Create nodes in a circular layout
    const nodes: GraphNode[] = uniqueOperators.map((op, index) => {
      const angle = (2 * Math.PI * index) / uniqueOperators.length - Math.PI / 2;
      return {
        id: op,
        label: MODAL_SYMBOLS[op],
        operator: op,
        x: centerX + radius * Math.cos(angle),
        y: centerY + radius * Math.sin(angle),
      };
    });

    // Create edges based on inference rules
    const edges: GraphEdge[] = [];
    
    // Witness Formation: Necessity + Possibility → Witness
    if (uniqueOperators.includes('NECESSITY') && uniqueOperators.includes('POSSIBILITY')) {
      edges.push({
        source: 'NECESSITY',
        target: 'POSSIBILITY',
        label: 'W',
        type: 'witness',
      });
      if (!uniqueOperators.includes('WITNESS')) {
        nodes.push({
          id: 'WITNESS',
          label: 'W',
          operator: 'WITNESS',
          x: centerX,
          y: centerY,
        });
      }
    }

    // Separation from Witness
    if (uniqueOperators.includes('WITNESS')) {
      edges.push({
        source: 'WITNESS',
        target: 'SEPARATION',
        label: 'σ',
        type: 'separation',
      });
    }

    // Staying from Necessity
    if (uniqueOperators.includes('NECESSITY')) {
      edges.push({
        source: 'NECESSITY',
        target: 'STAYING',
        label: 'π',
        type: 'inference',
      });
    }

    return { nodes, edges };
  }, [encodings]);

  if (nodes.length === 0) {
    return (
      <div className={`flex items-center justify-center h-[350px] bg-muted/30 rounded-lg ${className}`}>
        <p className="text-muted-foreground text-sm">No modal operators to visualize</p>
      </div>
    );
  }

  return (
    <div className={className}>
      <svg 
        viewBox={`0 0 ${svgWidth} ${svgHeight}`} 
        className="w-full h-auto"
        style={{ maxHeight: svgHeight }}
      >
        {/* Background gradient */}
        <defs>
          <radialGradient id="bgGradient" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#1a1f3c" stopOpacity="0.05" />
            <stop offset="100%" stopColor="#1a1f3c" stopOpacity="0" />
          </radialGradient>
          <filter id="glow">
            <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
            <feMerge>
              <feMergeNode in="coloredBlur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>

        {/* Background */}
        <rect width={svgWidth} height={svgHeight} fill="url(#bgGradient)" />

        {/* Edges */}
        {edges.map((edge, index) => {
          const sourceNode = nodes.find(n => n.id === edge.source);
          const targetNode = nodes.find(n => n.id === edge.target);
          if (!sourceNode || !targetNode) return null;

          return (
            <g key={`edge-${index}`}>
              <line
                x1={sourceNode.x}
                y1={sourceNode.y}
                x2={targetNode.x}
                y2={targetNode.y}
                stroke="#c9a227"
                strokeWidth="2"
                strokeDasharray={edge.type === 'inference' ? '5,5' : 'none'}
                opacity="0.6"
              />
              <text
                x={(sourceNode.x + targetNode.x) / 2}
                y={(sourceNode.y + targetNode.y) / 2 - 8}
                textAnchor="middle"
                className="fill-amber-600 text-xs font-medium"
              >
                {edge.label}
              </text>
            </g>
          );
        })}

        {/* Nodes */}
        {nodes.map((node) => {
          const color = getOperatorColor(node.operator);
          return (
            <g key={node.id} filter="url(#glow)">
              {/* Outer ring */}
              <circle
                cx={node.x}
                cy={node.y}
                r={nodeRadius + 4}
                fill="none"
                stroke={color}
                strokeWidth="2"
                opacity="0.3"
              />
              {/* Main circle */}
              <circle
                cx={node.x}
                cy={node.y}
                r={nodeRadius}
                fill={color}
                opacity="0.9"
              />
              {/* Symbol */}
              <text
                x={node.x}
                y={node.y}
                textAnchor="middle"
                dominantBaseline="central"
                className="fill-white text-2xl font-bold"
                style={{ fontSize: '24px' }}
              >
                {node.label}
              </text>
              {/* Label below */}
              <text
                x={node.x}
                y={node.y + nodeRadius + 18}
                textAnchor="middle"
                className="fill-foreground text-xs font-medium"
              >
                {node.id.charAt(0) + node.id.slice(1).toLowerCase().replace('_', ' ')}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}
