import re

with open("src/pages/decision/DecisionWorkspace.tsx", "r", encoding="utf-8") as f:
    text = f.read()

# Replace the block exactly by substring
to_remove = """          // In files where setFinalRec exists, we update it too, but we need to guard it
          if (typeof setFinalRec !== "undefined") {
            setFinalRec({
              recommendation: rec,
              reason: data.recommendation_basis || "No recommendation."
            });
          }"""

text = text.replace(to_remove, "")

with open("src/pages/decision/DecisionWorkspace.tsx", "w", encoding="utf-8") as f:
    f.write(text)
