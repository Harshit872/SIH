import os

with open("src/pages/approval/HumanApproval.tsx", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Fix the CURRENT RECOMMENDATION badge string
old_rec_string = '{demoMocks.getRecommendationString(reqSeed, requirements?.destination || "")}'
new_rec_string = '{decision?.bestTime === "Unavailable" ? "Unavailable" : `${decision?.bestTime} - ${decision?.bestVessel?.["Vessel Type"] || "Vessel"} via ${decision?.bestPort?.["Port"] || "Port"}`}'
text = text.replace(old_rec_string, new_rec_string)

# 2. Fix the bookNowEval to selectedEval
text = text.replace(
    'const bookNowEval = evaluations.find(e => e.scenario === "BOOK NOW");',
    'const selectedEval = evaluations.find(e => e.scenario === decision?.bestTime) || evaluations[0];'
)

# 3. Replace bookNowEval with selectedEval globally
text = text.replace('bookNowEval', 'selectedEval')

# 4. Fix the hardcoded label "Freight Cost (BOOK NOW)"
text = text.replace(
    'label="Freight Cost (BOOK NOW)"',
    'label={`Freight Cost (${decision?.bestTime || "Selected"})`}'
)

with open("src/pages/approval/HumanApproval.tsx", "w", encoding="utf-8") as f:
    f.write(text)
