import re

with open("src/pages/finalplan/VoyageReceipt.tsx", "r", encoding="utf-8") as f:
    text = f.read()

# Replace the state and useEffect block

start_str = "  const [evaluations, setEvaluations] = useState<any[]>([]);"
end_str = "  const bookNowEval = evaluations.find(e => e.scenario === \"BOOK NOW\");"

new_code = """  const evaluations = evaluateScenarios(requirements);
  const decision = runDecisionEngine(evaluations, requirements);
  
  const bookNowEval = evaluations.find(e => e.scenario === "BOOK NOW");"""

start_idx = text.find(start_str)
end_idx = text.find(end_str)

if start_idx != -1 and end_idx != -1:
    text = text[:start_idx] + new_code + text[end_idx + len(end_str):]
    
    # We also need to add the imports for evaluateScenarios, runDecisionEngine
    import_stmt = 'import { evaluateScenarios, runDecisionEngine } from "../../utils/DecisionLogic";\n'
    text = text.replace('import { useAuth } from "../../contexts/AuthContext";', 'import { useAuth } from "../../contexts/AuthContext";\n' + import_stmt)
    
    # Remove the old api imports
    text = text.replace('import { evaluateScenarios as apiEvaluateScenarios, generateRecommendation as apiRunDecision } from "../../services/api";\n', '')
    text = text.replace('import { useState, useEffect } from "react";\n', '')

    with open("src/pages/finalplan/VoyageReceipt.tsx", "w", encoding="utf-8") as f:
        f.write(text)
else:
    print("Could not find start/end bounds for replacement in VoyageReceipt")
