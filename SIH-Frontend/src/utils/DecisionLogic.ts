import { DatasetService } from "../data/DatasetService";
import type { VoyageRequirements } from "../contexts/VoyageContext";

// STEP 10 TYPES
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
    portCost: "Unavailable";
    delayCost: "Unavailable";
  };
}

// STEP 11 TYPES
export interface DecisionEngineResult {
  bestTime: ScenarioType | "Unavailable";
  bestTimeExplanation: string;
  bestVessel: any | "Unavailable";
  bestVesselExplanation: string;
  bestPort: any | "Unavailable";
  bestPortExplanation: string;
}

// STEP 12 TYPES
export type FinalRecommendationType = "BOOK NOW" | "WAIT" | "CHANGE PLAN" | "Recommendation Unavailable";

export interface FinalRecommendationResult {
  recommendation: FinalRecommendationType;
  reason: string;
  context: {
    evaluations: ScenarioEvaluation[];
    decision: DecisionEngineResult;
  };
}

// STEP 10 LOGIC
export function evaluateScenarios(requirements: VoyageRequirements | null): ScenarioEvaluation[] {
  const scenarios: ScenarioType[] = ["BOOK NOW", "WAIT 7D", "WAIT 14D"];

  const routeInfo = DatasetService.getRoutes().find(
    r => r.Origin === requirements?.origin && r.Destination === requirements?.destination
  );
  
  let baseFreightCost: number | "Unavailable" = "Unavailable";
  let transitDays = 0;

  if (routeInfo) {
    if (routeInfo["Freight Rate"] && requirements?.cargoMt) {
      baseFreightCost = Number(routeInfo["Freight Rate"]) * requirements.cargoMt;
    }
    if ((routeInfo as any)["Distance (nm)"]) {
      const distance = Number((routeInfo as any)["Distance (nm)"]);
      const avgSpeed = 13; // knots, typical bulk carrier speed from vessel master
      transitDays = Math.ceil(distance / (avgSpeed * 24));
    }
  }

  const deliveryDate = requirements?.deliveryDate ? new Date(requirements.deliveryDate) : null;
  const laycanStart = requirements?.laycan ? new Date(requirements.laycan.split(" - ")[0]) : null;

  return scenarios.map(scenario => {
    let delayDays = 0;
    if (scenario === "WAIT 7D") delayDays = 7;
    if (scenario === "WAIT 14D") delayDays = 14;

    let deadlineBuffer: number | "Unavailable" = "Unavailable";
    if (deliveryDate && laycanStart && transitDays > 0) {
      // Calculate buffer
      const estimatedArrival = new Date(laycanStart);
      estimatedArrival.setDate(estimatedArrival.getDate() + delayDays + transitDays);
      const diffTime = deliveryDate.getTime() - estimatedArrival.getTime();
      deadlineBuffer = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    }

    return {
      scenario,
      totalCost: "Unavailable", // Lacks complete cost components (bunker, port, etc.)
      saving: "Unavailable",
      riskScore: "Unavailable", // Lacks risk model data
      deadlineBuffer,
      details: {
        freightCost: scenario === "BOOK NOW" ? baseFreightCost : "Unavailable", // Forecasts are unavailable for 7D/14D
        bunkerCost: "Unavailable",
        portCost: "Unavailable",
        delayCost: "Unavailable"
      }
    };
  });
}

// STEP 11 LOGIC
export function runDecisionEngine(evaluations: ScenarioEvaluation[], requirements: VoyageRequirements | null): DecisionEngineResult {
  let bestTime: ScenarioType | "Unavailable" = "Unavailable";
  let bestTimeExplanation = "Insufficient data to accurately compare total costs, risks, and deadline feasibility across scenarios.";
  
  if (evaluations.length === 0) {
    bestTimeExplanation = "No evaluations provided.";
  }

  let bestVessel: any | "Unavailable" = "Unavailable";
  let bestVesselExplanation = "Insufficient requirements to map a feasible vessel.";
  
  if (requirements?.commodity) {
    const cargoMatch = DatasetService.getCargoes().find(c => c.Cargo === requirements.commodity);
    if (cargoMatch) {
      const candidateTypes = cargoMatch["Candidate Vessel Types"];
      const portInfo = DatasetService.getPorts().find(p => p.Port === requirements.origin || p.Port === requirements.destination);
      const matchingVessels = DatasetService.getVessels().filter(v => candidateTypes.includes(v["Vessel Type"]));
      
      if (matchingVessels.length > 0) {
        let selected = matchingVessels[0];
        if (portInfo && portInfo["Max Draft (m)"]) {
          const draftLimit = Number(portInfo["Max Draft (m)"]);
          const draftFeasible = matchingVessels.find(v => Number(v["SSW Draft (m)"]) <= draftLimit);
          if (draftFeasible) {
            selected = draftFeasible;
            bestVesselExplanation = `Selected from compatible vessel records based on commodity (${requirements.commodity}) and port draft constraints (${draftLimit}m).`;
          } else {
            bestVesselExplanation = `Selected based on commodity (${requirements.commodity}), but warning: may exceed known port draft limits.`;
          }
        } else {
          bestVesselExplanation = `Selected from compatible vessel records based on commodity requirements (${requirements.commodity}).`;
        }
        bestVessel = selected;
      }
    }
  }

  let bestPort: any | "Unavailable" = "Unavailable";
  let bestPortExplanation = "Required port information is missing from the dataset or voyage context.";
  
  if (requirements?.destination || requirements?.origin) {
    const targetPortName = requirements.destination || requirements.origin;
    const portRecord = DatasetService.getPorts().find(p => p.Port === targetPortName);
    if (portRecord) {
      bestPort = portRecord;
      bestPortExplanation = `Selected using available port master records and compatibility data for ${targetPortName}.`;
    }
  }

  // Determine Best Time based strictly on Deadline Buffer since cost/risk forecasts are absent
  const bookNow = evaluations.find(e => e.scenario === "BOOK NOW");

  if (bookNow && bookNow.deadlineBuffer !== "Unavailable") {
    if (bookNow.deadlineBuffer < 0) {
      bestTime = "Unavailable"; // Infeasible
      bestTimeExplanation = `Current plan is infeasible. Arrival will be ${Math.abs(bookNow.deadlineBuffer)} days late.`;
    } else {
      bestTime = "BOOK NOW";
      bestTimeExplanation = `BOOK NOW is recommended based on delivery feasibility. Deadline buffer is ${bookNow.deadlineBuffer} days. (Forecast optimization unavailable).`;
    }
  }

  return { bestTime, bestTimeExplanation, bestVessel, bestVesselExplanation, bestPort, bestPortExplanation };
}

// STEP 12 LOGIC
export function generateFinalRecommendation(
  evaluations: ScenarioEvaluation[], 
  decision: DecisionEngineResult
): FinalRecommendationResult {
  
  let recommendation: FinalRecommendationType = "Recommendation Unavailable";
  let reason = "Insufficient scenario evaluation data (forecasts, risk models, transit schedules) to deterministically recommend a final action.";

  const bookNowEval = evaluations.find(e => e.scenario === "BOOK NOW");
  const isFeasible = bookNowEval && bookNowEval.deadlineBuffer !== "Unavailable" && bookNowEval.deadlineBuffer >= 0;

  if (decision.bestTime === "BOOK NOW") {
    recommendation = "BOOK NOW";
    reason = "BOOK NOW is supported because the current scenario remains deadline-feasible. Optimization options require forecasting models.";
  } else if (!isFeasible && bookNowEval?.deadlineBuffer !== "Unavailable") {
    recommendation = "CHANGE PLAN";
    reason = `The current plan cannot satisfy the required constraints. Delivery would be ${Math.abs(Number(bookNowEval?.deadlineBuffer))} days late.`;
  } else if (decision.bestTime === "Unavailable" && decision.bestVessel === "Unavailable" && decision.bestPort === "Unavailable") {
    recommendation = "CHANGE PLAN";
    reason = "The current plan cannot satisfy the required constraints. The available data indicates that the existing voyage configuration cannot be reliably executed.";
  }

  return {
    recommendation,
    reason,
    context: {
      evaluations,
      decision
    }
  };
}
