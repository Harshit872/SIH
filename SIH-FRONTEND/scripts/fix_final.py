import re

with open("src/pages/finalplan/FinalPlan.tsx", "r", encoding="utf-8") as f:
    text = f.read()

# Replace the grid array
old_array = """                [
                  ["DWT (mt)",        finalDecision.bestVessel["DWT (mt)"]],
                  ["Draft (m)",       finalDecision.bestVessel["SSW Draft (m)"]],
                  ["LOA (m)",         finalDecision.bestVessel["LOA (m)"]],
                  ["Beam (m)",        finalDecision.bestVessel["Beam (m)"]],
                  ["Grain Cap (cbm)", finalDecision.bestVessel["Grain Capacity (cbm)"]],
                  ["Laden Spd (kn)",  finalDecision.bestVessel["Laden Speed (kn)"]],
                  ["Ballast Spd (kn)",finalDecision.bestVessel["Ballast Speed (kn)"]],
                  ["Max Age (yr)",    finalDecision.bestVessel["Max Age (yr)"]],
                  ["Geared",          String(finalDecision.bestVessel["Geared"])],
                ]"""

new_array = """                [
                  ["DWT (mt)",        finalDecision.bestVessel !== "Unavailable" ? finalDecision.bestVessel["DWT (mt)"] : undefined],
                  ["Draft (m)",       finalDecision.bestVessel !== "Unavailable" ? finalDecision.bestVessel["SSW Draft (m)"] : undefined],
                  ["LOA (m)",         finalDecision.bestVessel !== "Unavailable" ? finalDecision.bestVessel["LOA (m)"] : undefined],
                  ["Beam (m)",        finalDecision.bestVessel !== "Unavailable" ? finalDecision.bestVessel["Beam (m)"] : undefined],
                  ["Grain Cap (cbm)", finalDecision.bestVessel !== "Unavailable" ? finalDecision.bestVessel["Grain Capacity (cbm)"] : undefined],
                  ["Laden Spd (kn)",  finalDecision.bestVessel !== "Unavailable" ? finalDecision.bestVessel["Laden Speed (kn)"] : undefined],
                  ["Ballast Spd (kn)",finalDecision.bestVessel !== "Unavailable" ? finalDecision.bestVessel["Ballast Speed (kn)"] : undefined],
                  ["Max Age (yr)",    finalDecision.bestVessel !== "Unavailable" ? finalDecision.bestVessel["Max Age (yr)"] : undefined],
                  ["Geared",          finalDecision.bestVessel !== "Unavailable" ? (finalDecision.bestVessel["Geared"] ? "Yes" : "No") : undefined],
                ]"""

text = text.replace(old_array, new_array)

# Also fix the mapping to render UnavailablePill if value is undefined
old_map = """                ].map(([label, val]) => (
                  <div key={String(label)} className="bg-slate-50 border border-slate-100 rounded-lg px-3 py-2.5">
                    <span className="text-xs text-slate-500 font-medium block">{label}</span>
                    <span className="text-sm font-semibold text-slate-900">{String(val)}</span>
                  </div>
                ))}"""

new_map = """                ].map(([label, val]) => (
                  <div key={String(label)} className="bg-slate-50 border border-slate-100 rounded-lg px-3 py-2.5">
                    <span className="text-xs text-slate-500 font-medium block mb-0.5">{label}</span>
                    {val !== undefined ? (
                      <span className="text-sm font-semibold text-slate-900">{String(val)}</span>
                    ) : (
                      <span className="text-xs italic text-slate-400">Unavailable</span>
                    )}
                  </div>
                ))}"""
text = text.replace(old_map, new_map)

# Also fix "Approved By" to use real user identity instead of hardcoded placeholder
# I need to add useAuth to FinalPlan.tsx if it's not there!
# Wait, user_email is saved in approvalResult?
# The Approval page sends `user_email: user.sub`. We can display that!

with open("src/pages/finalplan/FinalPlan.tsx", "w", encoding="utf-8") as f:
    f.write(text)
