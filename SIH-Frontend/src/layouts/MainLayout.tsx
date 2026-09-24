import { useState, useEffect } from "react";
import { Outlet, Link, useLocation, useNavigate } from "react-router";
import { 
  Ship, Navigation, LineChart, Target, ShieldCheck, 
  CheckCircle, FileText, Menu, Pencil, Settings, User, LogOut, Lock
} from "lucide-react";
import { useVoyage } from "../contexts/VoyageContext";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "../components/ui/dropdown-menu";

// Example avatar
const AVATAR_INITIALS = "HS";
const USER_NAME = "Harshit Sachan";
const USER_EMAIL = "harshit@odyssey.app";

const NAV_ITEMS = [
  { path: "/voyage-requirement-input", label: "Voyage Details", icon: Navigation },
  { path: "/freight-forecasting", label: "Market Outlook", icon: LineChart },
  { path: "/decision-workspace", label: "Decision Workspace", icon: Target },
  { path: "/final-recommendation", label: "Recommendation", icon: ShieldCheck },
  { path: "/human-approval", label: "Approval", icon: CheckCircle },
  { path: "/final-plan", label: "Final Voyage Plan", icon: FileText },
];

function Sidebar({ location, handleEditVoyage, setIsMobileOpen }: { location: any; handleEditVoyage: () => void; setIsMobileOpen: (open: boolean) => void }) {
  const { completedSteps } = useVoyage();

  return (
    <div className="flex flex-col h-full bg-[#0b1b36] border-r border-[#1a2b4a]">
      <div className="p-6 border-b border-[#1a2b4a] flex items-center gap-3">
        <div className="h-10 w-10 bg-blue-600 rounded-lg flex items-center justify-center shrink-0 shadow-sm shadow-blue-900/50">
          <Ship size={24} className="text-white" />
        </div>
        <div className="overflow-hidden">
          <h1 className="text-lg font-bold tracking-tight text-white truncate">Odyssey</h1>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto py-6 px-4">
        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-4 px-2">Your Voyage</h3>
        <nav className="space-y-1.5">
          {NAV_ITEMS.map((item, index) => {
            const isActive = location.pathname === item.path;
            const isCompleted = completedSteps.includes(item.path);
            
            let isLocked = false;
            if (index > 0) {
              const prevPath = NAV_ITEMS[index - 1].path;
              isLocked = !completedSteps.includes(prevPath);
            }

            const Icon = item.icon;
            
            if (isLocked) {
              return (
                <div 
                  key={item.path} 
                  className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-slate-600 font-medium text-sm cursor-not-allowed select-none"
                >
                  <Lock size={16} className="text-slate-700" />
                  {item.label}
                </div>
              );
            }

            return (
              <Link 
                key={item.path} 
                to={item.path}
                onClick={() => setIsMobileOpen(false)}
                className={`
                  flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors font-medium text-sm
                  ${isActive 
                    ? "bg-blue-600/20 text-blue-400 font-semibold border border-blue-500/20" 
                    : "text-slate-400 hover:bg-slate-800/50 hover:text-white border border-transparent"
                  }
                `}
              >
                {isCompleted && !isActive ? (
                  <CheckCircle size={18} className="text-emerald-500" />
                ) : (
                  <Icon size={18} className={isActive ? "text-blue-400" : "text-slate-500"} />
                )}
                {item.label}
              </Link>
            );
          })}
        </nav>

        <div className="mt-8 pt-6 border-t border-[#1a2b4a]">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-4 px-2">Action</h3>
          <button 
            onClick={handleEditVoyage}
            className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-slate-400 hover:bg-slate-800/50 hover:text-white transition-colors font-medium text-sm text-left border border-transparent"
          >
            <Pencil size={18} className="text-slate-500" />
            Edit Voyage
          </button>
        </div>
      </div>

      <div className="p-4 border-t border-[#1a2b4a]">
        <Link 
          to="/settings"
          onClick={() => setIsMobileOpen(false)}
          className="flex items-center gap-3 px-3 py-2 rounded-lg text-slate-400 hover:bg-slate-800/50 hover:text-white transition-colors font-medium text-sm border border-transparent"
        >
          <Settings size={18} className="text-slate-500" />
          Settings
        </Link>
      </div>
    </div>
  );
}

export function MainLayout() {
  const { requirements, completedSteps } = useVoyage();
  const location = useLocation();
  const navigate = useNavigate();
  const [isMobileOpen, setIsMobileOpen] = useState(false);

  // Derive contextual summary string
  const voyageSummary = requirements?.origin && requirements?.destination 
    ? `${requirements.origin} → ${requirements.destination}` 
    : "No Voyage Defined";
  
  const secondarySummary = requirements?.cargoMt && requirements?.commodity
    ? `${requirements.cargoMt.toLocaleString()} MT • ${requirements.commodity}`
    : "";

  const handleEditVoyage = () => {
    setIsMobileOpen(false);
    navigate("/voyage-requirement-input");
  };

  const handleLogout = () => {
    navigate("/login");
  };


  // Enforce Navigation Locking
  useEffect(() => {
    const currentIndex = NAV_ITEMS.findIndex(item => item.path === location.pathname);
    if (currentIndex > 0) {
      const prevPath = NAV_ITEMS[currentIndex - 1].path;
      if (!completedSteps.includes(prevPath)) {
        // Find last completed
        let redirectPath = NAV_ITEMS[0].path;
        for (let i = NAV_ITEMS.length - 1; i >= 0; i--) {
          if (completedSteps.includes(NAV_ITEMS[i].path)) {
            redirectPath = NAV_ITEMS[i].path;
            break;
          }
        }
        navigate(redirectPath, { replace: true });
      }
    }
  }, [location.pathname, completedSteps, navigate]);

  return (
    <div className="flex w-full h-screen bg-[#f8fafc] font-sans overflow-hidden">
      
      {/* Desktop Sidebar */}
      <aside className="hidden md:block w-64 lg:w-72 h-full z-20 shrink-0 print:hidden">
        <Sidebar location={location} handleEditVoyage={handleEditVoyage} setIsMobileOpen={setIsMobileOpen} />
      </aside>

      {/* Mobile Drawer Overlay */}
      {isMobileOpen && (
        <div className="fixed inset-0 bg-slate-900/50 z-40 md:hidden backdrop-blur-sm print:hidden" onClick={() => setIsMobileOpen(false)} />
      )}

      {/* Mobile Sidebar */}
      <div className={`fixed inset-y-0 left-0 w-64 bg-white z-50 transform transition-transform duration-300 ease-in-out md:hidden print:hidden ${isMobileOpen ? "translate-x-0" : "-translate-x-full"}`}>
        <Sidebar location={location} handleEditVoyage={handleEditVoyage} setIsMobileOpen={setIsMobileOpen} />
      </div>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 h-full relative z-10 print:h-auto print:overflow-visible">
        
        {/* Topbar */}
        <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-4 sm:px-6 z-40 shrink-0 relative print:hidden">
          <div className="flex items-center gap-4">
            <button 
              onClick={() => setIsMobileOpen(true)}
              className="p-2 -ml-2 rounded-lg text-slate-500 hover:bg-slate-100 md:hidden"
            >
              <Menu size={24} />
            </button>
            
            <div className="hidden sm:flex flex-col">
              <span className="text-sm font-bold text-slate-900 truncate max-w-[300px] lg:max-w-[500px]">
                {voyageSummary}
              </span>
              {secondarySummary && (
                <span className="text-xs text-slate-500 font-medium truncate max-w-[300px] lg:max-w-[500px]">
                  {secondarySummary}
                </span>
              )}
            </div>
          </div>

          <div className="flex items-center gap-4 relative">
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <button 
                  className="h-9 w-9 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center font-bold text-sm shadow-sm hover:ring-2 hover:ring-blue-200 hover:ring-offset-2 transition-all focus:outline-none"
                >
                  {AVATAR_INITIALS}
                </button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-56 z-50">
                <DropdownMenuLabel className="font-normal">
                  <div className="flex flex-col space-y-1">
                    <p className="text-sm font-medium leading-none">{USER_NAME}</p>
                    <p className="text-xs leading-none text-slate-500">
                      {USER_EMAIL}
                    </p>
                  </div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem asChild>
                  <Link to="/settings" className="cursor-pointer flex items-center">
                    <User className="mr-2 h-4 w-4" />
                    <span>Profile & Settings</span>
                  </Link>
                </DropdownMenuItem>
                <DropdownMenuItem className="cursor-pointer flex items-center">
                  <div className="mr-2 h-4 w-4 flex items-center justify-center text-slate-400 text-xs font-bold">?</div>
                  <span>Help & Support</span>
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={handleLogout} className="cursor-pointer flex items-center text-rose-600 focus:text-rose-600 focus:bg-rose-50">
                  <LogOut className="mr-2 h-4 w-4" />
                  <span>Sign out</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </header>

        {/* Scrollable Main Content */}
        <main className="flex-1 overflow-y-auto overflow-x-hidden relative z-0 print:overflow-visible">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
