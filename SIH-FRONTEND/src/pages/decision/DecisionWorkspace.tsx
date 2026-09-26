import { useNavigate } from "react-router";
import { useVoyage } from "../../contexts/VoyageContext";
import { DatasetService } from "../../data/DatasetService";
import { 
  CalendarCheck, Clock, GitBranch, ShieldCheck, 
  Navigation, Anchor, AlertCircle
} from "lucide-react";
import { Button } from "../../components/ui/button";
import { evaluateScenarios, runDecisionEngine } from "../../utils/DecisionLogic";

export function DecisionWorkspace() {
  const { requirements, markStepComplete } = useVoyage();
  const navigate = useNavigate();
  const scenarios = evaluateScenarios(requirements);
  const decision = runDecisionEngine(scenarios, requirements);
  const selectedScenario = scenarios.find(s => s.scenario === decision.bestTime) || scenarios[0];

  return (
    <div className="w-full relative flex flex-col min-h-full">
      <main className="flex-1 w-full max-w-7xl mx-auto p-6 md:p-8 space-y-8 relative z-10">
        <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
          <h2 className="text-3xl font-bold text-slate-900 tracking-tight flex items-center gap-3">
            <GitBranch size={28} className="text-blue-600" /> Decision Workspace
          </h2>
          <p className="text-slate-500 mt-2 text-lg max-w-2xl">
            Explore timing options, vessel recommendations, and delivery feasibility to make an informed chartering decision.
          </p>
        </div>

        {/* Voyage Context Summary */}
        <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6 animate-in fade-in slide-in-from-bottom-6 duration-700 delay-100">
          <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400 mb-4 flex items-center gap-2">
            <Navigation size={16} /> Voyage Context
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div className="space-y-1">
              <span className="text-xs text-slate-500 font-medium">Route</span>
              <p className="text-sm font-semibold text-slate-900">
                {requirements?.origin || "Not set"} → {requirements?.destination || "Not set"}
              </p>
            </div>
            <div className="space-y-1">
              <span className="text-xs text-slate-500 font-medium">Commodity</span>
              <p className="text-sm font-semibold text-slate-900">{requirements?.commodity || "Not set"}</p>
            </div>
            <div className="space-y-1">
              <span className="text-xs text-slate-500 font-medium">Volume</span>
              <p className="text-sm font-semibold text-slate-900">{requirements?.cargoMt ? `${requirements.cargoMt} MT` : "Not set"}</p>
            </div>
            <div className="space-y-1">
              <span className="text-xs text-slate-500 font-medium">Delivery Target</span>
              <p className="text-sm font-semibold text-slate-900">{requirements?.deliveryDate || "Not set"}</p>
            </div>
            <div className="space-y-1">
              <span className="text-xs text-slate-500 font-medium">Laycan</span>
              <p className="text-sm font-semibold text-slate-900">{requirements?.laycan || "Not set"}</p>
            </div>
          </div>
        </div>

        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-6 duration-700 delay-150">
          
          {/* Explore Timing Options */}
          <div className="w-full">
            <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden flex flex-col h-full">
              <div className="bg-slate-50 border-b border-slate-100 p-5 flex items-center gap-3">
                <div className="p-2 bg-blue-100 text-blue-700 rounded-lg">
                  <Clock size={20} />
                </div>
                <div>
                  <h3 className="font-semibold text-slate-900">Explore Timing Options</h3>
                  <p className="text-xs text-slate-500">Evaluate cost, risk, and deadline buffer across timing strategies.</p>
                </div>
              </div>
              <div className="p-6">
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  {scenarios.map((evalData, idx) => (
                    <div key={idx} className="bg-slate-50 border border-slate-200 rounded-lg p-4 flex flex-col hover:border-blue-300 transition-colors">
                      <h4 className="font-bold text-slate-900 mb-4">{evalData.scenario}</h4>
                      
                      <div className="space-y-3 flex-1">
                        <div>
                          <span className="text-xs text-slate-500 block">Total Cost</span>
                          <span className="text-sm font-semibold text-slate-900">
                            {evalData.totalCost === "Unavailable" ? (
                              <span className="text-slate-400 text-xs italic">N/A - see note above</span>
                            ) : `$${evalData.totalCost.toLocaleString()}`}
                          </span>
                        </div>
                        <div>
                          <span className="text-xs text-slate-500 block">Risk Score</span>
                          <span className="text-sm font-semibold text-slate-900">
                            {evalData.riskScore === "Unavailable" ? (
                              <span className="text-slate-400 text-xs italic">N/A - see note above</span>
                            ) : evalData.riskScore}
                          </span>
                        </div>
                        <div>
                          <span className="text-xs text-slate-500 block">Deadline Buffer</span>
                          <span className="text-sm font-semibold text-slate-900">
                            {evalData.deadlineBuffer === "Unavailable" ? (
                              <span className="text-slate-400 text-xs italic">N/A - see note above</span>
                            ) : evalData.deadlineBuffer < 0 ? (
                              <span className="text-red-600 font-bold">{Math.abs(evalData.deadlineBuffer as number)} days late</span>
                            ) : (
                              <span className="text-emerald-600 font-bold">+{evalData.deadlineBuffer} days</span>
                            )}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Side Info: Vessel Recommendation & Delivery Feasibility */}
          <div className="space-y-6">
            
            {/* Vessel & Port Recommendation */}
            <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
              <div className="bg-slate-50 border-b border-slate-100 p-5 flex items-center gap-3">
                <div className="p-2 bg-emerald-100 text-emerald-700 rounded-lg">
                  <Anchor size={20} />
                </div>
                <h3 className="font-semibold text-slate-900">System Recommendations</h3>
              </div>
              <div className="p-6 space-y-6">
                {/* Vessel Options */}
                <div>
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">Vessel Options</h4>
                  {decision.bestVessel !== "Unavailable" ? (
                    <div className="space-y-3">
                      <span className="text-lg font-bold text-slate-900 block">{decision.bestVessel["Vessel Type"]}</span>
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span className="text-slate-500">Capacity (DWT)</span>
                          <span className="font-medium text-slate-900">{decision.bestVessel["DWT (mt)"]} MT</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-500">Draft</span>
                          <span className="font-medium text-slate-900">{decision.bestVessel["SSW Draft (m)"]}m</span>
                        </div>
                      </div>
                      <p className="text-xs text-slate-500 mt-2 p-2 bg-slate-50 rounded border border-slate-100">
                        {decision.bestVesselExplanation}
                      </p>
                    </div>
                  ) : (
                    <div className="flex items-center gap-2 text-slate-500 text-sm">
                      <AlertCircle size={16} /> Unavailable
                    </div>
                  )}
                </div>

                {/* Port Options */}
                <div>
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">Port Options</h4>
                  {decision.bestPort !== "Unavailable" ? (
                    <div className="space-y-3">
                      <span className="text-lg font-bold text-slate-900 block">{decision.bestPort["Port"]}</span>
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span className="text-slate-500">Region</span>
                          <span className="font-medium text-slate-900">{decision.bestPort["Region"]}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-500">Max Draft</span>
                          <span className="font-medium text-slate-900">{decision.bestPort["Max Draft (m)"]}m</span>
                        </div>
                      </div>
                      <p className="text-xs text-slate-500 mt-2 p-2 bg-slate-50 rounded border border-slate-100">
                        {decision.bestPortExplanation}
                      </p>
                    </div>
                  ) : (
                    <div className="flex items-center gap-2 text-slate-500 text-sm">
                      <AlertCircle size={16} /> Unavailable
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Delivery Feasibility */}
            <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
              <div className="bg-slate-50 border-b border-slate-100 p-5 flex items-center gap-3">
                <div className="p-2 bg-amber-100 text-amber-700 rounded-lg">
                  <CalendarCheck size={20} />
                </div>
                <h3 className="font-semibold text-slate-900">Delivery Feasibility</h3>
              </div>
              <div className="p-6 flex flex-col justify-center items-center py-8">
                 {selectedScenario && selectedScenario.deadlineBuffer !== "Unavailable" ? (
                   <>
                     <div className={`inline-flex items-center justify-center w-12 h-12 rounded-full mb-3 ${selectedScenario.deadlineBuffer >= 0 ? 'bg-emerald-100 text-emerald-600' : 'bg-red-100 text-red-600'}`}>
                        <ShieldCheck size={24} />
                     </div>
                     <div className={`inline-flex items-center px-4 py-2 rounded-full border font-medium text-sm ${selectedScenario.deadlineBuffer >= 0 ? 'bg-emerald-50 border-emerald-200 text-emerald-700' : 'bg-red-50 border-red-200 text-red-700'}`}>
                        {selectedScenario.deadlineBuffer >= 0 ? `Feasible (${selectedScenario.scenario})` : 'Infeasible Plan'}
                     </div>
                     <p className="text-xs text-center text-slate-500 mt-3 max-w-[200px]">
                        {selectedScenario.deadlineBuffer >= 0 ? `Current requirements allow a ${selectedScenario.deadlineBuffer}-day buffer.` : `Target arrival is ${Math.abs(selectedScenario.deadlineBuffer as number)} days late.`}
                     </p>
                   </>
                 ) : (
                   <>
                     <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-slate-100 text-slate-400 mb-3">
                        <ShieldCheck size={24} />
                     </div>
                     <div className="inline-flex items-center px-4 py-2 rounded-full bg-slate-100 border border-slate-200 text-slate-600 font-medium text-sm">
                        Validation unavailable
                     </div>
                     <p className="text-xs text-center text-slate-500 mt-3 max-w-[200px]">
                        Requires complete voyage parameters.
                     </p>
                   </>
                 )}
              </div>
            </div>

          </div>
        </div>

        {/* Global Action Footer */}
        <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm flex flex-col md:flex-row items-center justify-between gap-6 mt-8 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-300">
          <div>
            <h4 className="font-bold text-lg text-slate-900">Ready for your review?</h4>
            <p className="text-slate-500 text-sm max-w-lg mt-1">
              Review the recommended voyage plan based on your selected timing and vessel options.
            </p>
          </div>
          <Button 
            size="lg" 
            onClick={() => {
              markStepComplete('/decision-workspace');
              navigate('/final-recommendation');
            }}
            className="bg-blue-600 hover:bg-blue-700 text-white w-full md:w-auto shrink-0 shadow-md"
          >
            Review Recommendation
          </Button>
        </div>

      </main>
    </div>
  );
}
