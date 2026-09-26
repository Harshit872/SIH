import os

with open("src/utils/DecisionLogic.ts", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace('bestPortExplanation: "Destination port constraints verified."', 'bestPortExplanation: bestPort.Status')

with open("src/utils/DecisionLogic.ts", "w", encoding="utf-8") as f:
    f.write(text)
