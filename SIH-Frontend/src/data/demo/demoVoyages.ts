export interface DemoVoyage {
  id: string;
  name: string;
  origin: string; // Must match PORT_OPTIONS value
  destination: string; // Must match PORT_OPTIONS value
  commodity: string; // Must match COMMODITY_OPTIONS value
  cargoQuantity: string;
  contract: string; // Must match CONTRACT_OPTIONS value
  deliveryDate: Date;
  laycanStart: Date;
  laycanEnd: Date;
  purpose: string;
}

// 2027 base year as per requirements
const baseYear = 2027;

export const DEMO_SCENARIOS: DemoVoyage[] = [
  {
    id: "clear-recommendation",
    name: "Scenario 1 — Clear Recommendation",
    origin: "mumbai",
    destination: "rotterdam",
    commodity: "iron_ore",
    cargoQuantity: "25000",
    contract: "voyage_charter", // maps to "Voyage Charter"
    deliveryDate: new Date(baseYear, 5, 30), // 30 June 2027
    laycanStart: new Date(baseYear, 5, 1),   // 1 June 2027
    laycanEnd: new Date(baseYear, 5, 10),    // 10 June 2027
    purpose: "Clear feasible voyage for Book Now"
  },
  {
    id: "wait-7-days",
    name: "Scenario 2 — Wait 7 Days",
    origin: "richards_bay",
    destination: "rotterdam",
    commodity: "coal",
    cargoQuantity: "50000",
    contract: "voyage_charter",
    deliveryDate: new Date(baseYear, 6, 15), // 15 July 2027
    laycanStart: new Date(baseYear, 5, 10),  // 10 June 2027
    laycanEnd: new Date(baseYear, 5, 20),    // 20 June 2027
    purpose: "Waiting 7 days provides a better economic balance"
  },
  {
    id: "wait-14-days",
    name: "Scenario 3 — Wait 14 Days",
    origin: "tubarao",
    destination: "qingdao",
    commodity: "iron_ore",
    cargoQuantity: "70000",
    contract: "voyage_charter",
    deliveryDate: new Date(baseYear, 7, 30), // 30 Aug 2027
    laycanStart: new Date(baseYear, 6, 1),   // 1 July 2027
    laycanEnd: new Date(baseYear, 6, 15),    // 15 July 2027
    purpose: "Timing comparison showing Book Now vs Wait 14 Days"
  },
  {
    id: "deadline-pressure",
    name: "Scenario 4 — Deadline Pressure",
    origin: "newcastle",
    destination: "yokohama",
    commodity: "coal",
    cargoQuantity: "45000",
    contract: "voyage_charter",
    deliveryDate: new Date(baseYear, 4, 20), // 20 May 2027
    laycanStart: new Date(baseYear, 4, 1),   // 1 May 2027
    laycanEnd: new Date(baseYear, 4, 5),     // 5 May 2027
    purpose: "Demonstrate delivery feasibility constraint"
  },
  {
    id: "constraint",
    name: "Scenario 5 — Vessel/Port Constraint",
    origin: "kandla",
    destination: "hamburg",
    commodity: "steel_products", // Note: The dataset has 'Steel' - I will check options
    cargoQuantity: "30000",
    contract: "voyage_charter",
    deliveryDate: new Date(baseYear, 8, 10), // 10 Sept 2027
    laycanStart: new Date(baseYear, 7, 15),  // 15 Aug 2027
    laycanEnd: new Date(baseYear, 7, 25),    // 25 Aug 2027
    purpose: "Vessel options limited by port compatibility"
  },
  {
    id: "high-risk",
    name: "Scenario 6 — High Risk / Change Plan",
    origin: "santos",
    destination: "rotterdam",
    commodity: "soybean_meal", // Or 'Soybeans'
    cargoQuantity: "40000",
    contract: "voyage_charter",
    deliveryDate: new Date(baseYear, 9, 5),  // 5 Oct 2027
    laycanStart: new Date(baseYear, 8, 1),   // 1 Sept 2027
    laycanEnd: new Date(baseYear, 8, 10),    // 10 Sept 2027
    purpose: "Complex decision with stronger risk signal"
  }
];
