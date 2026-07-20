import { useScrollReveal } from '../../hooks/useScrollReveal';
import { useAnimatedCounter } from '../../hooks/useAnimatedCounter';

interface AnimatedCounterProps {
  end: number;
  suffix?: string;
  prefix?: string;
  decimals?: number;
  duration?: number;
  label: string;
  icon?: React.ReactNode;
}

export function AnimatedCounter({
  end,
  suffix = '',
  prefix = '',
  decimals = 0,
  duration = 2000,
  label,
  icon,
}: AnimatedCounterProps) {
  const { ref, isRevealed } = useScrollReveal({ threshold: 0.2 });
  const { formatted } = useAnimatedCounter(isRevealed, {
    end,
    suffix,
    prefix,
    decimals,
    duration,
  });

  return (
    <div ref={ref} className="flex flex-col items-center gap-2 text-center">
      {icon && (
        <div className="w-10 h-10 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center mb-1">
          {icon}
        </div>
      )}
      <span className="text-3xl md:text-4xl font-bold text-white tracking-tight">
        {formatted}
      </span>
      <span className="text-xs text-white/40 font-medium tracking-wide uppercase">
        {label}
      </span>
    </div>
  );
}
