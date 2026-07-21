import { cn } from '../../lib/utils';
import type { ReactNode } from 'react';

interface BadgeProps {
  children: ReactNode;
  glow?: boolean;
  className?: string;
}

export function Badge({ children, glow = false, className }: BadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-semibold tracking-wide',
        'border border-white/10 bg-white/5 text-accent-blue',
        glow && 'shadow-[0_0_20px_rgba(59,130,246,0.15)]',
        className
      )}
    >
      {children}
    </span>
  );
}
