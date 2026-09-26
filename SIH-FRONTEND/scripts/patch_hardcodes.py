import os
import re

# VoyageReceipt.tsx
path = 'SIH-FRONTEND/src/pages/finalplan/VoyageReceipt.tsx'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('<span className="font-semibold italic text-slate-400">Requires model</span>', '<span className="font-semibold text-slate-700">{bookNowEval?.details.bunkerCost !== "Unavailable" ? "$" + bookNowEval?.details.bunkerCost.toLocaleString() : "Requires model"}</span>', 1)
text = text.replace('<span className="font-semibold italic text-slate-400">Requires model</span>', '<span className="font-semibold text-slate-700">{bookNowEval?.details.portCost !== "Unavailable" ? "$" + bookNowEval?.details.portCost.toLocaleString() : "Requires model"}</span>', 1)
text = text.replace('<span className="font-semibold italic text-slate-400">Requires model</span>', '<span className="font-semibold text-slate-700">{bookNowEval?.details.delayCost !== "Unavailable" ? "$" + bookNowEval?.details.delayCost.toLocaleString() : "None"}</span>', 1)
text = text.replace('Requires model', 'Unavailable') # Replace all remaining

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

# FinalRecommendation.tsx
path = 'SIH-FRONTEND/src/pages/recommendation/FinalRecommendation.tsx'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('<ContextRow label="Bunker Cost" value="Requires model"', '<ContextRow label="Bunker Cost" value={bookNowEval?.details.bunkerCost !== "Unavailable" ? "$" + bookNowEval?.details.bunkerCost.toLocaleString() : "Requires model"}')
text = text.replace('<ContextRow label="Port Cost" value="Requires model"', '<ContextRow label="Port Cost" value={bookNowEval?.details.portCost !== "Unavailable" ? "$" + bookNowEval?.details.portCost.toLocaleString() : "Requires model"}')
text = text.replace('Requires model', 'Unavailable') # Replace all remaining

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
