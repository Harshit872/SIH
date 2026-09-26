import os

with open("src/pages/decision/DecisionWorkspace.tsx", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Insert selectedScenario
# Wait, let's just do a regex replace to insert it right before the return statement
text = text.replace(
    'const decision = runDecisionEngine(scenarios, requirements);',
    'const decision = runDecisionEngine(scenarios, requirements);\n  const selectedScenario = scenarios.find(s => s.scenario === decision.bestTime) || scenarios[0];'
)

# 2. Replace scenarios[0] with selectedScenario in the Feasibility block
# Wait, I'll just replace 'scenarios[0]' with 'selectedScenario' in the feasibility section.
# Specifically inside the "Delivery Feasibility" block
start_idx = text.find('Delivery Feasibility')
if start_idx != -1:
    before = text[:start_idx]
    after = text[start_idx:]
    after = after.replace('scenarios[0]', 'selectedScenario')
    after = after.replace("'Feasible (Book Now)'", "`Feasible (${selectedScenario.scenario})`")
    text = before + after

with open("src/pages/decision/DecisionWorkspace.tsx", "w", encoding="utf-8") as f:
    f.write(text)
