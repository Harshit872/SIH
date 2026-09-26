import os
import re

with open('SIH-FRONTEND/src/pages/finalplan/VoyageReceipt.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace DecisionLogic imports
text = text.replace(
    'import { evaluateScenarios, runDecisionEngine } from "../../utils/DecisionLogic";',
    'import { useState, useEffect } from "react";\nimport { evaluateScenarios as apiEvaluateScenarios, generateRecommendation as apiRunDecision } from "../../services/api";'
)

# Replace the component logic
hooks = '''export function VoyageReceipt() {
  const navigate = useNavigate();
  const { requirements } = useVoyage();
  const { approvalResult } = useApproval();

  const printRef = useRef<HTMLDivElement>(null);
  
  const planId = BR-2027-;

  const handlePrint = useReactToPrint({
    contentRef: printRef,
    documentTitle: Odyssey_Voyage_Receipt_
  });

  const handleDownloadPdf = () => {
    handlePrint();
  };

  const [evaluations, setEvaluations] = useState<any[]>([]);
  const [decision, setDecision] = useState<any>(null);
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

  const today = new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });

  if (isLoading) return <div className="p-8 text-center text-slate-500">Generating receipt...</div>;

  const bookNowEval = evaluations.find(e => e.scenario === "BOOK NOW");
'''

text = re.sub(r'export function VoyageReceipt\(\) \{.*?\n  const today = new Date\(\)\.toLocaleDateString.*?\n', hooks, text, flags=re.DOTALL)

with open('SIH-FRONTEND/src/pages/finalplan/VoyageReceipt.tsx', 'w', encoding='utf-8') as f:
    f.write(text)
