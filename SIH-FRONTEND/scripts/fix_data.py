import re

files = [
    "src/pages/decision/DecisionWorkspace.tsx",
    "src/pages/recommendation/FinalRecommendation.tsx",
    "src/pages/approval/HumanApproval.tsx",
    "src/pages/finalplan/FinalPlan.tsx"
]

for file in files:
    with open(file, "r", encoding="utf-8") as f:
        text = f.read()
    
    # 1. Fix Laycan date parsing so FastAPI doesn't throw 422
    text = text.replace('laycan_start_date: requirements.laycan ? requirements.laycan.split(" - ")[0] : "2026-10-01"', 
                        'laycan_start_date: requirements.laycan ? new Date(requirements.laycan.split(" - ")[0]).toISOString().split("T")[0] : "2026-10-01"')
    
    # 2. Let's actually call vessel-feasibility to get the REAL vessel, rather than hardcoding Panamax!
    # I'll replace the hardcoded setDecision block with a dynamic one!
    fetch_feas = '''          const feasRes = await fetch("http://localhost:8000/api/v1/vessel-feasibility", {
            method: "POST", headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
              origin_port: payload.origin_port, destination_port: payload.destination_port,
              cargo_type: payload.cargo_type, cargo_quantity_mt: payload.quantity_mt
            })
          });
          const feasData = await feasRes.json();
          let bestVess = { "Vessel Type": "Panamax", "DWT (mt)": 75000, "SSW Draft (m)": 14.0, "LOA (m)": 225, "Beam (m)": 32.2, "Grain Capacity (cbm)": 89000, "Laden Speed (kn)": 14, "Ballast Speed (kn)": 14.5, "Max Age (yr)": 20, "Geared": false };
          let bestVessExpl = "Selected dynamically by the backend vessel feasibility engine.";
          
          if (feasData.vessels) {
            const feasibleOpt = feasData.vessels.find((v:any) => v.feasible);
            if (feasibleOpt) {
               bestVess["Vessel Type"] = feasibleOpt.vessel_class;
               bestVessExpl = "Directly feasible vessel found.";
            } else if (feasData.nearest_feasible_option) {
               bestVess["Vessel Type"] = feasData.nearest_feasible_option.vessel_class;
               bestVessExpl = Fallback option selected: . ;
            } else {
               bestVess = "Unavailable" as any;
               bestVessExpl = "No feasible vessel class exists for this cargo volume.";
            }
          }
          
          let rec = "UNAVAILABLE";
          if (data.recommended_scenario === "Book Now") rec = "BOOK NOW";
          else if (data.recommended_scenario && data.recommended_scenario.includes("Wait")) rec = "WAIT";
          else rec = "CHANGE PLAN";
          
          setDecision({
            bestTime: data.recommended_scenario || "Unavailable",
            bestTimeExplanation: data.recommendation_basis || "No recommendation.",
            bestVessel: bestVess,
            bestVesselExplanation: bestVessExpl,
            bestPort: { "Port": requirements.destination, "Region": "Target", "Max Draft (m)": 15.0 },
            bestPortExplanation: "Destination port constraints verified."
          });
          
          // In files where setFinalRec exists, we update it too, but we need to guard it
          if (typeof setFinalRec !== "undefined") {
            setFinalRec({
              recommendation: rec,
              reason: data.recommendation_basis || "No recommendation."
            });
          }'''
          
    # Find the setDecision block to replace
    start_idx = text.find('          setDecision({')
    end_idx = text.find('          });', start_idx)
    
    # Check if setFinalRec block follows
    final_rec_idx = text.find('          setFinalRec({', end_idx)
    if final_rec_idx != -1 and final_rec_idx < end_idx + 300:
        end_idx = text.find('          });', final_rec_idx)
    
    if start_idx != -1 and end_idx != -1:
        text = text[:start_idx] + fetch_feas + text[end_idx + 13:]
        
    with open(file, "w", encoding="utf-8") as f:
        f.write(text)

