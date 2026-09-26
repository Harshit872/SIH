import re

with open("src/pages/finalplan/VoyageReceipt.tsx", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace('  const bookNowEval = evaluations.find(e => e.scenario === "BOOK NOW");', '  const bookNowEval = evaluations.find(e => e.scenario === "BOOK NOW");\n  const today = new Date().toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" });')

with open("src/pages/finalplan/VoyageReceipt.tsx", "w", encoding="utf-8") as f:
    f.write(text)
