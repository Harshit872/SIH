import re

with open("src/pages/decision/DecisionWorkspace.tsx", "r", encoding="utf-8") as f:
    text = f.read()

# Replace the layout wrapper
text = text.replace('<div className="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-in fade-in slide-in-from-bottom-6 duration-700 delay-150">', '<div className="space-y-6 animate-in fade-in slide-in-from-bottom-6 duration-700 delay-150">')

# Remove the lg:col-span-2 wrapper from Explore Timing Options
text = text.replace('<div className="lg:col-span-2 space-y-6">', '<div className="w-full">')

# Split the side info into 3 equal cards in a new grid row
# The old side info starts with:
# <div className="space-y-6">
#   {/* Vessel & Port Recommendation */}
#   <div className="bg-white border ...

# We want it to be:
# <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full">

text = text.replace('            {/* Side Info: Vessel Recommendation & Delivery Feasibility */}\n            <div className="space-y-6">', '            {/* Bottom Info Row */}\n            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">')

# Now we need to split the "System Recommendations" card into two separate cards (Vessel and Port)
# We will do a manual string replace to refactor this block.
old_system_rec_start = """              {/* Vessel & Port Recommendation */}
              <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
                <div className="bg-slate-50 border-b border-slate-100 p-5 flex items-center gap-3">
                  <div className="p-2 bg-emerald-100 text-emerald-700 rounded-lg">
                    <Anchor size={20} />
                  </div>
                  <h3 className="font-semibold text-slate-900">System Recommendations</h3>
                </div>
                <div className="p-6 space-y-6">
                  {/* Vessel Options */}
                  <div>
                    <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">Vessel Options</h4>"""

new_vessel_card = """              {/* Vessel Recommendation */}
              <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden flex flex-col">
                <div className="bg-slate-50 border-b border-slate-100 p-5 flex items-center gap-3">
                  <div className="p-2 bg-emerald-100 text-emerald-700 rounded-lg">
                    <Anchor size={20} />
                  </div>
                  <h3 className="font-semibold text-slate-900">Vessel Options</h3>
                </div>
                <div className="p-6 flex-1">"""

text = text.replace(old_system_rec_start, new_vessel_card)

# Now find where Vessel Options ends and Port Options begins
old_port_options_start = """                  </div>

                  {/* Port Options */}
                  <div>
                    <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">Port Options</h4>"""

new_port_card = """                </div>
              </div>

              {/* Port Options */}
              <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden flex flex-col">
                <div className="bg-slate-50 border-b border-slate-100 p-5 flex items-center gap-3">
                  <div className="p-2 bg-emerald-100 text-emerald-700 rounded-lg">
                    <Anchor size={20} />
                  </div>
                  <h3 className="font-semibold text-slate-900">Port Options</h3>
                </div>
                <div className="p-6 flex-1">"""

text = text.replace(old_port_options_start, new_port_card)

# Close the port card div
old_port_end = """                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Delivery Feasibility */}"""

new_port_end = """                      </div>
                    )}
                </div>
              </div>

              {/* Delivery Feasibility */}"""

text = text.replace(old_port_end, new_port_end)

with open("src/pages/decision/DecisionWorkspace.tsx", "w", encoding="utf-8") as f:
    f.write(text)
