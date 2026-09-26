import os
import re

files_to_patch = [
    'SIH-FRONTEND/src/pages/decision/DecisionWorkspace.tsx',
    'SIH-FRONTEND/src/pages/recommendation/FinalRecommendation.tsx',
    'SIH-FRONTEND/src/pages/approval/HumanApproval.tsx',
    'SIH-FRONTEND/src/pages/finalplan/VoyageReceipt.tsx',
    'SIH-FRONTEND/src/pages/finalplan/FinalPlan.tsx'
]

replacement = '''
        const mappedScenarios = scenariosRes.scenarios.map((s: any) => {
          const getComp = (name: string) => {
            if (!s.cost_report || !s.cost_report.components) return "Unavailable";
            const c = s.cost_report.components.find((x: any) => x.name === name);
            return c && c.amount !== null ? c.amount : "Unavailable";
          };
          return {
            scenario: s.name.toUpperCase(),
            totalCost: (s.cost_report && s.cost_report.total_amount !== null) ? s.cost_report.total_amount : "Unavailable",
            riskScore: (s.risk_report && s.risk_report.score !== null) ? s.risk_report.score : "Unavailable",
            deadlineBuffer: (s.schedule_report && s.schedule_report.buffer_days !== null) ? s.schedule_report.buffer_days : "Unavailable",
            details: {
              freightCost: getComp("Freight Cost"),
              bunkerCost: getComp("Bunker Cost"),
              portCost: getComp("Port Charges"),
              delayCost: getComp("Waiting Cost"),
            }
          };
        });
'''

for filepath in files_to_patch:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Replace the mappedScenarios block
    pattern = r'const mappedScenarios = scenariosRes\.scenarios\.map\(\(s: any\) => \(\{.*?\n\s*\}\)\);'
    text = re.sub(pattern, replacement.strip(), text, flags=re.DOTALL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
