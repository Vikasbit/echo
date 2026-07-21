import { cn } from '../../lib/utils';
import type { ReactNode, ButtonHTMLAttributes } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  children: ReactNode;
  icon?: ReactNode;
  iconRight?: ReactNode;
}

export function Button({
  variant = 'primary',
  size = 'md',
  children,
  icon,
  iconRight,
  className,
  ...props
}: ButtonProps) {
  const baseStyles = 'inline-flex items-center justify-center gap-2 font-semibold rounded-xl transition-all duration-200 active:scale-[0.98] disabled:opacity-50 disabled:pointer-events-none';

  const variants = {
    primary: 'bg-primary text-white hover:shadow-[0_0_30px_rgba(59,130,246,0.3)] hover:scale-[1.02]',
    secondary: 'bg-transparent text-white border border-white/10 hover:bg-white/5 hover:border-white/20 hover:scale-[1.02]',
    ghost: 'text-white/70 hover:text-white hover:bg-white/5',
  };

  const sizes = {
    sm: 'px-4 py-2 text-xs',
    md: 'px-6 py-3 text-sm',
    lg: 'px-8 py-4 text-base',
  };

  return (
    <button
      className={cn(baseStyles, variants[variant], sizes[size], className)}
      {...props}
    >
      {icon && <span className="flex-shrink-0">{icon}</span>}
      {children}
      {iconRight && <span className="flex-shrink-0">{iconRight}</span>}
    </button>
  );
}
