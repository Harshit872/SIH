import re

with open("src/pages/recommendation/FinalRecommendation.tsx", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace('type FinalRecommendationType = "BOOK NOW" | "WAIT" | "CHANGE PLAN" | "UNAVAILABLE";', '')
text = text.replace('import { evaluateScenarios, runDecisionEngine, generateFinalRecommendation } from "../../utils/DecisionLogic";', 'import { evaluateScenarios, runDecisionEngine, generateFinalRecommendation, FinalRecommendationType } from "../../utils/DecisionLogic";')

# Remove duplicate imports
text = text.replace('import { evaluateScenarios as apiEvaluateScenarios, generateRecommendation as apiRunDecision } from "../../services/api";\n', '')
text = text.replace('import { useState, useEffect } from "react";\n', '')
text = text.replace('import { DatasetService } from "../../data/DatasetService";\n', '')

with open("src/pages/recommendation/FinalRecommendation.tsx", "w", encoding="utf-8") as f:
    f.write(text)
