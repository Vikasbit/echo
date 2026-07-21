import { cn } from '../../lib/utils';
import type { ReactNode, HTMLAttributes } from 'react';

interface GlassCardProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode;
  glow?: 'blue' | 'purple' | 'cyan' | 'none';
  hover?: boolean;
  solid?: boolean;
}

export function GlassCard({
  children,
  glow = 'none',
  hover = false,
  solid = false,
  className,
  ...props
}: GlassCardProps) {
  const glowMap = {
    blue: 'hover:shadow-[0_0_40px_rgba(59,130,246,0.12)]',
    purple: 'hover:shadow-[0_0_40px_rgba(139,92,246,0.12)]',
    cyan: 'hover:shadow-[0_0_40px_rgba(6,182,212,0.12)]',
    none: '',
  };

  return (
    <div
      className={cn(
        solid ? 'glass-card-solid' : 'glass-card',
        hover && 'transition-all duration-300 hover:-translate-y-1 hover:border-white/15',
        glow !== 'none' && glowMap[glow],
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}
