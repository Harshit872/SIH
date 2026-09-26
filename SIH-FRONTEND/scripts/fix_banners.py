import re

def insert_banner(text, search_str, is_jsx=True):
    banner = """
              {decision?.bestVessel === "Unavailable" && (
                <div className="mx-6 mt-6 p-4 bg-slate-50 border border-slate-200 rounded-lg">
                  <p className="text-sm text-slate-700 font-medium">No feasible single-vessel plan exists for this cargo volume.</p>
                  <p className="text-xs text-slate-500 mt-1">
                    Multi-voyage planning required - approximately {Math.ceil(Number(requirements?.cargoMt || 0) / 170000)} voyages based on Capesize limits.
                  </p>
                </div>
              )}
"""
    if search_str in text:
        return text.replace(search_str, search_str + banner)
    return text

with open("src/pages/approval/HumanApproval.tsx", "r", encoding="utf-8") as f:
    text = f.read()
text = insert_banner(text, '<h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">')
with open("src/pages/approval/HumanApproval.tsx", "w", encoding="utf-8") as f:
    f.write(text)


with open("src/pages/recommendation/FinalRecommendation.tsx", "r", encoding="utf-8") as f:
    text = f.read()
banner2 = """
            {decision?.bestVessel === "Unavailable" && (
              <div className="mt-6 p-4 bg-slate-50 border border-slate-200 rounded-lg">
                <p className="text-sm text-slate-700 font-medium">No feasible single-vessel plan exists for this cargo volume.</p>
                <p className="text-xs text-slate-500 mt-1">
                  Multi-voyage planning required - approximately {Math.ceil(Number(requirements?.cargoMt || 0) / 170000)} voyages based on Capesize limits.
                </p>
              </div>
            )}
"""
text = text.replace('<RecommendationBadge rec={finalRec.recommendation} />', '<RecommendationBadge rec={finalRec.recommendation} />' + banner2)
with open("src/pages/recommendation/FinalRecommendation.tsx", "w", encoding="utf-8") as f:
    f.write(text)

# Let's also update the "Unavailable" pills to say "N/A - see note above" in these two files when appropriate.
# Since it's hard to be context-aware with regex, I'll just change the UnavailablePill component globally, 
# BUT wait! UnavailablePill might be used for things other than vessel! E.g. Date, Cost.
# In this scenario (345,600 MT), Cost is also unavailable. So "N/A - see note above" applies to Cost too!
