import os
import re

mock_data_ts = """
// TEMP: mock/randomized data for demo - replace with real backend calls once forecasting/risk model integration is complete.

export const getSeed = (seedStr: string) => {
  let h = 0;
  for (let i = 0; i < seedStr.length; i++) h = Math.imul(31, h) + seedStr.charCodeAt(i) | 0;
  return Math.abs(h);
};

export const getSeededRandom = (seedStr: string) => getSeed(seedStr) / 2147483648;

export const pick = <T>(seedStr: string, pool: T[]): T => pool[Math.floor(getSeededRandom(seedStr) * pool.length)];

export const demoMocks = {
  getTotalCost: (reqSeed: string, scenario: string) => {
     const base = pick(reqSeed + "cost", [2100500, 2145300, 2185000, 2225000, 2280000]);
     if (scenario.includes("7")) return base + pick(reqSeed + "7", [120000, 150000, 180000]);
     if (scenario.includes("14")) return base + pick(reqSeed + "14", [290000, 320000, 360000]);
     return base;
  },
  getRiskScore: (reqSeed: string, scenario: string) => {
     if (scenario.includes("14")) return pick(reqSeed + scenario, [65, 72, 78, 82, 85]);
     if (scenario.includes("7")) return pick(reqSeed + scenario, [45, 52, 58, 62, 68]);
     return pick(reqSeed + scenario, [15, 22, 28, 35, 42]);
  },
  getDeadlineBufferStr: (reqSeed: string, scenario: string) => {
     if (scenario.includes("14")) return pick(reqSeed + scenario, ["2 days late", "4 days late", "1 day late"]);
     if (scenario.includes("7")) return pick(reqSeed + scenario, ["on schedule", "1 day early", "1 day late"]);
     return pick(reqSeed + scenario, ["4 days early", "6 days early", "9 days early"]);
  },
  getDeadlineBufferNum: (reqSeed: string, scenario: string) => {
     const str = demoMocks.getDeadlineBufferStr(reqSeed, scenario);
     if (str.includes("early")) return parseInt(str);
     if (str.includes("late")) return -parseInt(str);
     return 0;
  },
  getPortOptions: (reqSeed: string, dest: string) => {
     return {
       "Port": dest,
       "Region": "Target",
       "Max Draft (m)": pick(reqSeed + "draft", [14.5, 15.2, 16.0, 18.5]),
       "Status": pick(reqSeed + "status", ["2 berths available", "Berth confirmed", "1 berth, congestion likely"])
     };
  },
  getDeliveryFeasibility: (reqSeed: string) => pick(reqSeed + "feas", ["Feasible", "Feasible with buffer", "At risk - tight schedule"]),
  getRecommendedTiming: (reqSeed: string) => pick(reqSeed + "timing", ["Book Now", "Wait 7 Days", "Wait 14 Days"]),
  getVesselSpecs: (reqSeed: string) => ({
     "Vessel Type": "Capesize",
     "DWT (mt)": 182000,
     "SSW Draft (m)": 18.2,
     "LOA (m)": 292,
     "Beam (m)": 45.0,
     "Grain Capacity (cbm)": 198000,
     "Laden Speed (kn)": 14.5,
     "Ballast Speed (kn)": 15.0,
     "Max Age (yr)": 15,
     "Geared": false
  }),
  getCostBreakdown: (reqSeed: string, scenario: string) => {
     const total = demoMocks.getTotalCost(reqSeed, scenario);
     const freight = Math.round(total * 0.75);
     const bunker = Math.round(total * 0.18);
     const port = total - freight - bunker;
     return { freight, bunker, port };
  },
  getTransitTime: (reqSeed: string) => pick(reqSeed + "transit", ["9 days", "11 days", "13 days"]),
  getWaitingCost: (reqSeed: string, scenario: string) => {
     if (scenario.includes("BOOK")) return 0;
     return pick(reqSeed + scenario + "wait", [45000, 85000, 120000, 150000, 180000]);
  },
  getRecommendationString: (reqSeed: string, dest: string) => {
     return `${demoMocks.getRecommendedTiming(reqSeed)} - Capesize via ${dest}`;
  }
};
"""

if not os.path.exists("src/utils"):
    os.makedirs("src/utils")

with open("src/utils/demoMocks.ts", "w", encoding="utf-8") as f:
    f.write(mock_data_ts)
