import { SectionHeading } from '../ui/SectionHeading';
import { useScrollReveal } from '../../hooks/useScrollReveal';
import { cn } from '../../lib/utils';
import { Car, Factory, Flame, Droplets, Pill, Plane, Truck, Boxes } from 'lucide-react';

const INDUSTRIES = [
  { name: 'Automotive', icon: Car },
  { name: 'Manufacturing', icon: Factory },
  { name: 'Energy', icon: Flame },
  { name: 'Oil & Gas', icon: Droplets },
  { name: 'Pharmaceutical', icon: Pill },
  { name: 'Aerospace', icon: Plane },
  { name: 'Logistics', icon: Truck },
  { name: 'Steel & Metals', icon: Boxes },
];

export function IndustriesSection() {
  const { ref, isRevealed } = useScrollReveal({ threshold: 0.1 });

  return (
    <section id="industries" className="py-28 md:py-36 relative">
      <div className="section-wrapper relative z-10">
        <SectionHeading
          overline="Industries"
          title="Built for"
          titleHighlight="heavy industry"
          subtitle="Any industry with complex technical documentation and equipment."
        />

        <div
          ref={ref}
          className={cn('reveal', isRevealed && 'revealed')}
        >
          <div className="flex flex-wrap items-center justify-center gap-3 md:gap-4 max-w-3xl mx-auto">
            {INDUSTRIES.map((industry) => {
              const Icon = industry.icon;
              return (
                <div
                  key={industry.name}
                  className="flex items-center gap-2.5 px-5 py-3 rounded-xl border border-white/[0.04] bg-white/[0.01] hover:bg-white/[0.03] hover:border-white/[0.08] transition-all duration-200 cursor-default"
                >
                  <Icon className="w-4 h-4 text-white/20" strokeWidth={1.5} />
                  <span className="text-[13px] font-medium text-white/50">{industry.name}</span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
}
