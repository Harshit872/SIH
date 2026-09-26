import re

with open("src/pages/decision/DecisionWorkspace.tsx", "r", encoding="utf-8") as f:
    text = f.read()

# Remove the setFinalRec block
text = re.sub(
    r'\s*// In files where setFinalRec exists, we update it too, but we need to guard it\s*if \(typeof setFinalRec !== "undefined"\) \{[\s\S]*?\}\s*\}',
    '',
    text
)

with open("src/pages/decision/DecisionWorkspace.tsx", "w", encoding="utf-8") as f:
    f.write(text)
