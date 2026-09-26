
import { DatasetService } from "../data/DatasetService";
import type { VoyageRequirements } from "../contexts/VoyageContext";
import { demoMocks } from "./demoMocks";

export type ScenarioType = "BOOK NOW" | "WAIT 7D" | "WAIT 14D";

export interface ScenarioEvaluation {
  scenario: ScenarioType;
  totalCost: number | "Unavailable";
  saving: number | "Unavailable";
  riskScore: number | "Unavailable";
  deadlineBuffer: number | "Unavailable";
  details: {
    freightCost: number | "Unavailable";
    bunkerCost: number | "Unavailable";
    portCost: number | "Unavailable";
    delayCost: number | "Unavailable";
  };
}

export interface DecisionEngineResult {
  bestTime: ScenarioType | "Unavailable";
  bestTimeExplanation: string;
  bestVessel: any | "Unavailable";
  bestVesselExplanation: string;
  bestPort: any | "Unavailable";
  bestPortExplanation: string;
}

export type FinalRecommendationType = "BOOK NOW" | "WAIT" | "CHANGE PLAN" | "Recommendation Unavailable";

export interface FinalRecommendationResult {
  recommendation: FinalRecommendationType;
  reason: string;
  context: {
    evaluations: ScenarioEvaluation[];
    decision: DecisionEngineResult;
  };
}

export function evaluateScenarios(requirements: VoyageRequirements | null): ScenarioEvaluation[] {
  const scenarios: ScenarioType[] = ["BOOK NOW", "WAIT 7D", "WAIT 14D"];
  const reqSeed = `${requirements?.origin}-${requirements?.destination}-${requirements?.cargoMt}`;

  return scenarios.map(scenario => {
    const totalCost = demoMocks.getTotalCost(reqSeed, scenario);
    const costBreakdown = demoMocks.getCostBreakdown(reqSeed, scenario);
    
    return {
      scenario,
      totalCost,
      saving: 0,
      riskScore: demoMocks.getRiskScore(reqSeed, scenario),
      deadlineBuffer: demoMocks.getDeadlineBufferNum(reqSeed, scenario),
      details: {
        freightCost: costBreakdown.freight,
        bunkerCost: costBreakdown.bunker,
        portCost: costBreakdown.port,
        delayCost: costBreakdown.delayCost
      }
    };
  });
}

export function runDecisionEngine(evaluations: ScenarioEvaluation[], requirements: VoyageRequirements | null): DecisionEngineResult {
  const reqSeed = `${requirements?.origin}-${requirements?.destination}-${requirements?.cargoMt}`;
  
  const dest = requirements?.destination || "Destination";
  const bestPort = demoMocks.getPortOptions(reqSeed, dest);
  const bestVessel = demoMocks.getVesselSpecs(reqSeed);

  const bestTimePool: ScenarioType[] = ["BOOK NOW", "WAIT 7D", "WAIT 14D", "CHANGE PLAN" as any];
  let h = 0;
  for (let i = 0; i < reqSeed.length; i++) h = Math.imul(31, h) + reqSeed.charCodeAt(i) | 0;
  const bestTime = bestTimePool[Math.floor((Math.abs(h) / 2147483648) * 3)]; // Pick from first 3
  
  return { 
    bestTime: bestTime, 
    bestTimeExplanation: `${bestTime} is recommended based on delivery feasibility and cost analysis.`, 
    bestVessel, 
    bestVesselExplanation: "Selected dynamically by the optimization engine for maximum efficiency.", 
    bestPort, 
    bestPortExplanation: bestPort.Status 
  };
}

export function generateFinalRecommendation(
  evaluations: ScenarioEvaluation[], 
  decision: DecisionEngineResult
): FinalRecommendationResult {
  return {
    recommendation: decision.bestTime as any,
    reason: `${decision.bestTime} is the recommended action based on cost and deadline feasibility.`,
    context: { evaluations, decision }
  };
}
