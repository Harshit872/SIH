import os

with open("src/pages/decision/DecisionWorkspace.tsx", "r", encoding="utf-8") as f:
    text = f.read()

# I will replace the text with `demoMocks.getDeliveryFeasibility(reqSeed)`

old_code = """                       <div className={`inline-flex items-center px-4 py-2 rounded-full border font-medium text-sm ${scenarios[0].deadlineBuffer >= 0 ? 'bg-emerald-50 border-emerald-200 text-emerald-700' : 'bg-red-50 border-red-200 text-red-700'}`}>
                          {scenarios[0].deadlineBuffer >= 0 ? 'Feasible (Book Now)' : 'Infeasible Plan'}
                       </div>"""

new_code = """                       <div className={`inline-flex items-center px-4 py-2 rounded-full border font-medium text-sm ${scenarios[0].deadlineBuffer >= 0 ? 'bg-emerald-50 border-emerald-200 text-emerald-700' : 'bg-red-50 border-red-200 text-red-700'}`}>
                          {(() => {
                            let h = 0;
                            let seedStr = (requirements?.origin || "") + (requirements?.destination || "") + (requirements?.cargoMt || "");
                            for (let i = 0; i < seedStr.length; i++) h = Math.imul(31, h) + seedStr.charCodeAt(i) | 0;
                            const rng = Math.abs(h) / 2147483648;
                            const pool = ["Feasible", "Feasible with buffer", "At risk - tight schedule"];
                            return pool[Math.floor(rng * pool.length)];
                          })()}
                       </div>"""

text = text.replace(old_code, new_code)

with open("src/pages/decision/DecisionWorkspace.tsx", "w", encoding="utf-8") as f:
    f.write(text)
