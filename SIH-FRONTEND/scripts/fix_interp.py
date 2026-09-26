import re

files = [
    "src/pages/decision/DecisionWorkspace.tsx",
    "src/pages/recommendation/FinalRecommendation.tsx",
    "src/pages/approval/HumanApproval.tsx",
    "src/pages/finalplan/FinalPlan.tsx"
]

for file in files:
    with open(file, "r", encoding="utf-8") as f:
        text = f.read()
    
    # Let's fix the broken string interpolation
    text = re.sub(
        r'bestVessExpl = Fallback option selected: \. ;',
        'bestVessExpl = `Fallback option selected: ${feasData.nearest_feasible_option.mode}. ${feasData.nearest_feasible_option.reason}`;',
        text
    )
    
    with open(file, "w", encoding="utf-8") as f:
        f.write(text)
