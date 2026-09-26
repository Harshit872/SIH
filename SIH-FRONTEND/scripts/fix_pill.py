import re

# Fix DecisionWorkspace.tsx
with open("src/pages/decision/DecisionWorkspace.tsx", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace('<span className="text-slate-400 text-xs italic">Unavailable</span>', '<span className="text-slate-400 text-xs italic">N/A - see note above</span>')

with open("src/pages/decision/DecisionWorkspace.tsx", "w", encoding="utf-8") as f:
    f.write(text)


# Fix HumanApproval.tsx
with open("src/pages/approval/HumanApproval.tsx", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace('return <span className="text-slate-400 italic text-sm">Unavailable</span>;', 'return <span className="text-slate-400 italic text-xs">N/A - see note above</span>;')

with open("src/pages/approval/HumanApproval.tsx", "w", encoding="utf-8") as f:
    f.write(text)


# Fix FinalPlan.tsx (already changed the manual span, let's fix the Pill just in case)
with open("src/pages/finalplan/FinalPlan.tsx", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace('return <span className="text-slate-400 italic text-sm">Unavailable</span>;', 'return <span className="text-slate-400 italic text-xs">N/A - see note above</span>;')

with open("src/pages/finalplan/FinalPlan.tsx", "w", encoding="utf-8") as f:
    f.write(text)
