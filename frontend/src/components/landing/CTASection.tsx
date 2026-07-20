import { useScrollReveal } from '../../hooks/useScrollReveal';
import { cn } from '../../lib/utils';
import { ArrowRight } from 'lucide-react';

export function CTASection() {
  const { ref, isRevealed } = useScrollReveal({ threshold: 0.15 });

  return (
    <section className="py-28 md:py-36 relative">
      <div className="section-wrapper relative z-10">
        <div
          ref={ref}
          className={cn('reveal-scale', isRevealed && 'revealed')}
        >
          <div className="relative rounded-2xl overflow-hidden border border-white/[0.06]">
            {/* Background */}
            <div
              className="absolute inset-0"
              style={{
                background: `
                  radial-gradient(ellipse 60% 50% at 50% 0%, rgba(59,130,246,0.08) 0%, transparent 100%),
                  radial-gradient(ellipse 50% 50% at 80% 100%, rgba(139,92,246,0.06) 0%, transparent 100%),
                  linear-gradient(180deg, rgba(12,17,30,0.9) 0%, rgba(8,12,24,0.95) 100%)
                `,
              }}
            />

            {/* Grid overlay */}
            <div
              className="absolute inset-0"
              style={{
                backgroundImage: 'linear-gradient(rgba(59,130,246,0.02) 1px, transparent 1px), linear-gradient(90deg, rgba(59,130,246,0.02) 1px, transparent 1px)',
                backgroundSize: '40px 40px',
                maskImage: 'radial-gradient(ellipse 80% 80% at 50% 30%, black, transparent)',
                WebkitMaskImage: 'radial-gradient(ellipse 80% 80% at 50% 30%, black, transparent)',
              }}
            />

            {/* Content */}
            <div className="relative z-10 py-20 md:py-28 px-8 text-center flex flex-col items-center gap-5">
              <h2 className="text-display-md md:text-display-lg text-white/90 font-bold tracking-tight max-w-2xl leading-tight">
                Start building your knowledge platform
              </h2>
              <p className="text-base text-white/30 max-w-lg font-light">
                Upload your first document and see how INDUS AI understands it. No credit card, no setup.
              </p>
              <div className="flex flex-col sm:flex-row items-center gap-3 mt-4">
                <a
                  href="#enterprise"
                  className="group inline-flex items-center gap-2 px-7 py-3.5 rounded-xl text-sm font-semibold text-white bg-primary hover:bg-primary/90 shadow-[0_0_40px_rgba(59,130,246,0.2)] hover:shadow-[0_0_60px_rgba(59,130,246,0.3)] transition-all duration-200 active:scale-[0.98]"
                >
                  Get Started — Free
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
                </a>
                <a
                  href="#enterprise"
                  className="inline-flex items-center gap-2 px-7 py-3.5 rounded-xl text-sm font-medium text-white/50 hover:text-white/80 transition-colors"
                >
                  Talk to Sales
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
