import re

with open("src/pages/recommendation/FinalRecommendation.tsx", "r", encoding="utf-8") as f:
    text = f.read()

# Replace the data loading section

start_str = "  const [evaluations, setEvaluations] = useState<any[]>([]);"
end_str = "    // Handlers"

new_code = """  const evaluations = evaluateScenarios(requirements);
  const decision = runDecisionEngine(evaluations, requirements);
  const finalRec = generateFinalRecommendation(evaluations, decision);
  const isLoading = false;
  
"""

start_idx = text.find(start_str)
end_idx = text.find(end_str)

if start_idx != -1 and end_idx != -1:
    text = text[:start_idx] + new_code + text[end_idx:]
    
    # We also need to add the imports for evaluateScenarios, runDecisionEngine, generateFinalRecommendation
    import_stmt = 'import { evaluateScenarios, runDecisionEngine, generateFinalRecommendation } from "../../utils/DecisionLogic";\n'
    text = text.replace('import { useVoyage } from "../../contexts/VoyageContext";', 'import { useVoyage } from "../../contexts/VoyageContext";\n' + import_stmt)
    
    with open("src/pages/recommendation/FinalRecommendation.tsx", "w", encoding="utf-8") as f:
        f.write(text)
else:
    print("Could not find start/end bounds for replacement")

