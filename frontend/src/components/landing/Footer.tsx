import { ExternalLink, Building2, Globe } from 'lucide-react';

const FOOTER_LINKS = {
  Product: [
    { label: 'Features', href: '#features' },
    { label: 'How It Works', href: '#how-it-works' },
    { label: 'Use Cases', href: '#use-cases' },
    { label: 'Pricing', href: '#enterprise' },
  ],
  Resources: [
    { label: 'Documentation', href: '#' },
    { label: 'API Reference', href: '#' },
    { label: 'Changelog', href: '#' },
  ],
  Company: [
    { label: 'About', href: '#' },
    { label: 'Contact', href: '#' },
    { label: 'Careers', href: '#' },
  ],
  Legal: [
    { label: 'Privacy', href: '#' },
    { label: 'Terms', href: '#' },
    { label: 'Security', href: '#' },
  ],
};

const SOCIAL_LINKS = [
  { icon: ExternalLink, href: '#', label: 'GitHub' },
  { icon: Building2, href: '#', label: 'LinkedIn' },
  { icon: Globe, href: '#', label: 'Website' },
];

export function Footer() {
  return (
    <footer className="border-t border-white/[0.04]">
      <div className="section-wrapper py-14">
        <div className="grid grid-cols-2 md:grid-cols-6 gap-8">
          {/* Brand */}
          <div className="col-span-2">
            <a href="#hero" className="flex items-center gap-2.5 mb-3">
              <div className="w-7 h-7 rounded-md bg-white flex items-center justify-center">
                <span className="text-black font-extrabold text-[10px] tracking-tighter">IN</span>
              </div>
              <span className="text-white/80 font-semibold text-sm tracking-tight">INDUS AI</span>
            </a>
            <p className="text-[13px] text-white/20 leading-relaxed max-w-xs mb-5 font-light">
              Industrial knowledge intelligence platform.
            </p>
            <div className="flex gap-2">
              {SOCIAL_LINKS.map((social) => {
                const Icon = social.icon;
                return (
                  <a
                    key={social.label}
                    href={social.href}
                    aria-label={social.label}
                    className="w-8 h-8 rounded-lg border border-white/[0.04] bg-white/[0.01] flex items-center justify-center text-white/20 hover:text-white/50 hover:bg-white/[0.03] transition-all"
                  >
                    <Icon className="w-3.5 h-3.5" />
                  </a>
                );
              })}
            </div>
          </div>

          {/* Links */}
          {Object.entries(FOOTER_LINKS).map(([category, links]) => (
            <div key={category}>
              <h4 className="text-[11px] font-medium text-white/25 uppercase tracking-wider mb-3">
                {category}
              </h4>
              <ul className="space-y-2">
                {links.map((link) => (
                  <li key={link.label}>
                    <a href={link.href} className="text-[13px] text-white/30 hover:text-white/60 transition-colors">
                      {link.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-12 pt-6 border-t border-white/[0.03] flex flex-col md:flex-row items-center justify-between gap-3">
          <p className="text-[11px] text-white/15">
            © {new Date().getFullYear()} INDUS AI
          </p>
        </div>
      </div>
    </footer>
  );
}
