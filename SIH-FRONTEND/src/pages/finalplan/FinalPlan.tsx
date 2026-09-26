import { useNavigate } from "react-router";
import { useVoyage } from "../../contexts/VoyageContext";
import { useApproval } from "../../contexts/ApprovalContext";
import { evaluateScenarios } from "../../utils/DecisionLogic";
import {
  CheckCircle2, PenLine, Anchor, Map,
  CalendarClock, AlertCircle, Clock, BarChart3,
  Info, AlertTriangle, FileText, RotateCcw
} from "lucide-react";

// ── helpers ──────────────────────────────────────────────────────────────────

function UnavailablePill() {
  return <span className="text-slate-400 italic text-xs">N/A - see note above</span>;
}

function PlanRow({ icon, label, value }: { icon: React.ReactNode; label: string; value: React.ReactNode }) {
  return (
    <div className="flex items-start gap-3 py-3 border-b border-slate-100 last:border-0">
      <div className="mt-0.5 text-blue-500 shrink-0">{icon}</div>
      <div className="flex-1 min-w-0 flex flex-col sm:flex-row sm:items-start sm:justify-between gap-1">
        <span className="text-sm text-slate-500 shrink-0">{label}</span>
        <span className="text-sm font-semibold text-slate-800 sm:text-right break-words">{value}</span>
      </div>
    </div>
  );
}

function StatusBadge({ status }: { status: "approved" | "modified" }) {
  if (status === "approved") {
    return (
      <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-50 border border-emerald-300 text-emerald-700 font-bold text-sm">
        <CheckCircle2 size={15} /> Approved
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-blue-50 border border-blue-300 text-blue-700 font-bold text-sm">
      <PenLine size={15} /> Modified by User
    </span>
  );
}

// ── component ─────────────────────────────────────────────────────────────────

export function FinalPlan() {
  const { requirements } = useVoyage();
  const { approvalResult, clearApproval } = useApproval();
  const navigate = useNavigate();

  const evaluations  = evaluateScenarios(requirements);
  
  // ── Guard — no approval state ────────────────────────────────────────────
  if (!approvalResult) {
    return (
      <div className="w-full relative">
        <main className="flex-1 flex items-center justify-center p-8 mt-12">
          <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-10 text-center max-w-md w-full space-y-4">
            <AlertCircle size={40} className="text-amber-500 mx-auto" />
            <h2 className="text-xl font-bold text-slate-900">No Approval Found</h2>
            <p className="text-sm text-slate-500">
              The Final Plan requires a completed human approval.
              Please return to the approval screen and submit your decision.
            </p>
            <button
              onClick={() => navigate("/human-approval")}
              className="bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 px-6 rounded-xl w-full transition-colors"
            >
              Return to Human Approval
            </button>
          </div>
        </main>
      </div>
    );
  }

  const { status, approvedAt, originalRecommendation, finalDecision } = approvalResult;
  const selectedEval = evaluations.find(e => e.scenario === finalDecision?.bestTime) || evaluations[0];
  const isModified = status === "modified";

  const vesselLabel = finalDecision.bestVessel !== "Unavailable"
    ? finalDecision.bestVessel["Vessel Type"] : null;
  const portLabel = finalDecision.bestPort !== "Unavailable"
    ? finalDecision.bestPort["Port"] : null;

  const approvedTime = (() => {
    try { return new Date(approvedAt).toLocaleString(); }
    catch { return approvedAt; }
  })();

  // ── Render ───────────────────────────────────────────────────────────────
  return (
    <div className="w-full relative flex flex-col min-h-full">
      <main className="flex-1 w-full max-w-7xl mx-auto p-6 md:p-8 space-y-8 relative z-10">

        {/* Title */}
        <div className="flex items-start justify-between gap-4 flex-wrap">
          <div>
            <h2 className="text-3xl font-bold text-slate-900 tracking-tight flex items-center gap-3">
              <FileText size={28} className="text-blue-600" />
              Final Plan
            </h2>
            <p className="text-slate-500 mt-2 text-base max-w-2xl">
              The consolidated decision output for this voyage, finalized through human approval.
            </p>
          </div>
          <StatusBadge status={status} />
        </div>

        {/* Modified warning banner */}
        {isModified && (
          <div className="flex items-start gap-3 bg-amber-50 border border-amber-200 rounded-xl p-5">
            <AlertTriangle size={18} className="text-amber-600 mt-0.5 shrink-0" />
            <div>
              <p className="text-sm font-semibold text-amber-900">Decision Modified by User</p>
              <p className="text-sm text-amber-800 mt-1">
                This plan reflects a human-modified decision. The original system recommendation was{" "}
                <strong>{originalRecommendation}</strong>.
                Modified selections may require revalidation of deadline feasibility before operational execution.
              </p>
            </div>
          </div>
        )}

        {/* ── TOP ROW: Recommendation + Approval ──────────────────────────── */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

          {/* Final Recommendation */}
          <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
            <div className="bg-slate-50 border-b border-slate-100 px-6 py-4">
              <h3 className="text-xs font-bold uppercase tracking-widest text-slate-400">Final Recommendation</h3>
            </div>
            <div className="px-6 py-6 space-y-4">
              <div className={`inline-flex items-center gap-2 px-5 py-3 rounded-xl font-black text-xl border-2 ${
                finalDecision.recommendation === "BOOK NOW"   ? "bg-emerald-50 border-emerald-400 text-emerald-700" :
                finalDecision.recommendation?.includes("WAIT")       ? "bg-amber-50 border-amber-400 text-amber-700" :
                finalDecision.recommendation === "CHANGE PLAN"? "bg-rose-50 border-rose-400 text-rose-700" :
                "bg-slate-100 border-slate-300 text-slate-600"
              }`}>
                {finalDecision.recommendation}
              </div>
              {isModified && originalRecommendation !== finalDecision.recommendation && (
                <p className="text-xs text-slate-500 flex items-start gap-1.5">
                  <Info size={12} className="mt-0.5 shrink-0" />
                  Original: <strong>{originalRecommendation}</strong>
                </p>
              )}
            </div>
          </div>

          {/* Approval metadata */}
          <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
            <div className="bg-slate-50 border-b border-slate-100 px-6 py-4">
              <h3 className="text-xs font-bold uppercase tracking-widest text-slate-400">Approval Record</h3>
            </div>
            <div className="px-6 py-2">
              <PlanRow icon={<CheckCircle2 size={15} />} label="Decision Status" value={<StatusBadge status={status} />} />
              <PlanRow icon={<Info size={15} />} label="Decision Source" value="Human Approval" />
              <PlanRow icon={<Clock size={15} />} label="Recorded At" value={approvedTime} />
            </div>
          </div>
        </div>

        {/* ── VOYAGE DETAILS ───────────────────────────────────────────────── */}
        <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
          <div className="bg-slate-50 border-b border-slate-100 px-6 py-4">
            <h3 className="text-xs font-bold uppercase tracking-widest text-slate-400">Voyage Details</h3>
          </div>
          <div className="px-6 py-2 grid grid-cols-1 sm:grid-cols-2 gap-x-12">
            <div>
              <PlanRow icon={<Map size={15} />} label="Origin"
                value={requirements?.origin || <UnavailablePill />} />
              <PlanRow icon={<Map size={15} />} label="Destination"
                value={requirements?.destination || <UnavailablePill />} />
              <PlanRow icon={<BarChart3 size={15} />} label="Commodity"
                value={requirements?.commodity || <UnavailablePill />} />
            </div>
            <div>
              <PlanRow icon={<BarChart3 size={15} />} label="Cargo Volume"
                value={requirements?.cargoMt ? `${Number(requirements.cargoMt).toLocaleString()} MT` : <UnavailablePill />} />
              <PlanRow icon={<Clock size={15} />} label="Delivery Date"
                value={requirements?.deliveryDate || <UnavailablePill />} />
              <PlanRow icon={<CalendarClock size={15} />} label="Laycan"
                value={requirements?.laycan || <UnavailablePill />} />
            </div>
          </div>
        </div>

        {/* ── FINAL DECISION ───────────────────────────────────────────────── */}
        <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
          <div className="bg-slate-50 border-b border-slate-100 px-6 py-4">
            <h3 className="text-xs font-bold uppercase tracking-widest text-slate-400">Final Decision</h3>
          </div>
          <div className="px-6 py-2">
            <PlanRow icon={<CalendarClock size={15} />} label="Best Time"
              value={finalDecision.bestTime === "Unavailable" ? <UnavailablePill /> : finalDecision.bestTime} />
            <PlanRow icon={<Anchor size={15} />} label="Best Vessel"
              value={vesselLabel ?? <UnavailablePill />} />
            <PlanRow icon={<Map size={15} />} label="Best Port"
              value={portLabel ?? <UnavailablePill />} />
          </div>
        </div>

        {/* ── DECISION CONTEXT ─────────────────────────────────────────────── */}
        <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
          <div className="bg-slate-50 border-b border-slate-100 px-6 py-4">
            <h3 className="text-xs font-bold uppercase tracking-widest text-slate-400">Decision Context</h3>
          </div>
          <div className="px-6 py-2">
            <PlanRow icon={<BarChart3 size={15} />} label={`Freight Cost (${finalDecision?.bestTime || "Selected"})`}
              value={
                selectedEval?.details.freightCost !== "Unavailable" && selectedEval?.details.freightCost !== undefined
                  ? `$${selectedEval.details.freightCost.toLocaleString()}`
                  : <UnavailablePill />
              } />
            <PlanRow icon={<AlertCircle size={15} />} label="Risk Score"
              value={selectedEval?.riskScore === "Unavailable" ? <UnavailablePill /> : String(selectedEval?.riskScore)} />
            <PlanRow icon={<Clock size={15} />} label="Deadline Buffer"
              value={selectedEval?.deadlineBuffer === "Unavailable" ? <UnavailablePill /> : `${selectedEval?.deadlineBuffer} days`} />
          </div>
        </div>

        {/* ── Vessel spec card (only if available) ─────────────────────────── */}
        {finalDecision.bestVessel !== "Unavailable" && (
          <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
            <div className="bg-slate-50 border-b border-slate-100 px-6 py-4 flex items-center gap-2">
              <Anchor size={16} className="text-amber-600" />
              <h3 className="text-xs font-bold uppercase tracking-widest text-slate-400">Vessel Specifications</h3>
            </div>
            
              {finalDecision.bestVessel === "Unavailable" && (
                <div className="px-6 py-4 bg-slate-50 border-y border-slate-100">
                  <p className="text-sm text-slate-700 font-medium">No feasible single-vessel plan exists for this cargo volume.</p>
                  <p className="text-xs text-slate-500 mt-1">
                    Multi-voyage planning required - approximately {Math.ceil(Number(requirements?.cargoMt || 0) / 170000)} voyages based on Capesize limits.
                  </p>
                </div>
              )}
              <div className="p-6 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
              {[
                ["DWT (mt)",        finalDecision.bestVessel["DWT (mt)"]],
                ["Draft (m)",       finalDecision.bestVessel["SSW Draft (m)"]],
                ["LOA (m)",         finalDecision.bestVessel["LOA (m)"]],
                ["Beam (m)",        finalDecision.bestVessel["Beam (m)"]],
                ["Grain Cap (cbm)", finalDecision.bestVessel["Grain Capacity (cbm)"]],
                ["Laden Spd (kn)",  finalDecision.bestVessel["Laden Speed (kn)"]],
                ["Ballast Spd (kn)",finalDecision.bestVessel["Ballast Speed (kn)"]],
                ["Max Age (yr)",    finalDecision.bestVessel["Max Age (yr)"]],
                ["Geared",          String(finalDecision.bestVessel["Geared"])],
              ].map(([label, val]) => (
                <div key={String(label)} className="bg-slate-50 border border-slate-100 rounded-lg px-3 py-2.5">
                  <span className="text-xs text-slate-400 block mb-0.5">{label}</span>
                  <span className="text-sm font-semibold text-slate-800">{val ?? "N/A"}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ── End of workflow message ───────────────────────────────────────── */}
        <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm flex flex-col md:flex-row items-center justify-between gap-6">
          <div>
            <h4 className="font-bold text-lg text-slate-900">Plan Finalized</h4>
            <p className="text-slate-500 text-sm max-w-lg mt-1">
              The voyage intelligence workflow is complete.
            </p>
          </div>
          <div className="flex flex-col sm:flex-row gap-3 w-full md:w-auto shrink-0">
            <button
              onClick={() => { clearApproval(); navigate("/human-approval"); }}
              className="inline-flex items-center justify-center gap-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold py-3 px-6 rounded-xl transition-colors whitespace-nowrap shadow-sm"
            >
              <RotateCcw size={18} />
              Modify
            </button>
            <button
              onClick={() => navigate("/voyage-receipt")}
              className="inline-flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-xl transition-colors whitespace-nowrap shadow-md"
            >
              <FileText size={18} />
              Generate Voyage Receipt
            </button>
          </div>
        </div>

      </main>
    </div>
  );
}
