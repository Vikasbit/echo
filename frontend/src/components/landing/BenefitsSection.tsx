import { SectionHeading } from '../ui/SectionHeading';
import { useScrollReveal } from '../../hooks/useScrollReveal';
import { cn } from '../../lib/utils';
import { Clock, Shield, Wrench, Zap, Lock } from 'lucide-react';

const BENEFITS = [
  {
    icon: Clock,
    title: 'Find information in seconds, not hours',
    description: 'Engineers spend 30% of their time searching for information. Semantic search delivers answers immediately.',
  },
  {
    icon: Shield,
    title: 'Capture institutional knowledge',
    description: 'When experienced engineers leave, their knowledge stays. Every document becomes part of a permanent, searchable AI memory.',
  },
  {
    icon: Wrench,
    title: 'Verified procedures, every time',
    description: 'No more guessing. Every answer cites the exact source document and page number so you can verify before acting.',
  },
  {
    icon: Zap,
    title: 'Operational intelligence',
    description: 'The knowledge graph surfaces connections you might miss — related incidents, relevant SOPs, equipment relationships.',
  },
  {
    icon: Lock,
    title: 'Your data stays yours',
    description: 'Deploy on-premise for zero external data sharing. Air-gapped mode available for classified environments.',
  },
];

export function BenefitsSection() {
  return (
    <section id="benefits" className="py-28 md:py-36 relative">
      <div className="section-wrapper relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-12 lg:gap-16">
          {/* Left — heading */}
          <div className="lg:col-span-2">
            <SectionHeading
              overline="Why Echo"
              title="Built for how engineers"
              titleHighlight="actually work"
              align="left"
              className="mb-0 lg:sticky lg:top-32"
            />
          </div>

          {/* Right — benefit items */}
          <div className="lg:col-span-3 space-y-1">
            {BENEFITS.map((benefit, i) => (
              <BenefitItem key={benefit.title} benefit={benefit} index={i} />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

function BenefitItem({
  benefit,
  index,
}: {
  benefit: (typeof BENEFITS)[0];
  index: number;
}) {
  const { ref, isRevealed } = useScrollReveal({ threshold: 0.2 });
  const Icon = benefit.icon;

  return (
    <div
      ref={ref}
      className={cn(
        'reveal group flex items-start gap-5 p-5 rounded-xl transition-colors duration-200 hover:bg-white/[0.02]',
        isRevealed && 'revealed'
      )}
      style={{ transitionDelay: `${index * 80}ms` }}
    >
      <div className="w-9 h-9 rounded-lg bg-white/[0.04] border border-white/[0.06] flex items-center justify-center flex-shrink-0 mt-0.5 group-hover:bg-white/[0.06] transition-colors">
        <Icon className="w-4 h-4 text-white/30 group-hover:text-white/50 transition-colors" strokeWidth={1.5} />
      </div>
      <div>
        <h3 className="text-[15px] font-semibold text-white/80 mb-1.5 tracking-tight">{benefit.title}</h3>
        <p className="text-[13px] text-white/30 leading-relaxed font-light">{benefit.description}</p>
      </div>
    </div>
  );
}
