import { Badge } from '../ui/Badge';
import { Button } from '../ui/Button';
import { ArrowRight, Sparkles } from 'lucide-react';

export function HeroSection() {
  return (
    <section
      id="hero"
      className="relative min-h-[100vh] flex flex-col items-center justify-center overflow-hidden"
    >
      {/* ── Background Layers ── */}
      {/* Animated grid */}
      <div className="hero-grid" />

      {/* Noise texture */}
      <div className="noise-overlay" />

      {/* Multi-layer radial glows */}
      <div className="hero-glow" />

      {/* Star field */}
      <div className="star-field" />

      {/* Horizon line at bottom */}
      <div className="hero-horizon" />

      {/* Light beam from bottom center */}
      <div className="light-beam" />

      {/* ── Content ── */}
      <div className="relative z-10 section-wrapper text-center flex flex-col items-center gap-8 px-4 pt-24 pb-32">
        {/* Badge */}
        <div
          className="animate-fade-in"
        >
          <Badge glow>
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-accent-blue opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-accent-blue"></span>
            </span>
            Now in Early Access
          </Badge>
        </div>

        {/* Headline */}
        <h1
          className="text-display-xl max-w-4xl leading-[1.05] tracking-tight animate-fade-up"
          style={{ animationDelay: '0.15s', animationFillMode: 'backwards' }}
        >
          <span className="text-gradient-hero">Your industrial</span>
          <br />
          <span className="text-gradient-hero">documents, understood</span>
          <br />
          <span className="text-gradient">by AI.</span>
        </h1>

        {/* Subtitle */}
        <p
          className="text-lg md:text-xl text-white/40 max-w-xl leading-relaxed font-light animate-fade-up"
          style={{ animationDelay: '0.3s', animationFillMode: 'backwards' }}
        >
          Upload equipment manuals, SOPs, and maintenance logs.
          Ask questions in plain language. Get answers with source citations.
        </p>

        {/* CTAs */}
        <div
          className="flex flex-col sm:flex-row items-center gap-4 mt-2 animate-fade-up"
          style={{ animationDelay: '0.45s', animationFillMode: 'backwards' }}
        >
          <Button
            variant="primary"
            size="lg"
            iconRight={<ArrowRight className="w-4 h-4" />}
            className="shadow-[0_0_40px_rgba(59,130,246,0.25)] hover:shadow-[0_0_60px_rgba(59,130,246,0.35)]"
          >
            Start Building — Free
          </Button>
          <Button variant="secondary" size="lg">
            See How It Works
          </Button>
        </div>

        {/* Subtle trust line — no fake numbers */}
        <div
          className="flex flex-wrap items-center justify-center gap-x-8 gap-y-2 mt-6 animate-fade-up"
          style={{ animationDelay: '0.6s', animationFillMode: 'backwards' }}
        >
          {[
            'PDF & DOCX Support',
            'Source Citations',
            'On-Premise Available',
          ].map((item) => (
            <div key={item} className="flex items-center gap-2 text-xs text-white/25 font-medium tracking-wide">
              <span className="text-white/15">—</span>
              {item}
            </div>
          ))}
        </div>
      </div>

      {/* Bottom gradient fade */}
      <div className="absolute bottom-0 left-0 right-0 h-40 bg-gradient-to-t from-void to-transparent pointer-events-none z-10" />
    </section>
  );
}
