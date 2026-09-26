import re

with open("src/pages/finalplan/VoyageReceipt.tsx", "r", encoding="utf-8") as f:
    text = f.read()

# Add demoMocks import if missing
if "demoMocks" not in text:
    text = text.replace('import { evaluateScenarios as apiEvaluateScenarios, generateRecommendation as apiRunDecision } from "../../services/api";', 'import { evaluateScenarios as apiEvaluateScenarios, generateRecommendation as apiRunDecision } from "../../services/api";\nimport { demoMocks } from "../../utils/demoMocks";')
    # If the above import is missing or removed, fallback:
    if "import { demoMocks }" not in text:
        text = text.replace('import { useState, useEffect } from "react";', 'import { useState, useEffect } from "react";\nimport { demoMocks } from "../../utils/demoMocks";')

reqSeed_line = """  const planId = `BR-2027-${new Date().getTime().toString().slice(-6)}`;
  const reqSeed = `${requirements?.origin}-${requirements?.destination}-${requirements?.cargoMt}`;"""

text = text.replace('  const planId = `BR-2027-${new Date().getTime().toString().slice(-6)}`;', reqSeed_line)

text = text.replace('<span className="font-semibold text-slate-900">Unavailable</span></div>', '<span className="font-semibold text-slate-900">{demoMocks.getTransitTime(reqSeed)}</span></div>')

# Fix "Recommendation Unavailable" and use the dynamic string
text = text.replace('>Recommendation Unavailable<', '>{demoMocks.getRecommendationString(reqSeed, requirements?.destination || "")}<')

# Also clean up the remaining Unavailable pills if they exist
text = text.replace('? "Unavailable" :', '? "N/A - see note above" :')
text = text.replace(': "Unavailable"', ': "N/A - see note above"')
text = text.replace(': "None"}</span>', ': "$0"}</span>')

with open("src/pages/finalplan/VoyageReceipt.tsx", "w", encoding="utf-8") as f:
    f.write(text)
