'use client';

import { memo } from 'react';

interface LogoProps {
  className?: string;
  size?: number;
}

function PureLogo({ className = '', size = 32 }: LogoProps) {
  return (
    <div
      className={`flex items-center justify-center shrink-0 ${className}`}
      style={{ width: size, height: size }}
    >
      <svg
        width={size}
        height={size}
        viewBox="0 0 32 32"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Outer circle - clean and simple */}
        <circle
          cx="16"
          cy="16"
          r="14"
          stroke="currentColor"
          strokeWidth="1.5"
          className="text-muted-foreground/40"
          fill="none"
        />

        {/* Compass directional arrows - minimalist */}
        <g stroke="currentColor" strokeWidth="2" strokeLinecap="round" className="text-foreground">
          {/* North arrow */}
          <line x1="16" y1="6" x2="16" y2="12" />
          <polyline points="16,6 14,8 18,8" fill="currentColor" />

          {/* South arrow */}
          <line x1="16" y1="26" x2="16" y2="20" />
          <polyline points="16,26 14,24 18,24" fill="currentColor" />

          {/* East arrow */}
          <line x1="26" y1="16" x2="20" y2="16" />
          <polyline points="26,16 24,14 24,18" fill="currentColor" />

          {/* West arrow */}
          <line x1="6" y1="16" x2="12" y2="16" />
          <polyline points="6,16 8,14 8,18" fill="currentColor" />
        </g>

        {/* Center point */}
        <circle
          cx="16"
          cy="16"
          r="1.5"
          fill="currentColor"
          className="text-foreground"
        />
      </svg>
    </div>
  );
}

export const Logo = memo(PureLogo);
