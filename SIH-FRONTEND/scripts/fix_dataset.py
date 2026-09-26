import re

files = [
    "src/pages/decision/DecisionWorkspace.tsx",
    "src/pages/recommendation/FinalRecommendation.tsx",
    "src/pages/approval/HumanApproval.tsx"
]

fetch_feas_old = """          let bestVess = { "Vessel Type": "Panamax", "DWT (mt)": 75000, "SSW Draft (m)": 14.0, "LOA (m)": 225, "Beam (m)": 32.2, "Grain Capacity (cbm)": 89000, "Laden Speed (kn)": 14, "Ballast Speed (kn)": 14.5, "Max Age (yr)": 20, "Geared": false };
          let bestVessExpl = "Selected dynamically by the backend vessel feasibility engine.";
          
          if (feasData.vessels) {
            const feasibleOpt = feasData.vessels.find((v:any) => v.feasible);
            if (feasibleOpt) {
               bestVess["Vessel Type"] = feasibleOpt.vessel_class;
               bestVessExpl = "Directly feasible vessel found.";
            } else if (feasData.nearest_feasible_option) {
               bestVess["Vessel Type"] = feasData.nearest_feasible_option.vessel_class;
               bestVessExpl = `Fallback option selected: ${feasData.nearest_feasible_option.mode}. ${feasData.nearest_feasible_option.reason}`;
            } else {
               bestVess = "Unavailable" as any;
               bestVessExpl = "No feasible vessel class exists for this cargo volume.";
            }
          }"""

fetch_feas_new = """          let bestVess: any = "Unavailable";
          let bestVessExpl = "No feasible vessel class exists for this cargo volume. Multi-voyage planning required.";
          
          if (feasData.vessels) {
            const feasibleOpt = feasData.vessels.find((v:any) => v.feasible);
            let targetClass = null;
            
            if (feasibleOpt) {
               targetClass = feasibleOpt.vessel_class;
               bestVessExpl = "Directly feasible vessel found.";
            } else if (feasData.nearest_feasible_option) {
               targetClass = feasData.nearest_feasible_option.vessel_class;
               bestVessExpl = `Fallback option selected: ${feasData.nearest_feasible_option.mode}. ${feasData.nearest_feasible_option.reason}`;
            }
            
            if (targetClass) {
               const allVessels = DatasetService.getVessels();
               const match = allVessels.find(v => v["Vessel Type"] === targetClass);
               if (match) {
                 bestVess = { ...match };
               } else {
                 // Fallback if dataset somehow missing
                 bestVess = { "Vessel Type": targetClass, "DWT (mt)": 75000, "SSW Draft (m)": 14.0, "LOA (m)": 225, "Beam (m)": 32.2, "Grain Capacity (cbm)": 89000, "Laden Speed (kn)": 14, "Ballast Speed (kn)": 14.5, "Max Age (yr)": 20, "Geared": false };
               }
            }
          }"""

for file in files:
    with open(file, "r", encoding="utf-8") as f:
        text = f.read()
    
    # 1. Inject import if missing
    if "import { DatasetService }" not in text:
        # FinalRecommendation and HumanApproval are nested differently, so we can just use relative path appropriately, but let's just do a blanket regex based on depth
        depth = "../../data/DatasetService"
        if "pages/decision/" in file: depth = "../../data/DatasetService"
        if "pages/recommendation/" in file: depth = "../../data/DatasetService"
        if "pages/approval/" in file: depth = "../../data/DatasetService"
        text = text.replace('import { useVoyage } from "../../contexts/VoyageContext";', f'import {{ useVoyage }} from "../../contexts/VoyageContext";\nimport {{ DatasetService }} from "{depth}";')

    text = text.replace(fetch_feas_old, fetch_feas_new)
    
    with open(file, "w", encoding="utf-8") as f:
        f.write(text)
