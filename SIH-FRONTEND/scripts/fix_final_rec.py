import os

with open("src/pages/recommendation/FinalRecommendation.tsx", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace('? "Unavailable" : ev.totalCost', '? "N/A - see note above" : ev.totalCost')
text = text.replace('? "Unavailable" : ev.riskScore', '? "N/A - see note above" : ev.riskScore')
text = text.replace('? "Unavailable" : (ev.deadlineBuffer as number) < 0', '? "N/A - see note above" : (ev.deadlineBuffer as number) < 0')

with open("src/pages/recommendation/FinalRecommendation.tsx", "w", encoding="utf-8") as f:
    f.write(text)
