
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

export type FinalRecommendationType = "BOOK NOW" | "WAIT" | "WAIT 7D" | "WAIT 14D" | "CHANGE PLAN" | "Recommendation Unavailable";


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
  const origin = requirements?.origin || "Newcastle";
  const dest = requirements?.destination || "Paradip";
  const cargoMt = Number(requirements?.cargoMt) || 75000;

  const evals = scenarios.map(scenario => {
    const totalCost = demoMocks.getTotalCost(reqSeed, scenario, origin, dest, cargoMt);
    const costBreakdown = demoMocks.getCostBreakdown(reqSeed, scenario, origin, dest, cargoMt);

    return {
      scenario,
      totalCost,
      saving: 0 as number | "Unavailable",
      riskScore: demoMocks.getRiskScore(reqSeed, scenario),
      deadlineBuffer: demoMocks.getDeadlineBufferNum(reqSeed, scenario),
      details: {
        freightCost: costBreakdown.freight,
        bunkerCost: costBreakdown.bunker,
        portCost: costBreakdown.port,
        delayCost: costBreakdown.delayCost,
      },
    };
  });

  // Compute savings relative to BOOK NOW baseline
  const bookNowCost = evals[0].totalCost as number;
  evals.forEach(e => {
    e.saving = typeof e.totalCost === "number" ? e.totalCost - bookNowCost : "Unavailable";
  });

  return evals;
}

export function runDecisionEngine(evaluations: ScenarioEvaluation[], requirements: VoyageRequirements | null): DecisionEngineResult {
  const reqSeed = `${requirements?.origin}-${requirements?.destination}-${requirements?.cargoMt}`;
  const dest = requirements?.destination || "Destination";
  const commodity = requirements?.commodity || "Coal";

  const bestPort = demoMocks.getPortOptions(reqSeed, dest);
  const bestVessel = demoMocks.getVesselSpecs(reqSeed, commodity);

  // Pick best time: prefer scenarios where deadlineBuffer >= 0, ranked by cost
  const feasible = evaluations.filter(e => typeof e.deadlineBuffer === "number" && (e.deadlineBuffer as number) >= 0);
  const ranked = feasible.length > 0
    ? feasible.sort((a, b) => (a.totalCost as number) - (b.totalCost as number))
    : evaluations;
  const bestTime = ranked[0]?.scenario || "BOOK NOW";

  const explanation: Record<string, string> = {
    "BOOK NOW": "Booking now minimises total voyage cost and ensures delivery well within the deadline with maximum schedule buffer.",
    "WAIT 7D": "Waiting 7 days is projected to reduce freight rates, resulting in modest savings while keeping the delivery timeline feasible.",
    "WAIT 14D": "Waiting 14 days captures the largest rate reduction but tightens the delivery window — accept only if the deadline allows flexibility.",
  };

  return {
    bestTime,
    bestTimeExplanation: explanation[bestTime] || `${bestTime} is recommended based on cost and feasibility analysis.`,
    bestVessel,
    bestVesselExplanation: `Selected for optimal cargo compatibility, draft clearance at ${dest}, and route efficiency.`,
    bestPort,
    bestPortExplanation: bestPort.Status,
  };
}

export function generateFinalRecommendation(
  evaluations: ScenarioEvaluation[],
  decision: DecisionEngineResult
): FinalRecommendationResult {
  const rec = decision.bestTime as FinalRecommendationType;
  return {
    recommendation: rec,
    reason: decision.bestTimeExplanation,
    context: { evaluations, decision },
  };
}
