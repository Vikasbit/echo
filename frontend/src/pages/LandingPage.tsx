import { Navbar } from '../components/landing/Navbar';
import { HeroSection } from '../components/landing/HeroSection';
import { MetricsBar } from '../components/landing/MetricsBar';
import { FeaturesSection } from '../components/landing/FeaturesSection';
import { HowItWorksSection } from '../components/landing/HowItWorksSection';
import { ProductShowcase } from '../components/landing/ProductShowcase';
import { BenefitsSection } from '../components/landing/BenefitsSection';
import { IndustriesSection } from '../components/landing/IndustriesSection';
import { EnterpriseSection } from '../components/landing/EnterpriseSection';
import { TestimonialsSection } from '../components/landing/TestimonialsSection';
import { FAQSection } from '../components/landing/FAQSection';
import { CTASection } from '../components/landing/CTASection';
import { Footer } from '../components/landing/Footer';

export function LandingPage() {
  return (
    <div className="min-h-screen bg-void text-white overflow-x-hidden">
      <Navbar />
      <main>
        <HeroSection />
        <MetricsBar />
        <FeaturesSection />
        <HowItWorksSection />
        <ProductShowcase />
        <BenefitsSection />
        <IndustriesSection />
        <EnterpriseSection />
        <TestimonialsSection />
        <FAQSection />
        <CTASection />
      </main>
      <Footer />
    </div>
  );
}
