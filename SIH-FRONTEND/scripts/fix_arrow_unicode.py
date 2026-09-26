import os

with open("src/pages/decision/DecisionWorkspace.tsx", "r", encoding="utf-8") as f:
    text = f.read()

# Replace the mangled route text
if "Not set" in text:
    old_line = '                {requirements?.origin || "Not set"} +\' {requirements?.destination || "Not set"}'
    new_line = '                {requirements?.origin || "Not set"} \u2192 {requirements?.destination || "Not set"}'
    
    # Try replacing dynamically if exact match fails
    import re
    text = re.sub(r'\{requirements\?\.origin \|\| "Not set"\} [^\{]+ \{requirements\?\.destination \|\| "Not set"\}', '{requirements?.origin || "Not set"} \u2192 {requirements?.destination || "Not set"}', text)

with open("src/pages/decision/DecisionWorkspace.tsx", "w", encoding="utf-8") as f:
    f.write(text)

with open("src/pages/recommendation/FinalRecommendation.tsx", "r", encoding="utf-8") as f:
    text2 = f.read()

    text2 = re.sub(r'\{requirements\?\.origin \|\| "Not set"\} [^\{]+ \{requirements\?\.destination \|\| "Not set"\}', '{requirements?.origin || "Not set"} \u2192 {requirements?.destination || "Not set"}', text2)

with open("src/pages/recommendation/FinalRecommendation.tsx", "w", encoding="utf-8") as f:
    f.write(text2)
