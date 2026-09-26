import os

with open("src/utils/DecisionLogic.ts", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace('import { VoyageRequirements }', 'import type { VoyageRequirements }')

with open("src/utils/DecisionLogic.ts", "w", encoding="utf-8") as f:
    f.write(text)
