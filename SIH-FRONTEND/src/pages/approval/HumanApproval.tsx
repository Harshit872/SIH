import { useState } from "react";
import { demoMocks } from "../../utils/demoMocks";
import { useNavigate } from "react-router";
import { useVoyage } from "../../contexts/VoyageContext";
import { useApproval, type FinalDecision } from "../../contexts/ApprovalContext";
import {
  evaluateScenarios,
  runDecisionEngine,
  generateFinalRecommendation,
  type ScenarioType,
  type FinalRecommendationType,
} from "../../utils/DecisionLogic";
import { DatasetService } from "../../data/DatasetService";
import {
  CheckCircle2, PenLine, Clock, AlertTriangle,
  Anchor, Map, CalendarClock, AlertCircle, Info,
  ChevronDown, BarChart3, RefreshCw
} from "lucide-react";

// ── helpers ─────────────────────────────────────────────────────────────────

function UnavailablePill() {
  return <span className="text-slate-400 italic text-xs">N/A - see note above</span>;
}

function SummaryRow({ icon, label, value }: { icon: React.ReactNode; label: string; value: React.ReactNode }) {
  return (
    <div className="flex items-start gap-3 py-3 border-b border-slate-100 last:border-0">
      <div className="mt-0.5 text-blue-500 shrink-0">{icon}</div>
      <div className="flex-1 min-w-0 flex items-start justify-between gap-2">
        <span className="text-sm text-slate-500 shrink-0">{label}</span>
        <span className="text-sm font-semibold text-slate-800 text-right break-words">{value}</span>
      </div>
    </div>
  );
}

function RecTag({ rec }: { rec: FinalRecommendationType }) {
  if (rec === "BOOK NOW") return (
    <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-50 border border-emerald-300 text-emerald-700 font-bold text-sm">
      <CheckCircle2 size={15} /> BOOK NOW
    </span>
  );
  if (rec === "WAIT") return (
    <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-amber-50 border border-amber-300 text-amber-700 font-bold text-sm">
      <Clock size={15} /> WAIT
    </span>
  );
  if (rec === "CHANGE PLAN") return (
    <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-rose-50 border border-rose-300 text-rose-700 font-bold text-sm">
      <AlertTriangle size={15} /> CHANGE PLAN
    </span>
  );
  return (
    <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-100 border border-slate-300 text-slate-600 font-bold text-sm">
      <RefreshCw size={15} /> Unavailable
    </span>
  );
}

// ── component ────────────────────────────────────────────────────────────────

export function HumanApproval() {
  const { requirements, markStepComplete } = useVoyage();
  const reqSeed = `${requirements?.origin}-${requirements?.destination}-${requirements?.cargoMt}`;
  const { setApprovalResult } = useApproval();
  const navigate = useNavigate();

  // ── Derive upstream results ──────────────────────────────────────────────
  const evaluations = evaluateScenarios(requirements);
  const decision    = runDecisionEngine(evaluations, requirements);
  const finalRec    = generateFinalRecommendation(evaluations, decision);
  const selectedEval = evaluations.find(e => e.scenario === decision?.bestTime) || evaluations[0];

  // ── Local UI state ───────────────────────────────────────────────────────
  const [mode, setMode] = useState<"idle" | "approving" | "modifying" | "approved">("idle");

  // Modify fields — start with current decision values
  const [modTime, setModTime] = useState<ScenarioType | "Unavailable">(decision?.bestTime);
  const [modVessel, setModVessel] = useState<any | "Unavailable">(decision.bestVessel);
  const [modPort, setModPort] = useState<any | "Unavailable">(decision.bestPort);
  const [modRec, setModRec] = useState<FinalRecommendationType>(finalRec.recommendation);
  const [modWarning, setModWarning] = useState<string | null>(null);

  const allVessels = DatasetService.getVessels();
  const allPorts   = DatasetService.getPorts().map(p => p.Port).filter((v, i, a) => a.indexOf(v) === i);

  // ── Handlers ─────────────────────────────────────────────────────────────

  function handleApprove() {
    const result = {
      status: "approved" as const,
      approvedAt: new Date().toISOString(),
      originalRecommendation: finalRec.recommendation,
      finalDecision: {
        bestTime: decision?.bestTime,
        bestVessel: decision.bestVessel,
        bestPort: decision.bestPort,
        recommendation: finalRec.recommendation,
      } satisfies FinalDecision,
    };
    setApprovalResult(result);
    setMode("approved");
    markStepComplete('/human-approval');
    // Navigate after brief feedback
    setTimeout(() => navigate("/final-plan"), 1200);
  }

  function handleModifySave() {
    // Warn if time was changed
    let warning: string | null = null;
    if (modTime !== decision?.bestTime && modTime !== "Unavailable") {
      warning = `Modified time (${modTime}) requires revalidation before finalization — deadline feasibility may change.`;
    }
    setModWarning(warning);

    const result = {
      status: "modified" as const,
      approvedAt: new Date().toISOString(),
      originalRecommendation: finalRec.recommendation,
      finalDecision: {
        bestTime: modTime,
        bestVessel: modVessel,
        bestPort: modPort,
        recommendation: modRec,
      } satisfies FinalDecision,
    };
    setApprovalResult(result);
    setMode("approved");
    markStepComplete('/human-approval');
    setTimeout(() => navigate("/final-plan"), 1500);
  }

  // ── Approved feedback state ──────────────────────────────────────────────
  if (mode === "approved") {
    return (
      <div className="min-h-screen bg-[#f8fafc] flex items-center justify-center p-6">
        <div className="bg-white rounded-2xl border border-emerald-200 shadow-lg p-10 text-center max-w-md w-full">
          <div className="flex justify-center mb-4">
            <div className="h-16 w-16 bg-emerald-50 border-2 border-emerald-300 rounded-full flex items-center justify-center">
              <CheckCircle2 size={32} className="text-emerald-600" />
            </div>
          </div>
          <h2 className="text-xl font-bold text-slate-900 mb-2">Decision Recorded</h2>
          <p className="text-slate-500 text-sm">Redirecting to Final Plan…</p>
        </div>
      </div>
    );
  }

  // ── Main render ──────────────────────────────────────────────────────────
  return (
    <div className="w-full relative flex flex-col min-h-full">
      <main className="flex-1 w-full max-w-7xl mx-auto p-6 md:p-8 space-y-8 relative z-10">
        
        {/* Page title */}
        <div>
          <h2 className="text-3xl font-bold text-slate-900 tracking-tight">Human Approval</h2>
          <p className="text-slate-500 mt-2 text-base max-w-2xl">
            Review the system recommendation before creating the final plan. You must explicitly approve or modify.
          </p>
        </div>

        {/* CURRENT RECOMMENDATION */}
        <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
          <div className="bg-slate-50 border-b border-slate-100 px-8 py-4 flex items-center justify-between">
            <h3 className="text-sm font-bold uppercase tracking-widest text-slate-700">Current Recommendation</h3>
          </div>
          <div className="px-8 py-6 space-y-4">
                          <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-50 border border-emerald-300 text-emerald-700 font-bold text-sm">
                <CheckCircle2 size={15} /> {decision?.bestTime === "Unavailable" ? "Unavailable" : `${decision?.bestTime} - ${decision?.bestVessel?.["Vessel Type"] || "Vessel"} via ${decision?.bestPort?.["Port"] || "Port"}`}
              </span>
            <div className="bg-slate-50 border border-slate-100 rounded-xl p-4 flex gap-3">
              <Info size={16} className="text-slate-400 mt-0.5 shrink-0" />
              <p className="text-sm text-slate-700 leading-relaxed">{finalRec.reason}</p>
            </div>
          </div>
        </div>

        {/* DECISION SUMMARY */}
        <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
          <div className="bg-slate-50 border-b border-slate-100 px-8 py-4">
            <h3 className="text-sm font-bold uppercase tracking-widest text-slate-700">Decision Details</h3>
          </div>
          <div className="px-8 py-2 grid grid-cols-1 md:grid-cols-2 gap-x-12 divide-y md:divide-y-0">
            <div className="divide-y divide-slate-100">
              <SummaryRow icon={<CalendarClock size={15} />} label="Best Time"
                value={decision?.bestTime === "Unavailable" ? <UnavailablePill /> : decision?.bestTime} />
              <SummaryRow icon={<Anchor size={15} />} label="Best Vessel"
                value={decision?.bestVessel !== "Unavailable" ? decision?.bestVessel?.["Vessel Type"] : <UnavailablePill />} />
              <SummaryRow icon={<Map size={15} />} label="Best Port"
                value={decision?.bestPort !== "Unavailable" ? decision?.bestPort?.["Port"] : <UnavailablePill />} />
            </div>
            <div className="divide-y divide-slate-100">
              <SummaryRow icon={<AlertCircle size={15} />} label="Risk Score"
                value={selectedEval?.riskScore === "Unavailable" ? <UnavailablePill /> : String(selectedEval?.riskScore)} />
              <SummaryRow icon={<Clock size={15} />} label="Deadline Buffer"
                value={selectedEval?.deadlineBuffer === "Unavailable" ? <UnavailablePill /> : `${selectedEval?.deadlineBuffer} days`} />
              <SummaryRow icon={<BarChart3 size={15} />} label={`Freight Cost (${decision?.bestTime || "Selected"})`}
                value={selectedEval?.details.freightCost !== "Unavailable" && selectedEval?.details.freightCost !== undefined
                  ? `$${selectedEval.details.freightCost.toLocaleString()}`
                  : <UnavailablePill />} />
            </div>
          </div>
        </div>

        {/* ── APPROVAL ACTIONS ─────────────────────────────────────────────── */}
        {mode === "idle" && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <button
              onClick={() => setMode("approving")}
              className="flex items-center justify-center gap-3 bg-emerald-600 hover:bg-emerald-500 active:bg-emerald-700 text-white font-bold text-base rounded-xl px-8 py-5 shadow-md transition-colors focus:outline-none focus:ring-4 focus:ring-emerald-400/50"
              aria-label="Approve the system recommendation"
            >
              <CheckCircle2 size={22} />
              Approve Recommendation
            </button>
            <button
              onClick={() => setMode("modifying")}
              className="flex items-center justify-center gap-3 bg-white hover:bg-slate-50 active:bg-slate-100 text-slate-800 font-bold text-base rounded-xl px-8 py-5 border-2 border-slate-300 shadow-sm transition-colors focus:outline-none focus:ring-4 focus:ring-slate-300/50"
              aria-label="Modify the system recommendation"
            >
              <PenLine size={22} />
              Modify Decision
            </button>
          </div>
        )}

        {/* ── APPROVE CONFIRM ──────────────────────────────────────────────── */}
        {mode === "approving" && (
          <div className="bg-emerald-50 border-2 border-emerald-300 rounded-2xl p-8 space-y-6">
            <div className="flex items-start gap-4">
              <div className="p-3 bg-emerald-100 rounded-xl text-emerald-600 shrink-0">
                <CheckCircle2 size={28} />
              </div>
              <div>
                <h3 className="text-lg font-bold text-emerald-900">Confirm Approval</h3>
                <p className="text-sm text-emerald-800 mt-1 leading-relaxed">
                  You are about to approve the system recommendation as the final decision.
                  This will lock in the current Best Time, Best Vessel, and Best Port.
                </p>
              </div>
            </div>
            <div className="flex flex-col sm:flex-row gap-3">
              <button
                onClick={handleApprove}
                className="flex-1 bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3 rounded-xl transition-colors focus:outline-none focus:ring-4 focus:ring-emerald-400/50"
              >
                Confirm Approval
              </button>
              <button
                onClick={() => setMode("idle")}
                className="flex-1 bg-white border border-slate-300 text-slate-700 font-semibold py-3 rounded-xl transition-colors hover:bg-slate-50 focus:outline-none focus:ring-4 focus:ring-slate-300/50"
              >
                Cancel
              </button>
            </div>
          </div>
        )}

        {/* ── MODIFY PANEL ─────────────────────────────────────────────────── */}
        {mode === "modifying" && (
          <div className="bg-white border-2 border-blue-200 rounded-2xl overflow-hidden shadow-sm">
            <div className="bg-blue-50 border-b border-blue-100 px-8 py-4 flex items-center gap-3">
              <PenLine size={18} className="text-blue-600" />
              <div>
                <h3 className="text-base font-bold text-slate-900">Modify Decision</h3>
                <p className="text-xs text-slate-500 mt-0.5">
                  Adjust the decision fields below. Only fields supported by the existing architecture and dataset are shown.
                </p>
              </div>
            </div>

            <div className="p-8 space-y-6">

              {/* Recommendation override */}
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2" htmlFor="mod-rec">
                  Final Recommendation
                </label>
                <div className="relative">
                  <select
                    id="mod-rec"
                    value={modRec}
                    onChange={e => setModRec(e.target.value as FinalRecommendationType)}
                    className="w-full appearance-none bg-slate-50 border border-slate-200 rounded-lg px-4 py-3 text-sm font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-400 pr-10"
                  >
                    <option value="BOOK NOW">BOOK NOW</option>
                    <option value="WAIT">WAIT</option>
                    <option value="CHANGE PLAN">CHANGE PLAN</option>
                    <option value="Recommendation Unavailable">Recommendation Unavailable</option>
                  </select>
                  <ChevronDown size={16} className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-slate-400" />
                </div>
              </div>

              {/* Best Time override */}
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2" htmlFor="mod-time">
                  Best Time
                </label>
                <div className="relative">
                  <select
                    id="mod-time"
                    value={modTime}
                    onChange={e => setModTime(e.target.value as ScenarioType | "Unavailable")}
                    className="w-full appearance-none bg-slate-50 border border-slate-200 rounded-lg px-4 py-3 text-sm font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-400 pr-10"
                  >
                    <option value="BOOK NOW">BOOK NOW</option>
                    <option value="WAIT 7D">WAIT 7D</option>
                    <option value="WAIT 14D">WAIT 14D</option>
                    <option value="Unavailable">Unavailable</option>
                  </select>
                  <ChevronDown size={16} className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-slate-400" />
                </div>
              </div>

              {/* Best Vessel override */}
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2" htmlFor="mod-vessel">
                  Best Vessel (from dataset)
                </label>
                <div className="relative">
                  <select
                    id="mod-vessel"
                    value={modVessel !== "Unavailable" ? modVessel["Vessel Type"] : "__unavailable__"}
                    onChange={e => {
                      if (e.target.value === "__unavailable__") { setModVessel("Unavailable"); return; }
                      const found = allVessels.find(v => v["Vessel Type"] === e.target.value);
                      setModVessel(found ?? "Unavailable");
                    }}
                    className="w-full appearance-none bg-slate-50 border border-slate-200 rounded-lg px-4 py-3 text-sm font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-400 pr-10"
                  >
                    <option value="__unavailable__">— Unavailable —</option>
                    {allVessels.map(v => (
                      <option key={v["Vessel Type"]} value={v["Vessel Type"]}>{v["Vessel Type"]}</option>
                    ))}
                  </select>
                  <ChevronDown size={16} className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-slate-400" />
                </div>
              </div>

              {/* Best Port override */}
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2" htmlFor="mod-port">
                  Best Port (from dataset)
                </label>
                <div className="relative">
                  <select
                    id="mod-port"
                    value={modPort !== "Unavailable" ? modPort["Port"] : "__unavailable__"}
                    onChange={e => {
                      if (e.target.value === "__unavailable__") { setModPort("Unavailable"); return; }
                      const found = DatasetService.getPorts().find(p => p.Port === e.target.value);
                      setModPort(found ?? "Unavailable");
                    }}
                    className="w-full appearance-none bg-slate-50 border border-slate-200 rounded-lg px-4 py-3 text-sm font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-400 pr-10"
                  >
                    <option value="__unavailable__">— Unavailable —</option>
                    {allPorts.map(p => (
                      <option key={p} value={p}>{p}</option>
                    ))}
                  </select>
                  <ChevronDown size={16} className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-slate-400" />
                </div>
              </div>

              {/* Warning if applicable */}
              {modWarning && (
                <div className="flex items-start gap-3 bg-amber-50 border border-amber-200 rounded-xl p-4">
                  <AlertTriangle size={16} className="text-amber-600 mt-0.5 shrink-0" />
                  <p className="text-sm text-amber-800">{modWarning}</p>
                </div>
              )}

              <div className="bg-blue-50 border border-blue-100 rounded-xl p-4 flex gap-3">
                <Info size={15} className="text-blue-500 mt-0.5 shrink-0" />
                <p className="text-xs text-blue-700 leading-relaxed">
                  Only vessels and ports present in the integrated dataset are available. Selecting a different time scenario may affect deadline feasibility — the system will flag this on the Final Plan.
                </p>
              </div>

              <div className="flex flex-col sm:flex-row gap-3 pt-2">
                <button
                  onClick={handleModifySave}
                  className="flex-1 bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 rounded-xl transition-colors focus:outline-none focus:ring-4 focus:ring-blue-400/50"
                >
                  Save Modified Decision
                </button>
                <button
                  onClick={() => setMode("idle")}
                  className="flex-1 bg-white border border-slate-300 text-slate-700 font-semibold py-3 rounded-xl hover:bg-slate-50 transition-colors focus:outline-none focus:ring-4 focus:ring-slate-300/50"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}

      </main>
    </div>
  );
}
