import { cn } from '../../lib/utils';
import { useScrollReveal } from '../../hooks/useScrollReveal';

interface SectionHeadingProps {
  overline?: string;
  title: string;
  titleHighlight?: string;
  subtitle?: string;
  align?: 'center' | 'left';
  className?: string;
}

export function SectionHeading({
  overline,
  title,
  titleHighlight,
  subtitle,
  align = 'center',
  className,
}: SectionHeadingProps) {
  const { ref, isRevealed } = useScrollReveal();

  return (
    <div
      ref={ref}
      className={cn(
        'reveal mb-14',
        isRevealed && 'revealed',
        align === 'center' && 'text-center',
        className
      )}
    >
      {overline && (
        <p className="text-[11px] font-medium uppercase text-white/20 tracking-[0.15em] mb-4">
          {overline}
        </p>
      )}
      <h2 className="text-display-lg text-white/90 font-bold tracking-tight leading-[1.1]">
        {title}
        {titleHighlight && (
          <span className="text-gradient"> {titleHighlight}</span>
        )}
      </h2>
      {subtitle && (
        <p className="mt-4 text-base text-white/30 max-w-lg mx-auto font-light leading-relaxed">
          {subtitle}
        </p>
      )}
    </div>
  );
}
