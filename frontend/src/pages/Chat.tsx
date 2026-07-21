import { useState, useRef, useEffect } from "react";
import { Send, Loader2, FileText, AlertCircle } from "lucide-react";
import { api } from "../lib/api";

type Message = {
  role: "user" | "assistant" | "system";
  content: string;
  sources?: any[];
  metadata?: any;
};

export function Chat() {
  const [messages, setMessages] = useState<Message[]>([
    { role: "assistant", content: "### Summary\nHello! I am Echo. I can answer questions specifically about the documents you have uploaded.\n\n### Explanation\nI use an advanced RAG (Retrieval-Augmented Generation) pipeline to search your private documents. How can I help you today?" }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg = input.trim();
    setInput("");
    setMessages(prev => [...prev, { role: "user", content: userMsg }]);
    setLoading(true);

    try {
      // Create conversation if none exists (mocking conversation ID for MVP)
      const convId = "default-conv-id"; 

      // Send to SSE endpoint
      const response = await fetch(`${api.defaults.baseURL}/chat/${convId}/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': api.defaults.headers.Authorization as string || ''
        },
        body: JSON.stringify({ content: userMsg })
      });

      if (!response.body) throw new Error("No response body");

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let assistantContent = "";
      let assistantSources = [];
      let assistantMetadata = {};

      setMessages(prev => [...prev, { role: "assistant", content: "" }]);

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n\n');
        
        for (const line of lines) {
          if (line.startsWith('event: chunk')) {
            const dataStr = line.split('data: ')[1];
            if (dataStr) {
              const data = JSON.parse(dataStr);
              assistantContent += data.content;
              setMessages(prev => {
                const newMsgs = [...prev];
                newMsgs[newMsgs.length - 1].content = assistantContent;
                return newMsgs;
              });
            }
          } else if (line.startsWith('event: sources')) {
            const dataStr = line.split('data: ')[1];
            if (dataStr) assistantSources = JSON.parse(dataStr).sources;
          } else if (line.startsWith('event: metadata')) {
            const dataStr = line.split('data: ')[1];
            if (dataStr) assistantMetadata = JSON.parse(dataStr);
          } else if (line.startsWith('event: error')) {
            const dataStr = line.split('data: ')[1];
            if (dataStr) {
              assistantContent += "\n\n**Error:** " + JSON.parse(dataStr).error;
              setMessages(prev => {
                const newMsgs = [...prev];
                newMsgs[newMsgs.length - 1].content = assistantContent;
                return newMsgs;
              });
            }
          }
        }
      }

      setMessages(prev => {
        const newMsgs = [...prev];
        newMsgs[newMsgs.length - 1].sources = assistantSources;
        newMsgs[newMsgs.length - 1].metadata = assistantMetadata;
        return newMsgs;
      });

    } catch (err) {
      console.error(err);
      setMessages(prev => [...prev, { role: "assistant", content: "Sorry, I encountered an error while connecting to the server." }]);
    } finally {
      setLoading(false);
    }
  };

  const formatContent = (content: string) => {
    // Basic markdown parsing for the specific strict headings requested
    let formatted = content
      .replace(/### Summary/g, '<h3 class="text-lg font-semibold text-primary mt-4 mb-2 flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-primary inline-block"></span>Summary</h3>')
      .replace(/### Explanation/g, '<h3 class="text-lg font-semibold text-primary mt-6 mb-2 flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-primary inline-block"></span>Explanation</h3>')
      .replace(/### Recommendations/g, '<h3 class="text-lg font-semibold text-primary mt-6 mb-2 flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-primary inline-block"></span>Recommendations</h3>')
      .replace(/### Confidence Score/g, '<h3 class="text-lg font-semibold text-primary mt-6 mb-2 flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-primary inline-block"></span>Confidence Score</h3>')
      .replace(/### Source Document/g, '<h3 class="text-lg font-semibold text-primary mt-6 mb-2 flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-primary inline-block"></span>Source Document</h3>')
      .replace(/### Page Number/g, '<h3 class="text-lg font-semibold text-primary mt-6 mb-2 flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-primary inline-block"></span>Page Number</h3>')
      .replace(/### Related Documents/g, '<h3 class="text-lg font-semibold text-primary mt-6 mb-2 flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-primary inline-block"></span>Related Documents</h3>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
      .replace(/\n/g, '<br/>'); // Newlines
    
    return <div dangerouslySetInnerHTML={{ __html: formatted }} className="text-sm leading-relaxed" />;
  };

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] max-w-5xl mx-auto animate-fade-in relative z-10">
      <div className="flex-1 overflow-y-auto pr-4 space-y-8 custom-scrollbar">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
            {msg.role === "assistant" && (
              <div className="w-8 h-8 rounded-full bg-white flex-shrink-0 mr-4 flex items-center justify-center mt-1">
                <span className="text-black font-bold text-sm">I</span>
              </div>
            )}
            <div className={`max-w-[85%] rounded-[1.25rem] p-6 ${
              msg.role === "user" 
                ? "bg-primary text-white" 
                : "glass-panel"
            }`}>
              {msg.role === "user" ? (
                <div className="text-sm font-medium">{msg.content}</div>
              ) : (
                <div className="prose prose-invert max-w-none text-white/90">
                  {formatContent(msg.content)}
                  
                  {msg.sources && msg.sources.length > 0 && (
                    <div className="mt-8 pt-5 border-t border-white/10">
                      <h4 className="text-xs font-bold uppercase tracking-wider text-white/50 mb-3 flex items-center gap-2">
                        <FileText className="w-4 h-4" /> References
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {msg.sources.map((s, idx) => (
                          <div key={idx} className="flex items-center gap-3 px-4 py-2 bg-[#2a2a2c] border border-white/5 rounded-xl text-xs hover:border-primary/50 cursor-pointer transition-all">
                            <span className="font-bold text-white">{s.document_title}</span>
                            <span className="text-white/50 font-mono">pg {s.page_number}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="w-8 h-8 rounded-full bg-white flex-shrink-0 mr-4 flex items-center justify-center mt-1 animate-pulse">
                <span className="text-black font-bold text-sm">I</span>
            </div>
            <div className="glass-panel rounded-[1.25rem] p-6 flex items-center gap-4">
              <Loader2 className="w-5 h-5 text-accent animate-spin" />
              <span className="text-sm text-white/80 font-medium tracking-wide">Synthesizing intelligence...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="mt-8 relative">
        <form onSubmit={handleSend} className="relative flex items-center group">
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Ask Echo..."
            className="w-full glass-panel border border-white/10 rounded-full pl-6 pr-16 py-5 text-white placeholder:text-white/40 focus:ring-2 focus:ring-primary/50 focus:border-primary/50 transition-all text-sm font-medium outline-none"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="absolute right-3 p-3 bg-white text-black rounded-full hover:scale-105 disabled:opacity-50 disabled:hover:scale-100 transition-all"
          >
            <Send className="w-5 h-5" />
          </button>
        </form>
        <div className="text-center mt-4 flex justify-center items-center gap-2 opacity-70">
          <AlertCircle className="w-4 h-4 text-white/50" />
          <p className="text-xs text-white/50 font-medium tracking-wide">Echo answers based strictly on uploaded documents. Always verify critical information.</p>
        </div>
      </div>
    </div>
  );
}
