/**
 * VoyageContextBar — Compact voyage summary shown on every processing step.
 * Shows real values from VoyageContext; falls back to "Not set".
 */
import type { VoyageRequirements } from "../../contexts/VoyageContext";
import { HugeiconsIcon } from "@hugeicons/react";
import { 
  Route01Icon, 
  DiamondIcon, 
  PackageIcon, 
  Calendar01Icon,
  Calendar02Icon
} from "@hugeicons/core-free-icons";

interface Props {
  requirements: VoyageRequirements | null;
}

export function VoyageContextBar({ requirements }: Props) {
  const route = requirements?.origin && requirements?.destination
    ? `${requirements.origin} → ${requirements.destination}`
    : "Not set";
  const commodity = requirements?.commodity || "Not set";
  const cargo = requirements?.cargoMt ? `${Number(requirements.cargoMt).toLocaleString()} MT` : "Not set";
  const delivery = requirements?.deliveryDate || "Not set";
  const laycan = requirements?.laycan || "Not set";

  return (
    <div className="bg-white border border-slate-200/80 rounded-2xl shadow-[0_2px_10px_-3px_rgba(6,81,237,0.05)] overflow-hidden transition-all duration-300 hover:shadow-md hover:border-slate-300/80">
      {/* Header section */}
      <div className="bg-slate-50/80 border-b border-slate-100 px-5 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="text-[11px] font-bold uppercase tracking-[0.2em] text-slate-500">
            Voyage Context
          </span>
          <span className="text-slate-300 hidden sm:inline">|</span>
          <span className="text-[11px] text-slate-400 font-medium hidden sm:inline">
            Current voyage under evaluation
          </span>
        </div>
        <div className="flex items-center gap-2">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          <span className="text-[10px] font-semibold uppercase tracking-wider text-slate-600">
            Current Voyage
          </span>
        </div>
      </div>

      {/* Main content grid */}
      <div className="p-5 flex flex-col lg:flex-row gap-6 lg:gap-8 items-start lg:items-center">
        
        {/* Route - Primary Field */}
        <div className="flex items-start gap-3 lg:flex-1">
          <div className="mt-0.5 text-blue-600 bg-blue-50 p-2 rounded-xl shrink-0 border border-blue-100/50">
            <HugeiconsIcon icon={Route01Icon} className="w-5 h-5" />
          </div>
          <div className="flex flex-col min-w-0 justify-center h-full pt-0.5">
            <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-1">Route</span>
            <span className="text-base font-semibold text-slate-900 truncate">{route}</span>
          </div>
        </div>

        {/* Separator - Hidden on mobile/tablet */}
        <div className="hidden lg:block w-px h-10 bg-slate-100 shrink-0" />

        {/* Info Grid for Mobile/Tablet, Inline for Desktop */}
        <div className="grid grid-cols-2 md:grid-cols-4 lg:flex lg:flex-row gap-6 lg:gap-8 w-full lg:w-auto">
          
          {/* Commodity */}
          <div className="flex items-start gap-3">
            <div className="mt-0.5 text-slate-400 shrink-0">
              <HugeiconsIcon icon={DiamondIcon} className="w-4 h-4 md:w-5 md:h-5" />
            </div>
            <div className="flex flex-col min-w-0 pt-1">
              <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-1">Commodity</span>
              <span className="text-sm font-medium text-slate-800 truncate">{commodity}</span>
            </div>
          </div>

          {/* Cargo */}
          <div className="flex items-start gap-3">
            <div className="mt-0.5 text-slate-400 shrink-0">
              <HugeiconsIcon icon={PackageIcon} className="w-4 h-4 md:w-5 md:h-5" />
            </div>
            <div className="flex flex-col min-w-0 pt-1">
              <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-1">Cargo</span>
              <span className="text-sm font-medium text-slate-800 truncate">{cargo}</span>
            </div>
          </div>

          {/* Delivery */}
          <div className="flex items-start gap-3">
            <div className="mt-0.5 text-slate-400 shrink-0">
              <HugeiconsIcon icon={Calendar01Icon} className="w-4 h-4 md:w-5 md:h-5" />
            </div>
            <div className="flex flex-col min-w-0 pt-1">
              <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-1">Delivery</span>
              <span className="text-sm font-medium text-slate-800 truncate">{delivery}</span>
            </div>
          </div>

          {/* Laycan */}
          <div className="flex items-start gap-3">
            <div className="mt-0.5 text-slate-400 shrink-0">
              <HugeiconsIcon icon={Calendar02Icon} className="w-4 h-4 md:w-5 md:h-5" />
            </div>
            <div className="flex flex-col min-w-0 pt-1">
              <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-1">Laycan</span>
              <span className="text-sm font-medium text-slate-800 truncate">{laycan}</span>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
