import { useEffect, useState } from "react";
import { Search } from "lucide-react";

export function CommandPalette() {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((open) => !open);
      }
    };
    document.addEventListener("keydown", down);
    return () => document.removeEventListener("keydown", down);
  }, []);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm flex items-start justify-center pt-[20vh]">
      <div className="w-full max-w-xl bg-card border border-border shadow-2xl rounded-xl overflow-hidden flex flex-col animate-fade-in">
        <div className="flex items-center px-4 py-3 border-b border-border/50">
          <Search className="w-5 h-5 text-muted-foreground mr-3" />
          <input 
            type="text" 
            placeholder="Search documents, equipment, conversations..." 
            className="flex-1 bg-transparent border-none outline-none text-foreground placeholder:text-muted-foreground"
            autoFocus
          />
          <kbd className="pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border border-border bg-background px-1.5 font-mono text-[10px] font-medium text-muted-foreground ml-2">
            ESC
          </kbd>
        </div>
        <div className="p-4 flex flex-col items-center justify-center h-32 text-muted-foreground">
          <p className="text-sm">Start typing to search across Echo</p>
        </div>
      </div>
    </div>
  );
}
