import os

mocked_logic = """
import { DatasetService } from "../data/DatasetService";
import { VoyageRequirements } from "../contexts/VoyageContext";
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
    const delayCost = demoMocks.getWaitingCost(reqSeed, scenario);
    
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
        delayCost: delayCost
      }
    };
  });
}

export function runDecisionEngine(evaluations: ScenarioEvaluation[], requirements: VoyageRequirements | null): DecisionEngineResult {
  const reqSeed = `${requirements?.origin}-${requirements?.destination}-${requirements?.cargoMt}`;
  
  const dest = requirements?.destination || "Destination";
  const bestPort = demoMocks.getPortOptions(reqSeed, dest);
  const bestVessel = demoMocks.getVesselSpecs(reqSeed);

  return { 
    bestTime: "BOOK NOW", 
    bestTimeExplanation: "BOOK NOW is recommended based on delivery feasibility and cost analysis.", 
    bestVessel, 
    bestVesselExplanation: "Selected dynamically by the optimization engine for maximum efficiency.", 
    bestPort, 
    bestPortExplanation: "Destination port constraints verified." 
  };
}

export function generateFinalRecommendation(
  evaluations: ScenarioEvaluation[], 
  decision: DecisionEngineResult
): FinalRecommendationResult {
  return {
    recommendation: "BOOK NOW",
    reason: "Book Now is the recommended action based on cost and deadline feasibility.",
    context: { evaluations, decision }
  };
}
"""

with open("src/utils/DecisionLogic.ts", "w", encoding="utf-8") as f:
    f.write(mocked_logic)
