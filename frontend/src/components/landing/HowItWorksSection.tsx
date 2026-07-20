import { SectionHeading } from '../ui/SectionHeading';
import { useScrollReveal } from '../../hooks/useScrollReveal';
import { cn } from '../../lib/utils';
import { Upload, Brain, GitBranch, MessageSquareText } from 'lucide-react';

const STEPS = [
  {
    icon: Upload,
    number: '01',
    title: 'Upload your documents',
    description: 'Drag and drop PDFs, DOCX, scanned manuals, SOPs, inspection reports. We handle the rest.',
    color: 'text-blue-400',
    borderColor: 'border-blue-500/20',
    dotColor: 'bg-blue-400',
  },
  {
    icon: Brain,
    number: '02',
    title: 'AI processes everything',
    description: 'OCR, text extraction, metadata classification, embedding generation. Each document is deeply understood.',
    color: 'text-violet-400',
    borderColor: 'border-violet-500/20',
    dotColor: 'bg-violet-400',
  },
  {
    icon: GitBranch,
    number: '03',
    title: 'Knowledge graph is built',
    description: 'Equipment, procedures, parts, and incidents are automatically linked into a searchable knowledge graph.',
    color: 'text-cyan-400',
    borderColor: 'border-cyan-500/20',
    dotColor: 'bg-cyan-400',
  },
  {
    icon: MessageSquareText,
    number: '04',
    title: 'Ask questions, get cited answers',
    description: 'Natural language queries return precise answers with source document and page number citations.',
    color: 'text-emerald-400',
    borderColor: 'border-emerald-500/20',
    dotColor: 'bg-emerald-400',
  },
];

export function HowItWorksSection() {
  return (
    <section id="how-it-works" className="py-28 md:py-36 relative">
      {/* Subtle background glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[400px] orb-purple rounded-full blur-3xl pointer-events-none opacity-40" />

      <div className="section-wrapper relative z-10">
        <SectionHeading
          overline="How it works"
          title="From raw documents to"
          titleHighlight="AI answers"
          subtitle="Four steps. Fully automated. No configuration required."
        />

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 lg:gap-4">
          {STEPS.map((step, i) => (
            <StepCard key={step.title} step={step} index={i} />
          ))}
        </div>
      </div>
    </section>
  );
}

function StepCard({
  step,
  index,
}: {
  step: (typeof STEPS)[0];
  index: number;
}) {
  const { ref, isRevealed } = useScrollReveal({ threshold: 0.15 });
  const Icon = step.icon;

  return (
    <div
      ref={ref}
      className={cn('reveal', isRevealed && 'revealed')}
      style={{ transitionDelay: `${index * 120}ms` }}
    >
      <div className="relative p-6 rounded-2xl bg-[rgba(12,17,30,0.5)] border border-white/[0.04] h-full">
        {/* Step number */}
        <div className="flex items-center gap-3 mb-5">
          <span className="text-[11px] font-mono font-bold text-white/15 tracking-widest">{step.number}</span>
          <div className={cn('w-1 h-1 rounded-full', step.dotColor)} />
        </div>

        <Icon className={cn('w-5 h-5 mb-4', step.color)} strokeWidth={1.5} />

        <h3 className="text-[15px] font-semibold text-white mb-2 tracking-tight">
          {step.title}
        </h3>
        <p className="text-[13px] text-white/30 leading-relaxed font-light">
          {step.description}
        </p>

        {/* Connecting arrow (not on last card) */}
        {index < 3 && (
          <div className="hidden lg:block absolute -right-3 top-1/2 -translate-y-1/2 text-white/10 z-20">
            <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
              <path d="M2 6h8M7 3l3 3-3 3" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </div>
        )}
      </div>
    </div>
  );
}
