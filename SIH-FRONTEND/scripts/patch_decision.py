import os
import re

with open('SIH-FRONTEND/src/pages/decision/DecisionWorkspace.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Imports
imports = '''import { useState, useEffect } from "react";
import { evaluateScenarios as apiEvaluateScenarios, generateRecommendation as apiRunDecision, getFeasibility } from "../../services/api";'''
text = text.replace('import { evaluateScenarios, runDecisionEngine } from "../../utils/DecisionLogic";', imports)

# 2. Hooks
hooks = '''const [scenarios, setScenarios] = useState<any[]>([]);
  const [decision, setDecision] = useState<any>(null);
  const [feasibility, setFeasibility] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      if (!requirements) {
        setIsLoading(false);
        return;
      }
      try {
        const payload = {
          origin: requirements.origin,
          destination: requirements.destination,
          commodity: requirements.commodity,
          cargoMt: requirements.cargoMt,
          deliveryDate: requirements.deliveryDate || new Date().toISOString(),
          contract: requirements.contract,
          laycan: requirements.laycan,
          noOfVoyages: requirements.noOfVoyages
        };
        const scenariosRes = await apiEvaluateScenarios(payload);
        
        const mappedScenarios = scenariosRes.scenarios.map((s: any) => ({
          scenario: s.name,
          totalCost: (s.cost_report && s.cost_report.is_total_complete) ? s.cost_report.total_amount : "Unavailable",
          saving: "Unavailable",
          riskScore: (s.risk_report && s.risk_report.status !== "INSUFFICIENT_DATA") ? s.risk_report.score : "Unavailable",
          deadlineBuffer: (s.schedule_report && s.schedule_report.status !== "INSUFFICIENT_DATA") ? s.schedule_report.buffer_days : "Unavailable",
          details: {
            freightCost: "Unavailable",
            bunkerCost: "Unavailable",
            portCost: "Unavailable",
            delayCost: "Unavailable",
          }
        }));
        setScenarios(mappedScenarios);

        try {
          const decisionRes = await apiRunDecision(payload);
          setDecision(decisionRes);
        } catch(e) {
          setDecision({
            bestTime: "Unavailable",
            bestTimeExplanation: "Backend decision engine not implemented yet.",
            bestVessel: "Unavailable",
            bestVesselExplanation: "",
            bestPort: "Unavailable",
            bestPortExplanation: ""
          });
        }

        try {
          const feasRes = await getFeasibility(payload);
          setFeasibility(feasRes);
        } catch(e) {
          console.error(e);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    }
    loadData();
  }, [requirements]);

  if (isLoading) return <div className="p-8 text-center text-slate-500">Loading evaluation from engine...</div>;'''

text = re.sub(r'  const scenarios = evaluateScenarios\(requirements\);.*?const decision = runDecisionEngine\(scenarios, requirements\);', hooks, text, flags=re.DOTALL)

# 3. Vessel Options UI
vessel_ui = '''<h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">Vessel Options (Feasibility)</h4>
                    {feasibility ? (
                      <div className="space-y-4 max-h-[400px] overflow-y-auto pr-2">
                        {feasibility.vessel_class_results.map((vr: any, idx: number) => (
                          <div key={idx} className="p-3 border rounded-lg bg-white">
                            <div className="flex items-center justify-between mb-2">
                              <span className="font-bold text-slate-900">{vr.vessel_type}</span>
                              <span className={	ext-xs font-semibold px-2 py-1 rounded-full }>
                                {vr.overall_status === 'INSUFFICIENT_DATA' ? 'UNKNOWN' : vr.overall_status}
                              </span>
                            </div>
                            {vr.overall_status === 'INFEASIBLE' && vr.berth_results.map((br: any, bidx: number) => (
                              br.status === 'INFEASIBLE' && (
                                <div key={bidx} className="text-xs text-red-600 mt-1">
                                  {br.berth}: {br.failed_constraints.join(", ")}
                                </div>
                              )
                            ))}
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div className="flex items-center gap-2 text-slate-500 text-sm">
                        <AlertCircle size={16} /> Checking feasibility...
                      </div>
                    )}'''

text = re.sub(r'<h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">Vessel Options</h4>.*?</div>\s*\)\}\s*</div>', vessel_ui, text, flags=re.DOTALL)

with open('SIH-FRONTEND/src/pages/decision/DecisionWorkspace.tsx', 'w', encoding='utf-8') as f:
    f.write(text)
