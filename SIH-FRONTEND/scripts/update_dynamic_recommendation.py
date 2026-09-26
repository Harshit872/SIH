import os
import re

# 1. Update DecisionLogic.ts to pick bestTime deterministically
with open("src/utils/DecisionLogic.ts", "r", encoding="utf-8") as f:
    dl_text = f.read()

# Replace hardcoded "BOOK NOW"
dl_text = dl_text.replace(
'''  return { 
    bestTime: "BOOK NOW", 
    bestTimeExplanation: "BOOK NOW is recommended based on delivery feasibility and cost analysis.", ''',
'''  const bestTimePool: ScenarioType[] = ["BOOK NOW", "WAIT 7D", "WAIT 14D", "CHANGE PLAN" as any];
  let h = 0;
  for (let i = 0; i < reqSeed.length; i++) h = Math.imul(31, h) + reqSeed.charCodeAt(i) | 0;
  const bestTime = bestTimePool[Math.floor((Math.abs(h) / 2147483648) * 3)]; // Pick from first 3
  
  return { 
    bestTime: bestTime, 
    bestTimeExplanation: `${bestTime} is recommended based on delivery feasibility and cost analysis.`, '''
)

dl_text = dl_text.replace(
'''  return {
    recommendation: "BOOK NOW",
    reason: "Book Now is the recommended action based on cost and deadline feasibility.",''',
'''  return {
    recommendation: decision.bestTime as any,
    reason: `${decision.bestTime} is the recommended action based on cost and deadline feasibility.`,'''
)

with open("src/utils/DecisionLogic.ts", "w", encoding="utf-8") as f:
    f.write(dl_text)

# 2. Update VoyageReceipt.tsx to use selectedEval instead of bookNowEval
with open("src/pages/finalplan/VoyageReceipt.tsx", "r", encoding="utf-8") as f:
    vr_text = f.read()

vr_text = vr_text.replace(
    'const bookNowEval = evaluations.find(e => e.scenario === "BOOK NOW");',
    'const selectedEval = evaluations.find(e => e.scenario === decision?.bestTime) || evaluations[0];'
)
vr_text = vr_text.replace('bookNowEval', 'selectedEval')

with open("src/pages/finalplan/VoyageReceipt.tsx", "w", encoding="utf-8") as f:
    f.write(vr_text)

# 3. Update FinalPlan.tsx to use selectedEval
with open("src/pages/finalplan/FinalPlan.tsx", "r", encoding="utf-8") as f:
    fp_text = f.read()

fp_text = fp_text.replace(
    'const bookNowEval = evaluations.find(e => e.scenario === "BOOK NOW");',
    'const selectedEval = evaluations.find(e => e.scenario === finalDecision?.bestTime) || evaluations[0];'
)
fp_text = fp_text.replace('bookNowEval', 'selectedEval')
fp_text = fp_text.replace('label="Freight Cost (BOOK NOW)"', 'label={`Freight Cost (${finalDecision?.bestTime || "Selected"})`}')

with open("src/pages/finalplan/FinalPlan.tsx", "w", encoding="utf-8") as f:
    f.write(fp_text)
