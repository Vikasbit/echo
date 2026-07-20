import { useState, useRef, useEffect } from 'react';
import { cn } from '../../lib/utils';
import { ChevronDown } from 'lucide-react';

interface AccordionItemProps {
  question: string;
  answer: string;
  isOpen?: boolean;
  onToggle?: () => void;
}

export function AccordionItem({ question, answer, isOpen = false, onToggle }: AccordionItemProps) {
  const contentRef = useRef<HTMLDivElement>(null);
  const [height, setHeight] = useState(0);

  useEffect(() => {
    if (contentRef.current) {
      setHeight(contentRef.current.scrollHeight);
    }
  }, [answer]);

  return (
    <div
      className={cn(
        'border-b border-white/8 transition-colors duration-200',
        isOpen && 'border-white/12'
      )}
    >
      <button
        onClick={onToggle}
        className="w-full flex items-center justify-between py-6 text-left group"
      >
        <span
          className={cn(
            'text-body-md font-medium transition-colors duration-200',
            isOpen ? 'text-white' : 'text-white/70 group-hover:text-white'
          )}
        >
          {question}
        </span>
        <ChevronDown
          className={cn(
            'w-5 h-5 text-white/40 transition-transform duration-300 flex-shrink-0 ml-4',
            isOpen && 'rotate-180 text-accent-blue'
          )}
        />
      </button>
      <div
        style={{
          height: isOpen ? height : 0,
          '--accordion-height': `${height}px`,
        } as React.CSSProperties}
        className={cn(
          'overflow-hidden transition-all duration-300 ease-out',
          isOpen ? 'opacity-100' : 'opacity-0'
        )}
      >
        <div ref={contentRef} className="pb-6 text-body-sm text-white/50 leading-relaxed">
          {answer}
        </div>
      </div>
    </div>
  );
}
