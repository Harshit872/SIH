// Demo mode: all API calls return realistic mock data locally.
// No backend required.

import { demoMocks } from "../utils/demoMocks";

function buildSeed(payload: any): string {
  return `${payload?.origin_port || ""}|${payload?.destination_port || ""}|${payload?.cargo_type || ""}|${payload?.quantity_mt || ""}`;
}

async function sleep(ms: number) {
  return new Promise(r => setTimeout(r, ms));
}

export const submitVoyage = async (req: any) => {
  await sleep(400);
  const seed = buildSeed(req);
  return { voyage_id: `V-${Date.now()}`, status: "submitted", seed };
};

export const getFeasibility = async (req: any) => {
  await sleep(350);
  const seed = buildSeed(req);
  return {
    feasibility: demoMocks.getDeliveryFeasibility(seed),
    transit_time: demoMocks.getTransitTime(seed),
    deadline_buffer_days: demoMocks.getDeadlineBufferNum(seed, "BOOK NOW"),
  };
};

export const getCosts = async (req: any) => {
  await sleep(350);
  const seed = buildSeed(req);
  const breakdown = demoMocks.getCostBreakdown(
    seed, "BOOK NOW",
    req?.origin_port, req?.destination_port, req?.quantity_mt
  );
  return {
    total_cost: breakdown.freight + breakdown.bunker + breakdown.port,
    freight_cost: breakdown.freight,
    bunker_cost: breakdown.bunker,
    port_cost: breakdown.port,
  };
};

export const getRisks = async (req: any) => {
  await sleep(300);
  const seed = buildSeed(req);
  return {
    risk_score: demoMocks.getRiskScore(seed, "BOOK NOW"),
    risk_label: demoMocks.getRiskScore(seed, "BOOK NOW") > 60 ? "High" : demoMocks.getRiskScore(seed, "BOOK NOW") > 35 ? "Medium" : "Low",
  };
};

export const evaluateScenarios = async (req: any) => {
  await sleep(500);
  const seed = buildSeed(req);
  return {
    scenarios: ["BOOK NOW", "WAIT 7D", "WAIT 14D"].map(s => ({
      scenario: s,
      total_cost: demoMocks.getTotalCost(seed, s, req?.origin_port, req?.destination_port, req?.quantity_mt),
      risk_score: demoMocks.getRiskScore(seed, s),
      deadline_buffer: demoMocks.getDeadlineBufferNum(seed, s),
    })),
  };
};

export const generateRecommendation = async (req: any) => {
  await sleep(400);
  const seed = buildSeed(req);
  return {
    recommendation: demoMocks.getRecommendedTiming(seed),
    reason: demoMocks.getRecommendationString(seed, req?.destination_port || "Port"),
  };
};
