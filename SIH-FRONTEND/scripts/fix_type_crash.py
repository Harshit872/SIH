import re

with open("src/pages/recommendation/FinalRecommendation.tsx", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace(
    'import { evaluateScenarios, runDecisionEngine, generateFinalRecommendation, FinalRecommendationType }',
    'import { evaluateScenarios, runDecisionEngine, generateFinalRecommendation }'
)

text = text.replace(
    'import { evaluateScenarios, runDecisionEngine, generateFinalRecommendation } from "../../utils/DecisionLogic";',
    'import { evaluateScenarios, runDecisionEngine, generateFinalRecommendation } from "../../utils/DecisionLogic";\nimport type { FinalRecommendationType } from "../../utils/DecisionLogic";'
)

with open("src/pages/recommendation/FinalRecommendation.tsx", "w", encoding="utf-8") as f:
    f.write(text)
