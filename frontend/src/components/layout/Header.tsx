import { Link, useLocation } from "react-router-dom";
import { Search, Bell, Settings, Asterisk, LayoutDashboard, MessageSquare, FileText, Building, CreditCard, User as UserIcon } from "lucide-react";
import { cn } from "../../lib/utils";

import { useAuth } from "../../hooks/useAuth";
import { useState } from "react";

const NAV_ITEMS = [
  { name: "Dashboard", href: "/app", icon: LayoutDashboard },
  { name: "Chat", href: "/app/chat", icon: MessageSquare },
  { name: "Documents", href: "/app/documents", icon: FileText },
];

export function Header() {
  const location = useLocation();
  const { user, signOut } = useAuth();
  const [dropdownOpen, setDropdownOpen] = useState(false);

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
            (item.href !== "/app" && location.pathname.startsWith(item.href));
            
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

        <div className="relative">
          <div 
            onClick={() => setDropdownOpen(!dropdownOpen)}
            className="w-10 h-10 rounded-full bg-gradient-to-tr from-accent to-primary flex items-center justify-center cursor-pointer ml-2 shadow-[0_0_15px_rgba(122,90,248,0.3)] hover:scale-105 transition-transform"
          >
            <span className="text-white font-bold text-sm">
              {user?.user_metadata?.full_name?.charAt(0)?.toUpperCase() || "U"}
            </span>
          </div>

          {dropdownOpen && (
            <div className="absolute right-0 mt-2 w-64 bg-[#1c1c1e] rounded-lg shadow-xl border border-white/10 py-1 z-50 animate-in fade-in slide-in-from-top-2">
              <div className="px-4 py-3 border-b border-white/10 bg-white/5">
                <p className="text-sm font-medium text-white truncate">
                  {user?.user_metadata?.full_name || "User"}
                </p>
                <p className="text-xs text-white/60 truncate mt-0.5">
                  {user?.email}
                </p>
              </div>
              
              <div className="py-2 border-b border-white/10">
                <div className="px-4 py-1.5 flex items-center text-xs font-semibold text-white/40 uppercase tracking-wider">
                  Workspace
                </div>
                <button className="w-full flex items-center px-4 py-2 text-sm text-white/80 hover:bg-white/5 hover:text-white transition-colors">
                  <Building className="w-4 h-4 mr-3 text-white/60" />
                  <span className="truncate">{user?.user_metadata?.company_name || "My Workspace"}</span>
                </button>
              </div>

              <div className="py-2 border-b border-white/10">
                <button className="w-full flex items-center px-4 py-2 text-sm text-white/80 hover:bg-white/5 hover:text-white transition-colors">
                  <UserIcon className="w-4 h-4 mr-3 text-white/60" />
                  Profile Details
                </button>
                <button className="w-full flex items-center px-4 py-2 text-sm text-white/80 hover:bg-white/5 hover:text-white transition-colors">
                  <Settings className="w-4 h-4 mr-3 text-white/60" />
                  Account Settings
                </button>
                <button className="w-full flex items-center px-4 py-2 text-sm text-white/80 hover:bg-white/5 hover:text-white transition-colors">
                  <CreditCard className="w-4 h-4 mr-3 text-white/60" />
                  Billing & Plan
                </button>
              </div>

              <div className="py-2">
                <button
                  onClick={signOut}
                  className="w-full text-left px-4 py-2 text-sm text-red-400 hover:bg-white/5 transition-colors"
                >
                  Log out
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
