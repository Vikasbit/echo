import { useState, useEffect } from 'react';
import { cn } from '../../lib/utils';
import { Menu, X, ArrowRight } from 'lucide-react';

const NAV_LINKS = [
  { label: 'Features', href: '#features' },
  { label: 'How It Works', href: '#how-it-works' },
  { label: 'Use Cases', href: '#industries' },
  { label: 'Pricing', href: '#enterprise' },
  { label: 'FAQ', href: '#faq' },
];

export function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  useEffect(() => {
    document.body.style.overflow = mobileOpen ? 'hidden' : '';
    return () => { document.body.style.overflow = ''; };
  }, [mobileOpen]);

  return (
    <>
      <nav
        className={cn(
          'fixed top-0 left-0 right-0 z-50 transition-all duration-500',
          scrolled
            ? 'bg-void/70 backdrop-blur-2xl border-b border-white/[0.04]'
            : 'bg-transparent'
        )}
      >
        <div className="section-wrapper">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <a href="#hero" className="flex items-center gap-2.5 group">
              <div className="w-8 h-8 rounded-lg bg-white flex items-center justify-center group-hover:shadow-[0_0_20px_rgba(255,255,255,0.15)] transition-shadow duration-300">
                <span className="text-black font-extrabold text-xs tracking-tighter">IN</span>
              </div>
              <span className="text-white font-semibold text-sm tracking-tight">
                Echo
              </span>
            </a>

            {/* Center Nav */}
            <div className="hidden lg:flex items-center gap-1">
              {NAV_LINKS.map((link) => (
                <a
                  key={link.label}
                  href={link.href}
                  className="px-3.5 py-1.5 text-[13px] font-medium text-white/40 hover:text-white/90 transition-colors duration-200"
                >
                  {link.label}
                </a>
              ))}
            </div>

            {/* Right */}
            <div className="hidden lg:flex items-center gap-2">
              <a
                href="/login"
                className="px-3.5 py-1.5 text-[13px] font-medium text-white/40 hover:text-white transition-colors"
              >
                Log in
              </a>
              <a
                href="#enterprise"
                className="group inline-flex items-center gap-1.5 px-4 py-2 text-[13px] font-semibold text-white bg-white/[0.08] hover:bg-white/[0.12] border border-white/[0.08] hover:border-white/[0.15] rounded-lg transition-all duration-200"
              >
                Get Started
                <ArrowRight className="w-3.5 h-3.5 text-white/50 group-hover:text-white group-hover:translate-x-0.5 transition-all" />
              </a>
            </div>

            {/* Mobile Toggle */}
            <button
              onClick={() => setMobileOpen(!mobileOpen)}
              className="lg:hidden w-9 h-9 flex items-center justify-center rounded-lg text-white/50 hover:text-white hover:bg-white/5 transition-colors"
              aria-label="Toggle menu"
            >
              {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </nav>

      {/* Mobile Menu */}
      {mobileOpen && (
        <div className="fixed inset-0 z-40 lg:hidden">
          <div
            className="absolute inset-0 bg-black/70 backdrop-blur-sm"
            onClick={() => setMobileOpen(false)}
          />
          <div className="absolute top-0 right-0 w-72 h-full bg-void/95 backdrop-blur-2xl border-l border-white/[0.06] animate-slide-in-right">
            <div className="flex flex-col p-6 pt-20 gap-1">
              {NAV_LINKS.map((link) => (
                <a
                  key={link.label}
                  href={link.href}
                  onClick={() => setMobileOpen(false)}
                  className="px-4 py-3 text-sm font-medium text-white/60 hover:text-white hover:bg-white/[0.04] rounded-lg transition-colors"
                >
                  {link.label}
                </a>
              ))}
              <div className="border-t border-white/[0.06] mt-4 pt-4 flex flex-col gap-2">
                <a
                  href="/login"
                  className="px-4 py-3 text-sm font-medium text-white/50 text-center rounded-lg border border-white/[0.06] hover:bg-white/[0.04] transition-colors"
                >
                  Log in
                </a>
                <a
                  href="#enterprise"
                  onClick={() => setMobileOpen(false)}
                  className="px-4 py-3 text-sm font-semibold text-white text-center rounded-lg bg-primary hover:bg-primary/90 transition-colors"
                >
                  Get Started
                </a>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
