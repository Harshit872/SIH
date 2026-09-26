import re

with open("src/pages/finalplan/FinalPlan.tsx", "r", encoding="utf-8") as f:
    text = f.read()

# Update the Unavailable message in FinalPlan to be "N/A - see note above"
text = text.replace('<span className="text-xs italic text-slate-400">Unavailable</span>', '<span className="text-xs italic text-slate-400">N/A - see note above</span>')

# Add the explanatory banner if vessel is unavailable
target = '<div className="p-6 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">'
banner = """
              {finalDecision.bestVessel === "Unavailable" && (
                <div className="px-6 py-4 bg-slate-50 border-y border-slate-100">
                  <p className="text-sm text-slate-700 font-medium">No feasible single-vessel plan exists for this cargo volume.</p>
                  <p className="text-xs text-slate-500 mt-1">
                    Multi-voyage planning required - approximately {Math.ceil(Number(requirements?.cargoMt || 0) / 170000)} voyages based on Capesize limits.
                  </p>
                </div>
              )}
              <div className="p-6 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">"""

text = text.replace(target, banner)

with open("src/pages/finalplan/FinalPlan.tsx", "w", encoding="utf-8") as f:
    f.write(text)
