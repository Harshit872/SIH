import os
import re

path = 'SIH-FRONTEND/src/pages/approval/HumanApproval.tsx'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

replacement = '''
  const finalRec = decision ? {
    recommendation: decision.bestTime === "BOOK NOW" ? "BOOK NOW" : (decision.bestTime === "WAIT 7 DAYS" || decision.bestTime === "WAIT 14 DAYS" ? "WAIT" : "CHANGE PLAN"),
    reason: decision.bestTimeExplanation
  } : { recommendation: "UNAVAILABLE", reason: "Unavailable" };
'''

text = re.sub(r'const finalRec = \{ recommendation: "UNAVAILABLE", reason: "Unavailable"\s* \};\s*', replacement.strip() + '\n', text)
# In case it's "Requires model." instead of "Unavailable":
text = re.sub(r'const finalRec = \{ recommendation: "UNAVAILABLE", reason: "Requires model\."\s* \};\s*', replacement.strip() + '\n', text)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
