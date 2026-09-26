import os

with open("src/pages/recommendation/FinalRecommendation.tsx", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace(
    'const bookNowEval = evaluations.find(e => e.scenario === "BOOK NOW");',
    'const selectedEval = evaluations.find(e => e.scenario === decision?.bestTime) || evaluations[0];'
)
text = text.replace('bookNowEval', 'selectedEval')

with open("src/pages/recommendation/FinalRecommendation.tsx", "w", encoding="utf-8") as f:
    f.write(text)
