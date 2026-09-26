import os
import re

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Replace DecisionLogic imports
    text = re.sub(
        r'import \{.*?\} from "\.\./\.\./utils/DecisionLogic";',
        'import { useState, useEffect } from "react";\nimport { evaluateScenarios as apiEvaluateScenarios, generateRecommendation as apiRunDecision } from "../../services/api";\ntype FinalRecommendationType = "BOOK NOW" | "WAIT" | "CHANGE PLAN" | "UNAVAILABLE";\ntype ScenarioType = "BOOK NOW" | "WAIT" | "CHANGE PLAN";',
        text,
        flags=re.DOTALL
    )

    # For HumanApproval.tsx
    if 'export function HumanApproval' in text:
        hooks = '''export function HumanApproval() {
  const { requirements, markStepComplete } = useVoyage();
  const { setApprovalResult } = useApproval();
  const navigate = useNavigate();

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
            bestVessel: "Unavailable",
            bestPort: "Unavailable"
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

  const finalRec = { recommendation: "UNAVAILABLE", reason: "Requires model." };
  
  // Keep original state hooks
  const [overrideRec, setOverrideRec] = useState<ScenarioType | "">("");
'''
        text = re.sub(r'export function HumanApproval\(\) \{.*?\n  const \[overrideRec, setOverrideRec\] = useState<ScenarioType \| "">\(""\);', hooks, text, flags=re.DOTALL)
        
        # Also need to fix null decision checks
        text = text.replace('decision.bestVessel !==', 'decision?.bestVessel !==')
        text = text.replace('decision.bestVessel[', 'decision?.bestVessel?.[')
        text = text.replace('decision.bestTime', 'decision?.bestTime')
        text = text.replace('decision.bestPort !==', 'decision?.bestPort !==')
        text = text.replace('decision.bestPort[', 'decision?.bestPort?.[')

        # Add loading return
        text = text.replace('return (\n    <div className="w-full relative min-h-screen', 'if (isLoading) return <div className="p-8 text-center text-slate-500">Loading approval workflow...</div>;\n\n  return (\n    <div className="w-full relative min-h-screen')

    # For FinalPlan.tsx
    if 'export function FinalPlan' in text:
        hooks = '''export function FinalPlan() {
  const { requirements, markStepComplete } = useVoyage();
  const { approvalResult } = useApproval();
  const navigate = useNavigate();

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
      } catch (err) {
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    }
    loadData();
  }, [requirements]);
'''
        text = re.sub(r'export function FinalPlan\(\) \{.*?\n  const evaluations = evaluateScenarios\(requirements\);', hooks, text, flags=re.DOTALL)
        
        # Add loading return
        text = text.replace('return (\n    <div className="w-full relative min-h-screen', 'if (isLoading) return <div className="p-8 text-center text-slate-500">Loading final plan...</div>;\n\n  return (\n    <div className="w-full relative min-h-screen')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

patch_file('SIH-FRONTEND/src/pages/approval/HumanApproval.tsx')
patch_file('SIH-FRONTEND/src/pages/finalplan/FinalPlan.tsx')
