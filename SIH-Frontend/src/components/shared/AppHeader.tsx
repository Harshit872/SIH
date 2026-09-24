/**
 * AppHeader — Shared header for all workflow pages (Steps 3–15).
 * Provides a consistent Odyssey nav bar with the current stage label.
 */
import { Ship } from "lucide-react";

const STEPS = [
  { path: "/voyage-requirement-input", label: "Voyage Input",         step: "3"  },
  { path: "/preparing-intelligence",   label: "Preparing Intelligence", step: "4-5"},
  { path: "/freight-forecasting",      label: "Freight Forecasting",  step: "6"  },
  { path: "/decision-workspace",       label: "Decision Workspace",   step: "7-11"},
  { path: "/final-recommendation",     label: "Final Recommendation", step: "12" },
  { path: "/decision-dashboard",       label: "Decision Dashboard",   step: "13" },
  { path: "/human-approval",           label: "Human Approval",       step: "14" },
  { path: "/final-plan",               label: "Final Plan",           step: "15" },
] as const;

interface Props {
  currentPath: string;
}

export function AppHeader({ currentPath }: Props) {
  const current = STEPS.find(s => s.path === currentPath);

  return (
    <header className="bg-slate-900 text-white py-4 px-6 md:px-8 shadow-md relative z-10">
      <div className="max-w-[1440px] mx-auto flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 bg-blue-600 rounded-lg flex items-center justify-center">
            <Ship size={24} aria-hidden="true" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight">Odyssey</h1>
            <p className="text-[10px] text-white/70 uppercase font-medium tracking-widest">
              Smart Shipping Intelligence
            </p>
          </div>
        </div>
        {current && (
          <div className="hidden md:flex flex-col items-end">
            <span className="text-xs text-white/50 uppercase tracking-wider font-semibold">
              Step {current.step} of 15
            </span>
            <span className="text-sm font-semibold text-blue-400">{current.label}</span>
          </div>
        )}
      </div>
    </header>
  );
}
