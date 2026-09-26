import os

with open("src/pages/finalplan/FinalPlan.tsx", "r", encoding="utf-8") as f:
    text = f.read()

# Remove selectedEval from the top
text = text.replace(
    'const selectedEval  = evaluations.find(e => e.scenario === finalDecision?.bestTime) || evaluations[0];\n',
    ''
)

# Insert it after approvalResult destructuring
destructure_line = 'const { status, approvedAt, originalRecommendation, finalDecision } = approvalResult;'
new_lines = destructure_line + '\n  const selectedEval = evaluations.find(e => e.scenario === finalDecision?.bestTime) || evaluations[0];'

text = text.replace(destructure_line, new_lines)

with open("src/pages/finalplan/FinalPlan.tsx", "w", encoding="utf-8") as f:
    f.write(text)
