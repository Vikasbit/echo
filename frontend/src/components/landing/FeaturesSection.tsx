import { SectionHeading } from '../ui/SectionHeading';
import { useScrollReveal } from '../../hooks/useScrollReveal';
import { cn } from '../../lib/utils';
import {
  FileSearch2,
  Search,
  GitBranch,
  Cpu,
  MessageSquareText,
  Lightbulb,
} from 'lucide-react';

const FEATURES = [
  {
    icon: FileSearch2,
    title: 'Document Understanding',
    description:
      'Upload PDFs and DOCX files. The AI reads every page, extracts structured metadata, identifies equipment references, safety warnings, and procedures.',
    color: 'text-blue-400',
    gradient: 'from-blue-500/10 to-blue-500/0',
    borderColor: 'rgba(59, 130, 246, 0.2)',
  },
  {
    icon: Search,
    title: 'Semantic Search',
    description:
      'Search by meaning, not keywords. Ask "how to replace the hydraulic pump seal" and find relevant procedures across your entire document library.',
    color: 'text-violet-400',
    gradient: 'from-violet-500/10 to-violet-500/0',
    borderColor: 'rgba(139, 92, 246, 0.2)',
  },
  {
    icon: GitBranch,
    title: 'Knowledge Graph',
    description:
      'Automatically maps relationships between equipment, procedures, parts, and incidents. See how everything connects across your plant.',
    color: 'text-cyan-400',
    gradient: 'from-cyan-500/10 to-cyan-500/0',
    borderColor: 'rgba(6, 182, 212, 0.2)',
  },
  {
    icon: Cpu,
    title: 'Equipment Profiles',
    description:
      'Each piece of equipment gets an AI-generated profile — linked manuals, maintenance history, known issues, and recommended procedures.',
    color: 'text-emerald-400',
    gradient: 'from-emerald-500/10 to-emerald-500/0',
    borderColor: 'rgba(52, 211, 153, 0.2)',
  },
  {
    icon: MessageSquareText,
    title: 'AI Chat with Citations',
    description:
      'Ask questions in plain language. Get detailed answers with exact source document names and page numbers so you can always verify.',
    color: 'text-amber-400',
    gradient: 'from-amber-500/10 to-amber-500/0',
    borderColor: 'rgba(251, 191, 36, 0.2)',
  },
  {
    icon: Lightbulb,
    title: 'Smart Recommendations',
    description:
      'The AI surfaces relevant procedures, related incidents, and maintenance tips based on the context of your current query.',
    color: 'text-rose-400',
    gradient: 'from-rose-500/10 to-rose-500/0',
    borderColor: 'rgba(251, 113, 133, 0.2)',
  },
];

export function FeaturesSection() {
  return (
    <section id="features" className="py-28 md:py-36 relative">
      <div className="section-wrapper relative z-10">
        <SectionHeading
          overline="Capabilities"
          title="Built for industrial"
          titleHighlight="complexity"
          subtitle="Every feature designed to reduce the time engineers spend searching for information."
        />

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {FEATURES.map((feature, i) => (
            <FeatureCard key={feature.title} feature={feature} index={i} />
          ))}
        </div>
      </div>
    </section>
  );
}

function FeatureCard({
  feature,
  index,
}: {
  feature: (typeof FEATURES)[0];
  index: number;
}) {
  const { ref, isRevealed } = useScrollReveal({ threshold: 0.1 });
  const Icon = feature.icon;

  return (
    <div
      ref={ref}
      className={cn('reveal', isRevealed && 'revealed')}
      style={{ transitionDelay: `${index * 80}ms` }}
    >
      <div
        className="group relative rounded-2xl p-6 md:p-7 h-full transition-all duration-300 hover:-translate-y-0.5 cursor-default"
        style={{
          background: 'rgba(12, 17, 30, 0.7)',
          border: `1px solid rgba(255, 255, 255, 0.04)`,
        }}
        onMouseEnter={(e) => {
          (e.currentTarget as HTMLDivElement).style.borderColor = feature.borderColor;
        }}
        onMouseLeave={(e) => {
          (e.currentTarget as HTMLDivElement).style.borderColor = 'rgba(255, 255, 255, 0.04)';
        }}
      >
        {/* Subtle gradient background on hover */}
        <div className={cn(
          'absolute inset-0 rounded-2xl bg-gradient-to-b opacity-0 group-hover:opacity-100 transition-opacity duration-500',
          feature.gradient
        )} />

        <div className="relative z-10">
          <div className="mb-5">
            <Icon className={cn('w-5 h-5', feature.color)} strokeWidth={1.5} />
          </div>
          <h3 className="text-[15px] font-semibold text-white mb-2.5 tracking-tight">{feature.title}</h3>
          <p className="text-[13px] text-white/35 leading-relaxed font-light">{feature.description}</p>
        </div>
      </div>
    </div>
  );
}
