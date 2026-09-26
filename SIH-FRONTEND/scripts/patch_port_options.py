import re

with open("SIH-FRONTEND/src/pages/voyage/VoyageRequirementInput.tsx", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace('PORT_OPTIONS.find(o => o.value === origin)?.label || origin', 'origin')
text = text.replace('PORT_OPTIONS.find(o => o.value === destination)?.label || destination', 'destination')
text = text.replace('COMMODITY_OPTIONS.find(o => o.value === commodity)?.label || commodity', 'commodity')

with open("SIH-FRONTEND/src/pages/voyage/VoyageRequirementInput.tsx", "w", encoding="utf-8") as f:
    f.write(text)
