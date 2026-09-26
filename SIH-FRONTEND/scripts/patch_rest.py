import re

files = [
    "SIH-FRONTEND/src/pages/recommendation/FinalRecommendation.tsx",
    "SIH-FRONTEND/src/pages/approval/HumanApproval.tsx",
    "SIH-FRONTEND/src/pages/finalplan/FinalPlan.tsx"
]

hooks = '''
  const [evaluations, setEvaluations] = useState<any[]>([]);
  const [decision, setDecision] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [finalRec, setFinalRec] = useState<any>({
    recommendation: "UNAVAILABLE",
    reason: "Awaiting calculation..."
  });

  useEffect(() => {
    async function loadData() {
      if (!requirements) {
        setIsLoading(false);
        return;
      }
      try {
        const payload = {
          origin_port: requirements.origin,
          destination_port: requirements.destination,
          cargo_type: requirements.commodity,
          quantity_mt: Number(requirements.cargoMt),
          vessel_class: "Panamax",
          route_distance_nm: 6300,
          bunker_price_usd_per_mt: 850,
          bdi_value: 1500,
          port_turnaround_days: 4.5,
          demurrage_rate: 20000,
          laycan_start_date: requirements.laycan ? requirements.laycan.split(" - ")[0] : "2026-10-01",
          required_delivery_date: requirements.deliveryDate || "2026-10-25"
        };
        
        const res = await fetch("http://localhost:8000/api/v1/what-if", {
          method: "POST", headers: {"Content-Type": "application/json"},
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        
        if (data.scenarios) {
          const mapped = data.scenarios.map((s: any) => ({
            scenario: s.scenario_name.toUpperCase(),
            totalCost: s.total_cost_usd,
            saving: "Unavailable",
            riskScore: s.risk_score,
            deadlineBuffer: s.deadline_feasible ? 2 : (s.risk_score === 50 ? -5 : "Unavailable"),
            details: {
              freightCost: "Unavailable", bunkerCost: "Unavailable", portCost: "Unavailable", delayCost: "Unavailable"
            }
          }));

          const dlRes = await fetch("http://localhost:8000/api/v1/deadline-check", {
            method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({...payload, vessel_speed_knots: 13.5})
          });
          const dlData = await dlRes.json();
          if (mapped.length > 0 && dlData.buffer_days !== undefined) {
            mapped[0].deadlineBuffer = dlData.buffer_days;
          }

          setEvaluations(mapped);
          
          setDecision({
            bestTime: data.recommended_scenario,
            bestTimeExplanation: data.recommendation_basis,
            bestVessel: { "Vessel Type": "Panamax", "DWT (mt)": 75000, "SSW Draft (m)": 14.0 },
            bestVesselExplanation: "Feasible",
            bestPort: { "Port": requirements.destination, "Region": "Target", "Max Draft (m)": 15.0 },
            bestPortExplanation: "Feasible"
          });

          let rec = "UNAVAILABLE";
          if (data.recommended_scenario === "Book Now") rec = "BOOK NOW";
          else if (data.recommended_scenario.includes("Wait")) rec = "WAIT";
          else rec = "CHANGE PLAN";
          
          setFinalRec({
            recommendation: rec,
            reason: data.recommendation_basis
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
'''

for file in files:
    with open(file, "r", encoding="utf-8") as f:
        text = f.read()
    
    # Replace the useEffect logic
    # Find start of hooks
    start_idx = text.find('  const [evaluations, setEvaluations] = useState<any[]>([])')
    end_idx = text.find('  if (isLoading)', start_idx)
    
    if start_idx != -1 and end_idx != -1:
        text = text[:start_idx] + hooks + text[end_idx:]
        with open(file, "w", encoding="utf-8") as f:
            f.write(text)

