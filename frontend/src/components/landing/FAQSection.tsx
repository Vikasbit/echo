import { useState } from 'react';
import { SectionHeading } from '../ui/SectionHeading';
import { cn } from '../../lib/utils';
import { Plus, Minus } from 'lucide-react';
import { useScrollReveal } from '../../hooks/useScrollReveal';

const FAQ_ITEMS = [
  {
    question: 'What document formats are supported?',
    answer:
      'PDF and DOCX files. The pipeline includes OCR for scanned documents, so even old paper manuals that have been digitized work well. We extract text, tables, and structured data from each document.',
  },
  {
    question: 'How does the AI generate answers?',
    answer:
      'We use a RAG (Retrieval-Augmented Generation) pipeline. When you ask a question, the system finds the most relevant document chunks using semantic search, then generates an answer grounded in those specific sources. Every answer includes citations.',
  },
  {
    question: 'Can it run completely offline?',
    answer:
      'Yes. The Enterprise Edition deploys on your infrastructure with local AI models (LLaMA, Mistral). Zero internet dependency. This is designed for air-gapped environments in defense, energy, and critical infrastructure.',
  },
  {
    question: 'What about data security?',
    answer:
      'Cloud Edition uses encrypted storage and transport. Enterprise Edition keeps all data on your premises with zero external sharing. We support role-based access control, audit logging, and SSO integration via SAML and OIDC.',
  },
  {
    question: 'How long does document processing take?',
    answer:
      'A typical 100-page PDF processes in under 2 minutes — that includes OCR, metadata extraction, embedding generation, and knowledge graph integration. Processing scales linearly with document size.',
  },
  {
    question: 'What integrations are available?',
    answer:
      'REST API for programmatic access. Enterprise customers get custom integrations with CMMS systems (SAP PM, Maximo), document management platforms, and ERP systems.',
  },
];

export function FAQSection() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  return (
    <section id="faq" className="py-28 md:py-36 relative">
      <div className="section-wrapper relative z-10 max-w-2xl">
        <SectionHeading
          overline="FAQ"
          title="Common"
          titleHighlight="questions"
        />

        <div>
          {FAQ_ITEMS.map((item, i) => (
            <FAQItem
              key={i}
              item={item}
              index={i}
              isOpen={openIndex === i}
              onToggle={() => setOpenIndex(openIndex === i ? null : i)}
            />
          ))}
        </div>
      </div>
    </section>
  );
}

function FAQItem({
  item,
  index,
  isOpen,
  onToggle,
}: {
  item: (typeof FAQ_ITEMS)[0];
  index: number;
  isOpen: boolean;
  onToggle: () => void;
}) {
  const { ref, isRevealed } = useScrollReveal({ threshold: 0.2 });

  return (
    <div
      ref={ref}
      className={cn(
        'reveal border-b border-white/[0.04]',
        isRevealed && 'revealed'
      )}
      style={{ transitionDelay: `${index * 50}ms` }}
    >
      <button
        onClick={onToggle}
        className="w-full flex items-center justify-between py-5 text-left group"
      >
        <span className={cn(
          'text-[14px] font-medium transition-colors duration-200 pr-4',
          isOpen ? 'text-white/80' : 'text-white/40 group-hover:text-white/60'
        )}>
          {item.question}
        </span>
        <div className={cn(
          'w-6 h-6 rounded-md flex items-center justify-center flex-shrink-0 transition-all duration-200',
          isOpen ? 'bg-white/[0.06]' : 'bg-transparent'
        )}>
          {isOpen
            ? <Minus className="w-3.5 h-3.5 text-white/40" />
            : <Plus className="w-3.5 h-3.5 text-white/20 group-hover:text-white/40 transition-colors" />
          }
        </div>
      </button>
      <div className={cn(
        'overflow-hidden transition-all duration-300 ease-out',
        isOpen ? 'max-h-96 opacity-100 pb-5' : 'max-h-0 opacity-0'
      )}>
        <p className="text-[13px] text-white/30 leading-relaxed font-light pr-10">
          {item.answer}
        </p>
      </div>
    </div>
  );
}
