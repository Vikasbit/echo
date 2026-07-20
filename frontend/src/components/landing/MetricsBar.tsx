import { useScrollReveal } from '../../hooks/useScrollReveal';
import { cn } from '../../lib/utils';

const CAPABILITIES = [
  { label: 'Document Types', value: 'PDF, DOCX, Scanned' },
  { label: 'AI Model', value: 'RAG Pipeline' },
  { label: 'Deployment', value: 'Cloud & On-Premise' },
  { label: 'Citations', value: 'Page-Level Sources' },
];

export function MetricsBar() {
  const { ref, isRevealed } = useScrollReveal({ threshold: 0.2 });

  return (
    <section className="relative z-20 section-wrapper -mt-8">
      <div
        ref={ref}
        className={cn('reveal', isRevealed && 'revealed')}
      >
        <div className="flex flex-wrap items-center justify-center gap-x-12 gap-y-4 py-8 border-t border-b border-white/[0.04]">
          {CAPABILITIES.map((cap) => (
            <div key={cap.label} className="flex items-center gap-3 text-sm">
              <span className="text-white/20 font-medium">{cap.label}</span>
              <span className="text-white/60 font-semibold">{cap.value}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
