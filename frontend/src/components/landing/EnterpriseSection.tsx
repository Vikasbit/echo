import { SectionHeading } from '../ui/SectionHeading';
import { useScrollReveal } from '../../hooks/useScrollReveal';
import { cn } from '../../lib/utils';
import { Cloud, Server, Check, ArrowRight } from 'lucide-react';

const PLANS = [
  {
    name: 'Cloud',
    icon: Cloud,
    description: 'Managed platform. Get started in minutes.',
    price: 'Free to start',
    priceNote: 'then usage-based pricing',
    features: [
      'Hosted AI models',
      'Automatic scaling',
      'Up to 10,000 documents',
      '99.9% uptime SLA',
      'Standard support',
    ],
    cta: 'Start Building — Free',
    ctaStyle: 'bg-white/[0.08] hover:bg-white/[0.12] text-white border border-white/[0.08]',
  },
  {
    name: 'Enterprise',
    icon: Server,
    description: 'Private deployment. Full control.',
    price: 'Custom',
    priceNote: 'annual license',
    recommended: true,
    features: [
      'Fully offline — air-gapped capable',
      'Local AI models (no data leaves your network)',
      'On-premise or private cloud',
      'Unlimited documents',
      'Custom integrations (SAP, Maximo)',
      'Dedicated support & onboarding',
      'SSO, RBAC, audit logging',
    ],
    cta: 'Contact Sales',
    ctaStyle: 'bg-primary hover:bg-primary/90 text-white shadow-[0_0_30px_rgba(59,130,246,0.15)]',
  },
];

export function EnterpriseSection() {
  return (
    <section id="enterprise" className="py-28 md:py-36 relative">
      <div className="section-wrapper relative z-10">
        <SectionHeading
          overline="Pricing"
          title="Start free, scale to"
          titleHighlight="enterprise"
          subtitle="No credit card required. Deploy on our cloud or your own infrastructure."
        />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5 max-w-4xl mx-auto">
          {PLANS.map((plan, i) => (
            <PlanCard key={plan.name} plan={plan} index={i} />
          ))}
        </div>
      </div>
    </section>
  );
}

function PlanCard({
  plan,
  index,
}: {
  plan: (typeof PLANS)[0];
  index: number;
}) {
  const { ref, isRevealed } = useScrollReveal({ threshold: 0.1 });
  const Icon = plan.icon;

  return (
    <div
      ref={ref}
      className={cn('reveal', isRevealed && 'revealed')}
      style={{ transitionDelay: `${index * 100}ms` }}
    >
      <div className={cn(
        'relative rounded-2xl p-7 md:p-8 h-full flex flex-col border',
        plan.recommended
          ? 'border-blue-500/20 bg-gradient-to-b from-blue-500/[0.04] to-transparent'
          : 'border-white/[0.04] bg-[rgba(12,17,30,0.5)]'
      )}>
        {plan.recommended && (
          <div className="absolute -top-2.5 left-6 px-3 py-0.5 rounded-full bg-blue-500/20 border border-blue-500/30 text-[10px] font-bold text-blue-400 uppercase tracking-wider">
            Recommended
          </div>
        )}

        <div className="flex items-center gap-3 mb-4">
          <Icon className="w-4 h-4 text-white/30" strokeWidth={1.5} />
          <h3 className="text-base font-semibold text-white/90">{plan.name}</h3>
        </div>

        <p className="text-[13px] text-white/30 mb-6">{plan.description}</p>

        <div className="mb-6">
          <span className="text-2xl font-bold text-white/90">{plan.price}</span>
          <span className="text-[12px] text-white/20 ml-2">{plan.priceNote}</span>
        </div>

        <ul className="space-y-3 mb-8 flex-1">
          {plan.features.map((feature) => (
            <li key={feature} className="flex items-start gap-2.5 text-[13px] text-white/45">
              <Check className="w-3.5 h-3.5 mt-0.5 flex-shrink-0 text-white/20" />
              {feature}
            </li>
          ))}
        </ul>

        <button className={cn(
          'w-full flex items-center justify-center gap-2 py-3 px-4 rounded-xl text-[13px] font-semibold transition-all duration-200 active:scale-[0.98]',
          plan.ctaStyle
        )}>
          {plan.cta}
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
}
