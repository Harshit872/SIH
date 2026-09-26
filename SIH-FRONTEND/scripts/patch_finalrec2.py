import os
import re

path = 'SIH-FRONTEND/src/pages/recommendation/FinalRecommendation.tsx'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

replacement = '''
        try {
          const decisionRes = await apiRunDecision(payload);
          setDecision(decisionRes);
          setFinalRec({
            recommendation: decisionRes.bestTime === "BOOK NOW" ? "BOOK NOW" : (decisionRes.bestTime === "WAIT 7 DAYS" || decisionRes.bestTime === "WAIT 14 DAYS" ? "WAIT" : "CHANGE PLAN"),
            reason: decisionRes.bestTimeExplanation
          });
        } catch(e) {
          setDecision({
            bestTime: "Unavailable",
            bestTimeExplanation: "Backend decision engine not implemented yet.",
            bestVessel: "Unavailable",
            bestVesselExplanation: "",
            bestPort: "Unavailable",
            bestPortExplanation: ""
          });
        }
'''

text = re.sub(r'setFinalRec\(\{.*?\}\);\s*try \{\s*const decisionRes = await apiRunDecision\(payload\);\s*setDecision\(decisionRes\);\s*\} catch\(e\) \{.*?\}', replacement.strip(), text, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
