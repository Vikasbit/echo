import { useState } from 'react';
import { SectionHeading } from '../ui/SectionHeading';
import { useScrollReveal } from '../../hooks/useScrollReveal';
import { cn } from '../../lib/utils';
import {
  MessageSquareText,
  FileText,
  GitBranch,
  Cpu,
  Send,
  Sparkles,
  Search,
} from 'lucide-react';

const TABS = [
  { id: 'chat', label: 'AI Chat', icon: MessageSquareText },
  { id: 'docs', label: 'Documents', icon: FileText },
  { id: 'graph', label: 'Knowledge Graph', icon: GitBranch },
  { id: 'equipment', label: 'Equipment', icon: Cpu },
];

export function ProductShowcase() {
  const [activeTab, setActiveTab] = useState('chat');
  const { ref, isRevealed } = useScrollReveal({ threshold: 0.05 });

  return (
    <section id="product-showcase" className="py-28 md:py-36 relative">
      <div className="section-wrapper relative z-10">
        <SectionHeading
          overline="Product"
          title="See what you're"
          titleHighlight="building"
          subtitle="A complete knowledge intelligence platform for engineering teams."
        />

        {/* Tabs */}
        <div className="flex items-center justify-center mb-10">
          <div className="inline-flex items-center gap-0.5 p-1 rounded-xl bg-white/[0.03] border border-white/[0.04]">
            {TABS.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={cn(
                    'flex items-center gap-2 px-4 py-2 rounded-lg text-[13px] font-medium transition-all duration-200',
                    activeTab === tab.id
                      ? 'bg-white/[0.08] text-white shadow-sm'
                      : 'text-white/30 hover:text-white/60'
                  )}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span className="hidden sm:inline">{tab.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Browser Mockup */}
        <div
          ref={ref}
          className={cn('reveal-scale', isRevealed && 'revealed')}
        >
          <div className="relative">
            {/* Glow behind the browser */}
            <div className="absolute -inset-4 bg-gradient-to-b from-blue-500/[0.03] to-transparent rounded-3xl blur-xl pointer-events-none" />

            <div
              className="relative rounded-xl overflow-hidden border border-white/[0.06]"
              style={{ background: 'linear-gradient(180deg, rgba(15,20,35,0.9) 0%, rgba(8,12,24,0.95) 100%)' }}
            >
              {/* Browser chrome */}
              <div className="flex items-center gap-2 px-4 py-3 border-b border-white/[0.04] bg-white/[0.02]">
                <div className="flex gap-1.5">
                  <div className="w-2.5 h-2.5 rounded-full bg-white/[0.06]" />
                  <div className="w-2.5 h-2.5 rounded-full bg-white/[0.06]" />
                  <div className="w-2.5 h-2.5 rounded-full bg-white/[0.06]" />
                </div>
                <div className="flex-1 flex justify-center">
                  <div className="px-4 py-1 rounded-md bg-white/[0.03] text-[11px] text-white/20 font-mono flex items-center gap-2">
                    <Search className="w-3 h-3" />
                    app.indusai.com
                  </div>
                </div>
                <div className="w-12" />
              </div>

              {/* Content */}
              <div className="p-5 md:p-8 min-h-[420px] md:min-h-[480px]">
                {activeTab === 'chat' && <ChatPreview />}
                {activeTab === 'docs' && <DocsPreview />}
                {activeTab === 'graph' && <GraphPreview />}
                {activeTab === 'equipment' && <EquipmentPreview />}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ── Mock Previews ── */

function ChatPreview() {
  return (
    <div className="flex flex-col gap-5 max-w-2xl mx-auto">
      {/* AI response */}
      <div className="flex gap-3">
        <div className="w-7 h-7 rounded-md bg-gradient-to-br from-blue-500/20 to-violet-500/20 border border-white/[0.06] flex items-center justify-center flex-shrink-0 mt-0.5">
          <Sparkles className="w-3.5 h-3.5 text-blue-400" />
        </div>
        <div className="space-y-3 flex-1">
          <div className="rounded-xl rounded-tl-sm p-4 bg-white/[0.02] border border-white/[0.04]">
            <p className="text-[13px] text-white/60 leading-relaxed">
              Based on <span className="text-blue-400">HYD-Manual-v3.pdf</span> Section 4.2.3, the hydraulic pump housing bolts require a torque specification of <span className="text-white font-medium">45 Nm ± 5 Nm</span>.
            </p>
            <p className="text-[13px] text-white/60 leading-relaxed mt-2">
              Apply torque in a star pattern sequence. Re-torque after 24 hours of operation. Use calibrated torque wrench only.
            </p>
          </div>
          <div className="flex gap-2">
            <span className="px-2.5 py-1 rounded-md bg-blue-500/[0.08] border border-blue-500/[0.1] text-blue-400/80 text-[11px] font-medium">
              HYD-Manual-v3.pdf · p.47
            </span>
            <span className="px-2.5 py-1 rounded-md bg-violet-500/[0.08] border border-violet-500/[0.1] text-violet-400/80 text-[11px] font-medium">
              SOP-042.docx · p.12
            </span>
          </div>
        </div>
      </div>

      {/* User message */}
      <div className="flex justify-end">
        <div className="bg-white/[0.06] border border-white/[0.06] rounded-xl rounded-tr-sm px-4 py-3 max-w-sm">
          <p className="text-[13px] text-white/70 font-medium">What's the recommended inspection interval?</p>
        </div>
      </div>

      {/* AI typing */}
      <div className="flex gap-3">
        <div className="w-7 h-7 rounded-md bg-gradient-to-br from-blue-500/20 to-violet-500/20 border border-white/[0.06] flex items-center justify-center flex-shrink-0 mt-0.5">
          <Sparkles className="w-3.5 h-3.5 text-blue-400" />
        </div>
        <div className="rounded-xl rounded-tl-sm p-4 bg-white/[0.02] border border-white/[0.04]">
          <div className="flex items-center gap-1.5">
            <div className="w-1.5 h-1.5 rounded-full bg-blue-400/60 animate-pulse" />
            <div className="w-1.5 h-1.5 rounded-full bg-blue-400/40 animate-pulse" style={{ animationDelay: '0.2s' }} />
            <div className="w-1.5 h-1.5 rounded-full bg-blue-400/20 animate-pulse" style={{ animationDelay: '0.4s' }} />
          </div>
        </div>
      </div>

      {/* Input */}
      <div className="mt-4 flex items-center gap-2 p-2.5 rounded-xl border border-white/[0.06] bg-white/[0.02]">
        <input
          readOnly
          placeholder="Ask about your documents..."
          className="flex-1 bg-transparent text-[13px] text-white/30 outline-none px-2"
        />
        <div className="w-8 h-8 rounded-lg bg-white/[0.06] flex items-center justify-center">
          <Send className="w-3.5 h-3.5 text-white/30" />
        </div>
      </div>
    </div>
  );
}

function DocsPreview() {
  const docs = [
    { name: 'HYD-Manual-v3.pdf', type: 'Equipment Manual', pages: 142, status: 'Indexed' },
    { name: 'SOP-042-Pump-Maintenance.docx', type: 'Standard Operating Procedure', pages: 28, status: 'Indexed' },
    { name: 'Incident-Report-2024-Q3.pdf', type: 'Incident Report', pages: 15, status: 'Indexed' },
    { name: 'Compressor-System-Guide.pdf', type: 'Equipment Manual', pages: 234, status: 'Processing' },
    { name: 'Safety-Audit-Dec-2024.pdf', type: 'Audit Report', pages: 45, status: 'Indexed' },
  ];

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <h3 className="text-sm font-semibold text-white/80">Documents</h3>
          <span className="text-[11px] text-white/20 font-mono">{docs.length} files</span>
        </div>
        <div className="px-3 py-1.5 rounded-lg bg-blue-500/10 border border-blue-500/20 text-blue-400 text-[11px] font-semibold cursor-default">
          + Upload
        </div>
      </div>
      {docs.map((doc) => (
        <div key={doc.name} className="flex items-center gap-3 p-3.5 rounded-lg border border-white/[0.04] bg-white/[0.01] hover:bg-white/[0.02] transition-colors">
          <div className="w-8 h-8 rounded-lg bg-white/[0.04] flex items-center justify-center flex-shrink-0">
            <FileText className="w-4 h-4 text-white/25" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-[13px] font-medium text-white/70 truncate">{doc.name}</p>
            <p className="text-[11px] text-white/20">{doc.type} · {doc.pages} pages</p>
          </div>
          <span className={cn(
            'px-2 py-0.5 rounded text-[10px] font-medium',
            doc.status === 'Indexed' ? 'bg-emerald-500/10 text-emerald-400/70' : 'bg-amber-500/10 text-amber-400/70'
          )}>
            {doc.status}
          </span>
        </div>
      ))}
    </div>
  );
}

function GraphPreview() {
  return (
    <div className="flex items-center justify-center h-[380px] relative">
      {/* Central node */}
      <div className="relative">
        <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500/15 to-violet-500/15 border border-white/[0.08] flex items-center justify-center shadow-[0_0_30px_rgba(59,130,246,0.1)] z-10 relative">
          <GitBranch className="w-6 h-6 text-blue-400/70" />
        </div>

        {/* Nodes */}
        {[
          { label: 'Pump HYD-001', x: -160, y: -70, color: 'border-blue-500/15 bg-blue-500/5' },
          { label: 'SOP-042', x: 150, y: -50, color: 'border-violet-500/15 bg-violet-500/5' },
          { label: 'Bearing Assembly', x: -140, y: 70, color: 'border-cyan-500/15 bg-cyan-500/5' },
          { label: 'Incident #47', x: 160, y: 80, color: 'border-rose-500/15 bg-rose-500/5' },
          { label: 'Motor B-200', x: 10, y: -130, color: 'border-emerald-500/15 bg-emerald-500/5' },
          { label: 'Manual v3', x: -50, y: 130, color: 'border-amber-500/15 bg-amber-500/5' },
        ].map((node) => (
          <div key={node.label}>
            <svg className="absolute top-1/2 left-1/2 w-0 h-0 overflow-visible pointer-events-none" style={{ zIndex: 0 }}>
              <line x1="0" y1="0" x2={node.x} y2={node.y} stroke="rgba(255,255,255,0.04)" strokeWidth="1" />
            </svg>
            <div
              className={cn('absolute top-1/2 left-1/2 px-3 py-1.5 rounded-lg text-[11px] font-medium text-white/50 border', node.color)}
              style={{ transform: `translate(calc(-50% + ${node.x}px), calc(-50% + ${node.y}px))` }}
            >
              {node.label}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function EquipmentPreview() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
      <div className="space-y-3">
        <h3 className="text-sm font-semibold text-white/80 mb-4">Equipment Registry</h3>
        {[
          { name: 'Hydraulic Pump Unit A', id: 'HYD-001', status: 'Operational', docs: 12 },
          { name: 'Compressor System C', id: 'CMP-003', status: 'Needs Service', docs: 8 },
          { name: 'Conveyor Belt Line 2', id: 'CNV-002', status: 'Operational', docs: 5 },
        ].map((eq) => (
          <div key={eq.id} className="p-3.5 rounded-lg border border-white/[0.04] bg-white/[0.01]">
            <div className="flex items-center justify-between mb-2">
              <div>
                <p className="text-[13px] font-medium text-white/70">{eq.name}</p>
                <p className="text-[11px] text-white/20 font-mono">{eq.id}</p>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-1.5">
                <div className={cn('w-1.5 h-1.5 rounded-full', eq.status === 'Operational' ? 'bg-emerald-500' : 'bg-amber-500')} />
                <span className="text-[11px] text-white/30">{eq.status}</span>
              </div>
              <span className="text-[11px] text-white/20">{eq.docs} docs linked</span>
            </div>
          </div>
        ))}
      </div>
      <div className="p-5 rounded-lg border border-white/[0.04] bg-white/[0.01]">
        <span className="text-[10px] text-white/20 font-mono tracking-wider uppercase">Equipment Detail</span>
        <h3 className="text-base font-semibold text-white/80 mt-2 mb-5">Hydraulic Pump Unit A</h3>
        <div className="space-y-3 text-[13px]">
          {[
            ['ID', 'HYD-001'],
            ['Manufacturer', 'Parker Hannifin'],
            ['Model', 'PV270R1K1T1'],
            ['Installed', '2022-03-15'],
            ['Last Service', '2024-09-15'],
            ['Linked Docs', '12'],
          ].map(([label, value]) => (
            <div key={label} className="flex items-center justify-between py-1.5 border-b border-white/[0.03]">
              <span className="text-white/20">{label}</span>
              <span className="text-white/60 font-medium">{value}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
