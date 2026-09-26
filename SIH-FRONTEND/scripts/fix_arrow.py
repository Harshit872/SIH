import os
import re

files_to_check = [
    "src/pages/decision/DecisionWorkspace.tsx",
    "src/pages/recommendation/FinalRecommendation.tsx"
]

for file in files_to_check:
    with open(file, "r", encoding="utf-8") as f:
        text = f.read()
    
    text = re.sub(r'\+\'', '?', text)
    text = text.replace('+\'', '?')
    
    with open(file, "w", encoding="utf-8") as f:
        f.write(text)
