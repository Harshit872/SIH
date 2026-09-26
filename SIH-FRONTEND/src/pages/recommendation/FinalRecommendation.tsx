import { useVoyage } from "../../contexts/VoyageContext";
import { evaluateScenarios, runDecisionEngine, generateFinalRecommendation } from "../../utils/DecisionLogic";
import type { FinalRecommendationType } from "../../utils/DecisionLogic";

import { useNavigate } from "react-router";
import {
  CheckCircle2, Clock, AlertTriangle,
  RefreshCw, Info, Anchor, Map, CalendarClock, BarChart3
} from "lucide-react";
import { Button } from "../../components/ui/button";


function RecommendationBadge({ rec }: { rec: FinalRecommendationType }) {
  if (rec === "BOOK NOW") {
    return (
      <div className="inline-flex items-center gap-3 px-6 py-3 bg-emerald-50 border-2 border-emerald-400 rounded-xl">
        <CheckCircle2 size={28} className="text-emerald-600" aria-hidden="true" />
        <span className="text-2xl font-black text-emerald-700 tracking-tight">BOOK NOW</span>
      </div>
    );
  }
  if (rec?.includes("WAIT")) {
    return (
      <div className="inline-flex items-center gap-3 px-6 py-3 bg-amber-50 border-2 border-amber-400 rounded-xl">
        <Clock size={28} className="text-amber-600" aria-hidden="true" />
        <span className="text-2xl font-black text-amber-700 tracking-tight">{rec}</span>
      </div>
    );
  }
  if (rec === "CHANGE PLAN") {
    return (
      <div className="inline-flex items-center gap-3 px-6 py-3 bg-rose-50 border-2 border-rose-400 rounded-xl">
        <AlertTriangle size={28} className="text-rose-600" aria-hidden="true" />
        <span className="text-2xl font-black text-rose-700 tracking-tight">CHANGE PLAN</span>
      </div>
    );
  }
  return (
    <div className="inline-flex items-center gap-3 px-6 py-3 bg-slate-100 border-2 border-slate-300 rounded-xl">
      <RefreshCw size={28} className="text-slate-500" aria-hidden="true" />
      <span className="text-2xl font-black text-slate-600 tracking-tight">Recommendation Unavailable</span>
    </div>
  );
}

function ContextRow({ label, value, icon }: { label: string; value: string; icon: React.ReactNode }) {
  return (
    <div className="flex items-start gap-3 py-3 border-b border-slate-100 last:border-0">
      <div className="mt-0.5 shrink-0 text-blue-500">{icon}</div>
      <div className="min-w-0">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-400 block mb-0.5">{label}</span>
        <span className="text-sm font-medium text-slate-800 break-words">{value}</span>
      </div>
    </div>
  );
}

export function FinalRecommendation() {
  const { requirements, markStepComplete } = useVoyage();
  const navigate = useNavigate();


  const evaluations = evaluateScenarios(requirements);
  const decision = runDecisionEngine(evaluations, requirements);
  const finalRec = generateFinalRecommendation(evaluations, decision);
  const isLoading = false;
  
  const selectedEval = evaluations.find(e => e.scenario === decision?.bestTime) || evaluations[0];


  return (
    <div className="w-full relative flex flex-col min-h-full">
      <main className="flex-1 w-full max-w-7xl mx-auto p-6 md:p-8 space-y-8 relative z-10">
        
        {/* Page title */}
        <div>
          <h2 className="text-3xl font-bold text-slate-900 tracking-tight">Your Recommendation</h2>
          <p className="text-slate-500 mt-2 text-lg max-w-2xl">
            The calculated best course of action based on current market conditions, vessel availability, and your delivery timeline.
          </p>
        </div>

        {/* Recommendation hero card */}
        <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
          <div className="bg-slate-50 border-b border-slate-100 px-8 py-5">
            <h3 className="text-xl font-bold text-slate-900">Recommended Action</h3>
          </div>
          <div className="px-8 py-8 space-y-6">
            <RecommendationBadge rec={finalRec.recommendation} />
            {decision?.bestVessel === "Unavailable" && (
              <div className="mt-6 p-4 bg-slate-50 border border-slate-200 rounded-lg">
                <p className="text-sm text-slate-700 font-medium">No feasible single-vessel plan exists for this cargo volume.</p>
                <p className="text-xs text-slate-500 mt-1">
                  Multi-voyage planning required - approximately {Math.ceil(Number(requirements?.cargoMt || 0) / 170000)} voyages based on Capesize limits.
                </p>
              </div>
            )}

            <div className="bg-slate-50 border border-slate-100 rounded-xl p-5 flex gap-3">
              <Info size={18} className="text-slate-400 mt-0.5 shrink-0" aria-hidden="true" />
              <p className="text-sm text-slate-700 leading-relaxed">{finalRec.reason}</p>
            </div>
          </div>
        </div>

        {/* Decision Context */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

          {/* System Best Choice */}
          <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6">
            <h4 className="text-sm font-bold uppercase tracking-widest text-slate-400 mb-4">Recommended Details</h4>
            <ContextRow label="Recommended Timing" value={decision?.bestTime} icon={<CalendarClock size={16} />} />
            <ContextRow
              label="Recommended Vessel"
              value={decision?.bestVessel !== "Unavailable" ? decision?.bestVessel?.["Vessel Type"] : "Unavailable"}
              icon={<Anchor size={16} />}
            />
            <ContextRow
              label="Recommended Port"
              value={decision?.bestPort !== "Unavailable" ? decision?.bestPort?.["Port"] : "Unavailable"}
              icon={<Map size={16} />}
            />
          </div>

          {/* Scenario Summary */}
          <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6">
            <h4 className="text-sm font-bold uppercase tracking-widest text-slate-400 mb-4">Scenario Summary</h4>
            <div className="space-y-3">
              {evaluations.map(ev => (
                <div key={ev.scenario} className="flex justify-between items-center text-sm py-2 border-b border-slate-100 last:border-0">
                  <span className="font-semibold text-slate-700">{ev.scenario}</span>
                  <div className="text-right text-xs text-slate-500 space-y-0.5">
                    <div>Cost: <span className="italic">{ev.totalCost === "Unavailable" ? "N/A - see note above" : ev.totalCost}</span></div>
                    <div>Risk: <span className="italic">{ev.riskScore === "Unavailable" ? "N/A - see note above" : ev.riskScore}</span></div>
                    <div>Buffer: <span className="italic">{ev.deadlineBuffer === "Unavailable" ? "N/A - see note above" : (ev.deadlineBuffer as number) < 0 ? `${Math.abs(ev.deadlineBuffer as number)} days late` : `+${ev.deadlineBuffer} days`}</span></div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Cost reference */}
          <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6">
            <h4 className="text-sm font-bold uppercase tracking-widest text-slate-400 mb-4">Cost Breakdown</h4>
            <ContextRow
              label="Freight Cost"
              value={selectedEval?.details.freightCost !== "Unavailable" && selectedEval?.details.freightCost !== undefined
                ? `$${selectedEval.details.freightCost.toLocaleString()}`
                : "Unavailable"}
              icon={<BarChart3 size={16} />}
            />
            <ContextRow label="Bunker Cost" value={selectedEval?.details.bunkerCost !== "Unavailable" ? "$" + selectedEval?.details.bunkerCost.toLocaleString() : "Unavailable"} icon={<BarChart3 size={16} />} />
            <ContextRow label="Port Cost" value={selectedEval?.details.portCost !== "Unavailable" ? "$" + selectedEval?.details.portCost.toLocaleString() : "Unavailable"} icon={<BarChart3 size={16} />} />
            <div className="mt-4 p-3 bg-blue-50 border border-blue-100 rounded-lg">
              <p className="text-xs text-blue-700 leading-relaxed">
                Full cost breakdown requires forecasting model for bunker and port tariffs.
              </p>
            </div>
          </div>
        </div>

        {/* Continue footer */}
        <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm flex flex-col md:flex-row items-center justify-between gap-6">
          <div>
            <h4 className="font-bold text-lg text-slate-900">Ready to proceed?</h4>
            <p className="text-slate-500 text-sm max-w-lg mt-1">
              View the consolidated summary of this recommendation.
            </p>
          </div>
          <Button 
            size="lg" 
            onClick={() => {
              markStepComplete('/final-recommendation');
              navigate('/human-approval');
            }}
            className="bg-blue-600 hover:bg-blue-700 text-white w-full md:w-auto shrink-0 shadow-md"
          >
            Request Approval
          </Button>
        </div>

      </main>
    </div>
  );
}
