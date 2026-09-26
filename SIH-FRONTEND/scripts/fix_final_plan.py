import os

# --- 1. Fix FinalRecommendation.tsx Badge ---
with open("src/pages/recommendation/FinalRecommendation.tsx", "r", encoding="utf-8") as f:
    fr_text = f.read()

fr_text = fr_text.replace('if (rec === "WAIT") {', 'if (rec?.includes("WAIT")) {')
fr_text = fr_text.replace('<span className="text-2xl font-black text-amber-700 tracking-tight">WAIT</span>', '<span className="text-2xl font-black text-amber-700 tracking-tight">{rec}</span>')

with open("src/pages/recommendation/FinalRecommendation.tsx", "w", encoding="utf-8") as f:
    f.write(fr_text)


# --- 2. Fix FinalPlan.tsx ---
with open("src/pages/finalplan/FinalPlan.tsx", "r", encoding="utf-8") as f:
    fp_text = f.read()

fp_text = fp_text.replace(
    'const selectedEval  = evaluations.find(e => e.scenario === "BOOK NOW");',
    'const selectedEval  = evaluations.find(e => e.scenario === finalDecision?.bestTime) || evaluations[0];'
)

# Fix the badge styling conditions
fp_text = fp_text.replace('finalDecision.recommendation === "WAIT"', 'finalDecision.recommendation?.includes("WAIT")')

with open("src/pages/finalplan/FinalPlan.tsx", "w", encoding="utf-8") as f:
    f.write(fp_text)
