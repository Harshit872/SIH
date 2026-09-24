import { Outlet } from "react-router";
import { Ship } from "lucide-react";

export function AuthLayout() {
  return (
    <div className="min-h-screen relative flex items-center justify-center overflow-hidden font-sans bg-slate-900">
      
      {/* 1. Full-Screen Background Image */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <div 
          className="absolute inset-0"
          style={{
            backgroundImage: 'url("/auth-bg-new.jpg")',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            backgroundRepeat: 'no-repeat',
            // Image Treatment: subtle contrast enhancement
            filter: 'contrast(1.05) brightness(1.02)'
          }}
        />
        {/* Dark Navy Overlay for text readability and maritime tone */}
        <div className="absolute inset-0 bg-[#020817]/40 mix-blend-multiply" />
        {/* Gradient for left-side text readability on desktop */}
        <div className="absolute inset-0 bg-gradient-to-r from-[#020817]/80 via-[#020817]/30 to-transparent hidden lg:block" />
        {/* Gradient for mobile text readability */}
        <div className="absolute inset-0 bg-gradient-to-b from-[#020817]/60 via-transparent to-[#020817]/80 lg:hidden" />
      </div>

      {/* 2. Page Content Container */}
      <div className="relative z-10 w-full max-w-[1440px] mx-auto min-h-screen flex flex-col lg:flex-row p-6 sm:p-12">
        
        {/* Left Side: Branding and Messaging */}
        <div className="flex-1 flex flex-col justify-between pt-4 pb-8 lg:pb-4 lg:pr-12 text-white">
          
          {/* Branding (Top Left) */}
          <div className="flex items-center gap-3 font-semibold tracking-tight drop-shadow-md">
            <div className="h-12 w-12 bg-white/10 backdrop-blur-md rounded-xl flex items-center justify-center border border-white/20 shadow-lg">
              <Ship size={24} className="text-white" />
            </div>
            <div className="flex flex-col">
              <span className="text-3xl leading-none font-bold">Odyssey</span>
              <span className="text-[11px] uppercase tracking-[0.25em] text-white/80 mt-1">Maritime Intelligence</span>
            </div>
          </div>

          {/* Messaging (Bottom Left) */}
          <div className="hidden lg:block max-w-xl mt-auto">
            <h1 className="text-4xl font-bold tracking-tight mb-4 drop-shadow-lg leading-tight">
              Advanced Shipping Intelligence
            </h1>
            <p className="text-white/90 text-lg leading-relaxed mb-8 drop-shadow-md">
              Access enterprise-grade maritime forecasting, charter optimization, and feasibility analytics in one unified platform.
            </p>
            
            <div className="flex items-center gap-4 text-sm font-medium text-white/70 drop-shadow-sm">
              <span>© 2026 Odyssey Maritime</span>
              <span className="w-1 h-1 bg-white/30 rounded-full" />
              <span>Enterprise Portal</span>
            </div>
          </div>
        </div>

        {/* Right Side: Floating Auth Card */}
        <div className="flex flex-col items-center justify-center lg:items-end w-full lg:w-auto mt-6 lg:mt-0">
          <div className="w-full max-w-[440px] bg-white rounded-2xl shadow-2xl p-8 sm:p-10 border border-slate-100 relative animate-in fade-in slide-in-from-bottom-8 duration-700">
            <Outlet />
          </div>
          
          {/* Mobile Messaging / Footer */}
          <div className="lg:hidden mt-12 text-center text-white">
            <h1 className="text-2xl font-bold mb-3 drop-shadow-md">Advanced Shipping Intelligence</h1>
            <p className="text-white/80 text-sm mb-6 drop-shadow-sm px-4">
              Enterprise-grade maritime forecasting and charter optimization.
            </p>
            <p className="text-xs text-white/60">© 2026 Odyssey Maritime</p>
          </div>
        </div>

      </div>
    </div>
  );
}
