import { SectionHeading } from '../ui/SectionHeading';
import { useScrollReveal } from '../../hooks/useScrollReveal';
import { cn } from '../../lib/utils';

const USE_CASES = [
  {
    industry: 'Manufacturing',
    problem: 'Engineers waste hours searching paper manuals for machine troubleshooting steps during production stoppages.',
    solution: 'Upload all equipment manuals. Ask "How to clear fault code E-304 on CNC machine" and get step-by-step instructions with page references.',
  },
  {
    industry: 'Energy & Utilities',
    problem: 'Safety procedures are scattered across hundreds of documents. Finding the right SOP during an incident takes too long.',
    solution: 'Centralize all SOPs and safety docs. Instant search surfaces the exact procedure, plus related incident reports from similar past events.',
  },
  {
    industry: 'Oil & Gas',
    problem: 'Maintenance teams on offshore platforms have limited connectivity and can\'t access cloud-based systems.',
    solution: 'Deploy Echo on-premise in fully air-gapped mode. All AI processing runs locally with zero internet dependency.',
  },
];

export function TestimonialsSection() {
  return (
    <section id="use-cases" className="py-28 md:py-36 relative">
      <div className="section-wrapper relative z-10">
        <SectionHeading
          overline="Use cases"
          title="How teams use"
          titleHighlight="Echo"
          subtitle="Real problems, practical solutions."
        />

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {USE_CASES.map((uc, i) => (
            <UseCaseCard key={uc.industry} useCase={uc} index={i} />
          ))}
        </div>
      </div>
    </section>
  );
}

function UseCaseCard({
  useCase,
  index,
}: {
  useCase: (typeof USE_CASES)[0];
  index: number;
}) {
  const { ref, isRevealed } = useScrollReveal({ threshold: 0.1 });

  return (
    <div
      ref={ref}
      className={cn('reveal', isRevealed && 'revealed')}
      style={{ transitionDelay: `${index * 100}ms` }}
    >
      <div className="rounded-2xl p-6 md:p-7 h-full border border-white/[0.04] bg-[rgba(12,17,30,0.5)] flex flex-col">
        {/* Industry tag */}
        <span className="text-[11px] font-semibold text-blue-400/60 uppercase tracking-wider mb-5">
          {useCase.industry}
        </span>

        {/* Problem */}
        <div className="mb-5">
          <span className="text-[11px] text-white/15 font-mono uppercase tracking-widest">Problem</span>
          <p className="mt-2 text-[13px] text-white/40 leading-relaxed font-light">
            {useCase.problem}
          </p>
        </div>

        {/* Divider */}
        <div className="w-8 h-px bg-white/[0.06] mb-5" />

        {/* Solution */}
        <div className="flex-1">
          <span className="text-[11px] text-emerald-400/40 font-mono uppercase tracking-widest">Solution</span>
          <p className="mt-2 text-[13px] text-white/55 leading-relaxed font-light">
            {useCase.solution}
          </p>
        </div>
      </div>
    </div>
  );
}
