import { Outlet } from "react-router-dom";
import { Header } from "./Header";
import { CommandPalette } from "./CommandPalette";

export function AppLayout() {
  return (
    <div className="flex flex-col h-screen overflow-hidden bg-background text-foreground p-4 md:p-6">
      <CommandPalette />
      <div className="flex-1 flex flex-col min-w-0 bg-[#151515] rounded-[2rem] border border-white/5 shadow-2xl overflow-hidden relative">
        <Header />
        <main className="flex-1 overflow-y-auto relative">
          <div className="h-full relative w-full max-w-[1400px] mx-auto p-6 md:p-10">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
