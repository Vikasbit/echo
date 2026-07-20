import { Link, useLocation } from "react-router-dom";
import { Search, Bell, Settings, Asterisk, LayoutDashboard, MessageSquare, FileText } from "lucide-react";
import { cn } from "../../lib/utils";

const NAV_ITEMS = [
  { name: "Dashboard", href: "/", icon: LayoutDashboard },
  { name: "Chat", href: "/chat", icon: MessageSquare },
  { name: "Documents", href: "/documents", icon: FileText },
];

export function Header() {
  const location = useLocation();

  return (
    <header className="h-24 flex items-center justify-between px-8 border-b border-white/5 bg-[#151515] z-20">
      {/* Left Logo */}
      <div className="flex-shrink-0">
        <Link to="/" className="w-12 h-12 rounded-full bg-white flex items-center justify-center hover:scale-105 transition-transform shadow-[0_0_15px_rgba(255,255,255,0.2)]">
          <Asterisk className="w-8 h-8 text-black" strokeWidth={3} />
        </Link>
      </div>

      {/* Center Navigation Pills */}
      <nav className="flex items-center gap-2 bg-[#1c1c1e] p-1.5 rounded-full border border-white/5">
        {NAV_ITEMS.map((item) => {
          const isActive = location.pathname === item.href || 
            (item.href !== "/" && location.pathname.startsWith(item.href));
            
          return (
            <Link
              key={item.name}
              to={item.href}
              className={cn(
                "px-6 py-2.5 text-sm font-semibold rounded-full transition-all duration-300",
                isActive 
                  ? "bg-white text-black shadow-md" 
                  : "text-white/60 hover:text-white hover:bg-white/5"
              )}
            >
              {item.name}
            </Link>
          );
        })}
      </nav>

      {/* Right Actions */}
      <div className="flex items-center gap-3 flex-shrink-0">
        <button className="w-10 h-10 flex items-center justify-center rounded-full border border-white/10 bg-[#1c1c1e] text-white/60 hover:text-white hover:bg-white/10 transition-colors">
          <Settings className="w-4 h-4" />
        </button>
        <button className="relative w-10 h-10 flex items-center justify-center rounded-full border border-white/10 bg-[#1c1c1e] text-white/60 hover:text-white hover:bg-white/10 transition-colors">
          <Bell className="w-4 h-4" />
          <span className="absolute top-2.5 right-2.5 w-1.5 h-1.5 bg-primary rounded-full"></span>
        </button>
        <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-accent to-primary flex items-center justify-center cursor-pointer ml-2 shadow-[0_0_15px_rgba(122,90,248,0.3)] hover:scale-105 transition-transform">
          <span className="text-white font-bold text-sm">V</span>
        </div>
      </div>
    </header>
  );
}
