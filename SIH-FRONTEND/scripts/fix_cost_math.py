import os

with open("src/utils/demoMocks.ts", "r", encoding="utf-8") as f:
    text = f.read()

# I will update getCostBreakdown to pass delayCost and subtract it from port/bunker or just subtract it so the 4 values sum to total.
# Wait, getCostBreakdown doesn't have delayCost currently.
# Let's rewrite demoMocks to just include delayCost in the cost breakdown!

old_breakdown = """  getCostBreakdown: (reqSeed: string, scenario: string) => {
     const total = demoMocks.getTotalCost(reqSeed, scenario);
     const freight = Math.round(total * 0.75);
     const bunker = Math.round(total * 0.18);
     const port = total - freight - bunker;
     return { freight, bunker, port };
  },"""

new_breakdown = """  getCostBreakdown: (reqSeed: string, scenario: string) => {
     const total = demoMocks.getTotalCost(reqSeed, scenario);
     const delayCost = demoMocks.getWaitingCost(reqSeed, scenario);
     const remaining = total - delayCost;
     const freight = Math.round(remaining * 0.75);
     const bunker = Math.round(remaining * 0.18);
     const port = remaining - freight - bunker;
     return { freight, bunker, port, delayCost };
  },"""

text = text.replace(old_breakdown, new_breakdown)

with open("src/utils/demoMocks.ts", "w", encoding="utf-8") as f:
    f.write(text)

# Also update DecisionLogic.ts to use costBreakdown.delayCost
with open("src/utils/DecisionLogic.ts", "r", encoding="utf-8") as f:
    dl_text = f.read()

dl_text = dl_text.replace(
'''    const costBreakdown = demoMocks.getCostBreakdown(reqSeed, scenario);
    const delayCost = demoMocks.getWaitingCost(reqSeed, scenario);''',
'''    const costBreakdown = demoMocks.getCostBreakdown(reqSeed, scenario);'''
)
dl_text = dl_text.replace('delayCost: delayCost', 'delayCost: costBreakdown.delayCost')

with open("src/utils/DecisionLogic.ts", "w", encoding="utf-8") as f:
    f.write(dl_text)

