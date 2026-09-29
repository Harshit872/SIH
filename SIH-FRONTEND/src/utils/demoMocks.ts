
// Demo-mode mock data engine.
// All outputs are deterministically seeded from route/cargo/volume inputs,
// so the same input always returns the same result, but different inputs
// return meaningfully different values — just like a real model would.

// ── Seeded PRNG ───────────────────────────────────────────────────────────────

export const getSeed = (seedStr: string): number => {
  let h = 0;
  for (let i = 0; i < seedStr.length; i++) h = Math.imul(31, h) + seedStr.charCodeAt(i) | 0;
  return Math.abs(h);
};

// Returns a float in [0, 1) deterministically from a string key
export const getSeededRandom = (key: string): number => getSeed(key) / 2147483648;

// Pick one item from a pool using a key
export const pick = <T>(key: string, pool: T[]): T =>
  pool[Math.floor(getSeededRandom(key) * pool.length)];

// Return a float in [min, max] seeded by key
const inRange = (key: string, min: number, max: number): number =>
  +(min + getSeededRandom(key) * (max - min)).toFixed(2);

// ── Route-aware helpers ───────────────────────────────────────────────────────

const VESSEL_TYPES: Record<string, string> = {
  Coal: "Capesize",
  "Iron Ore": "Capesize",
  Iron: "Capesize",
  Grain: "Panamax",
  Wheat: "Panamax",
  Soya: "Supramax",
  Bauxite: "Capesize",
  Fertilizer: "Supramax",
  Steel: "Handymax",
};

function resolveVesselType(commodity: string): string {
  const key = Object.keys(VESSEL_TYPES).find(k =>
    commodity?.toLowerCase().includes(k.toLowerCase())
  );
  return key ? VESSEL_TYPES[key] : "Panamax";
}

const VESSEL_SPECS: Record<string, object> = {
  Capesize: {
    "Vessel Type": "Capesize",
    "DWT (mt)": 182000,
    "SSW Draft (m)": 18.2,
    "LOA (m)": 292,
    "Beam (m)": 45.0,
    "Grain Capacity (cbm)": 198000,
    "Laden Speed (kn)": 14.5,
    "Ballast Speed (kn)": 15.0,
    "Max Age (yr)": 15,
    "Geared": false,
  },
  Panamax: {
    "Vessel Type": "Panamax",
    "DWT (mt)": 75000,
    "SSW Draft (m)": 13.6,
    "LOA (m)": 229,
    "Beam (m)": 32.3,
    "Grain Capacity (cbm)": 91000,
    "Laden Speed (kn)": 13.8,
    "Ballast Speed (kn)": 14.2,
    "Max Age (yr)": 15,
    "Geared": false,
  },
  Supramax: {
    "Vessel Type": "Supramax",
    "DWT (mt)": 58000,
    "SSW Draft (m)": 12.2,
    "LOA (m)": 196,
    "Beam (m)": 32.5,
    "Grain Capacity (cbm)": 74000,
    "Laden Speed (kn)": 13.5,
    "Ballast Speed (kn)": 14.0,
    "Max Age (yr)": 20,
    "Geared": true,
  },
  Handymax: {
    "Vessel Type": "Handymax",
    "DWT (mt)": 45000,
    "SSW Draft (m)": 11.5,
    "LOA (m)": 185,
    "Beam (m)": 30.0,
    "Grain Capacity (cbm)": 59000,
    "Laden Speed (kn)": 13.0,
    "Ballast Speed (kn)": 13.5,
    "Max Age (yr)": 20,
    "Geared": true,
  },
};

// ── Route distance estimator ──────────────────────────────────────────────────
// Used to scale costs realistically. Approximate NM between major port pairs.
const ROUTE_DISTANCES: Record<string, number> = {
  "Newcastle|Paradip": 5800, "Newcastle|Vizag": 5900, "Newcastle|Mumbai": 6100,
  "Newcastle|Karachi": 6500, "Newcastle|Port Qasim": 6500, "Newcastle|Colombo": 5700,
  "Gladstone|Paradip": 6000, "Gladstone|Vizag": 6100, "Gladstone|Mumbai": 6400,
  "Hay Point|Paradip": 5700, "Hay Point|Vizag": 5800,
  "Port Hedland|Paradip": 3800, "Port Hedland|Vizag": 3900, "Port Hedland|Kandla": 4100,
  "Dampier|Paradip": 3900, "Dampier|Mumbai": 4300,
  "Richards Bay|Mumbai": 4600, "Richards Bay|Paradip": 5400,
  "Tubarao|Paradip": 12000, "Tubarao|Vizag": 12100, "Tubarao|Mumbai": 11800,
};

function getRouteDistance(origin: string, dest: string, seed: number): number {
  const key = `${origin}|${dest}`;
  const revKey = `${dest}|${origin}`;
  return ROUTE_DISTANCES[key] || ROUTE_DISTANCES[revKey] || (4000 + (seed % 4000));
}

// ── Cost model ────────────────────────────────────────────────────────────────
// Costs scale with route distance and cargo volume — realistic for bulk shipping.
// Base freight: $8–18/MT, bunker ~35% of freight, port ~10%.

interface CostComponents { freight: number; bunker: number; port: number; delayCost: number; }

function computeBaseCost(reqSeed: string, origin: string, dest: string, cargoMt: number): number {
  const seed = getSeed(reqSeed);
  const distNm = getRouteDistance(origin, dest, seed);
  // Realistic freight rate: $9–17/MT for bulk, scaling gently with distance
  const baseRatePerMT = 9 + (seed % 8) + (distNm / 10000) * 4;
  const freight = Math.round(baseRatePerMT * cargoMt);
  const bunker = Math.round(freight * (0.30 + inRange(reqSeed + "bunk", 0, 0.1)));
  const port = Math.round(freight * (0.08 + inRange(reqSeed + "port", 0, 0.06)));
  return freight + bunker + port;
}

export const demoMocks = {

  getTotalCost: (reqSeed: string, scenario: string, origin?: string, dest?: string, cargoMt?: number): number => {
    const actualOrigin = origin || "Newcastle";
    const actualDest = dest || "Paradip";
    const actualCargo = cargoMt || 75000;
    const base = computeBaseCost(reqSeed, actualOrigin, actualDest, actualCargo);
    if (scenario.includes("7")) return Math.round(base * (1 + inRange(reqSeed + "wait7", 0.02, 0.07)));
    if (scenario.includes("14")) return Math.round(base * (1 + inRange(reqSeed + "wait14", 0.06, 0.16)));
    return base;
  },

  getRiskScore: (reqSeed: string, scenario: string): number => {
    if (scenario.includes("14")) return pick(reqSeed + scenario + "risk", [58, 65, 72, 78, 82, 85]);
    if (scenario.includes("7"))  return pick(reqSeed + scenario + "risk", [38, 45, 52, 58, 63, 68]);
    return pick(reqSeed + scenario + "risk", [12, 18, 22, 28, 33, 40]);
  },

  getDeadlineBufferNum: (reqSeed: string, scenario: string): number => {
    if (scenario.includes("14")) return pick(reqSeed + scenario + "buf", [-4, -3, -2, -1, 1]);
    if (scenario.includes("7"))  return pick(reqSeed + scenario + "buf", [-1, 0, 1, 2, 3]);
    return pick(reqSeed + scenario + "buf", [3, 4, 5, 6, 7, 8, 9]);
  },

  getDeadlineBufferStr: (reqSeed: string, scenario: string): string => {
    const n = demoMocks.getDeadlineBufferNum(reqSeed, scenario);
    if (n > 0) return `${n} days early`;
    if (n < 0) return `${Math.abs(n)} days late`;
    return "on schedule";
  },

  getCostBreakdown: (reqSeed: string, scenario: string, origin?: string, dest?: string, cargoMt?: number): CostComponents => {
    const total = demoMocks.getTotalCost(reqSeed, scenario, origin, dest, cargoMt);
    const delayCost = demoMocks.getWaitingCost(reqSeed, scenario);
    const remaining = total - delayCost;
    const freightRatio = 0.70 + inRange(reqSeed + "fratio", 0, 0.08);
    const bunkerRatio  = 0.18 + inRange(reqSeed + "bratio", 0, 0.05);
    const freight = Math.round(remaining * freightRatio);
    const bunker  = Math.round(remaining * bunkerRatio);
    const port    = remaining - freight - bunker;
    return { freight, bunker, port, delayCost };
  },

  getPortOptions: (reqSeed: string, dest: string) => {
    const draft = pick(reqSeed + "draft", [13.5, 14.5, 15.2, 16.0, 18.5]);
    const status = pick(reqSeed + "status", [
      "2 berths available", "Berth confirmed", "1 berth, congestion likely",
      "Berth pre-booked", "3 berths available",
    ]);
    const region = pick(reqSeed + "region", ["East India", "West India", "South Asia", "Middle East", "Southeast Asia"]);
    return {
      Port: dest || "Paradip",
      Region: region,
      "Max Draft (m)": draft,
      Status: status,
    };
  },

  getVesselSpecs: (reqSeed: string, commodity?: string): object => {
    const vesselType = resolveVesselType(commodity || "Coal");
    return VESSEL_SPECS[vesselType] || VESSEL_SPECS["Panamax"];
  },

  getTransitTime: (reqSeed: string): string => {
    return pick(reqSeed + "transit", ["9 days", "11 days", "12 days", "14 days", "16 days"]);
  },

  getWaitingCost: (reqSeed: string, scenario: string): number => {
    if (scenario.toUpperCase().includes("BOOK")) return 0;
    if (scenario.includes("7"))  return pick(reqSeed + scenario + "wait", [42000, 68000, 95000, 120000]);
    if (scenario.includes("14")) return pick(reqSeed + scenario + "wait", [120000, 165000, 210000, 260000]);
    return 0;
  },

  getDeliveryFeasibility: (reqSeed: string): string =>
    pick(reqSeed + "feas", ["Feasible", "Feasible with buffer", "At risk - tight schedule"]),

  getRecommendedTiming: (reqSeed: string): string =>
    pick(reqSeed + "timing", ["Book Now", "Wait 7 Days", "Wait 14 Days"]),

  getRecommendationString: (reqSeed: string, dest: string): string => {
    const vessel = resolveVesselType("Coal");
    return `${demoMocks.getRecommendedTiming(reqSeed)} — ${vessel} via ${dest}`;
  },
};
