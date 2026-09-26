import os
import re

with open('SIH-FRONTEND/src/pages/recommendation/FinalRecommendation.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace DecisionLogic imports
text = text.replace(
    'import {\n  evaluateScenarios,\n  runDecisionEngine,\n  generateFinalRecommendation,\n  type FinalRecommendationType\n} from "../../utils/DecisionLogic";',
    'import { useState, useEffect } from "react";\nimport { evaluateScenarios as apiEvaluateScenarios, generateRecommendation as apiRunDecision } from "../../services/api";\ntype FinalRecommendationType = "BOOK NOW" | "WAIT" | "CHANGE PLAN" | "UNAVAILABLE";'
)

# Replace the component logic
hooks = '''export function FinalRecommendation() {
  const { requirements, markStepComplete } = useVoyage();
  const navigate = useNavigate();

  const [evaluations, setEvaluations] = useState<any[]>([]);
  const [decision, setDecision] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [finalRec, setFinalRec] = useState<{recommendation: FinalRecommendationType, reason: string}>({
    recommendation: "UNAVAILABLE",
    reason: "Awaiting calculation..."
  });

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
        setEvaluations(mappedScenarios);

        setFinalRec({
          recommendation: "UNAVAILABLE",
          reason: "Final recommendation relies on missing model predictions (freight rate forecast and bunker cost). Cannot confidently recommend BOOK NOW or WAIT without full cost comparison."
        });

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
      } catch (err) {
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    }
    loadData();
  }, [requirements]);

  if (isLoading) return <div className="p-8 text-center text-slate-500">Generating final recommendation...</div>;

  const bookNowEval = evaluations.find(e => e.scenario === "BOOK NOW");
'''

text = re.sub(r'export function FinalRecommendation\(\) \{.*?\n  const bookNowEval = evaluations\.find\(e => e\.scenario === "BOOK NOW"\);', hooks, text, flags=re.DOTALL)

with open('SIH-FRONTEND/src/pages/recommendation/FinalRecommendation.tsx', 'w', encoding='utf-8') as f:
    f.write(text)
