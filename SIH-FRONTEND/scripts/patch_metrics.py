import os
import re

with open("SIH-FRONTEND/src/pages/forecasting/FreightForecasting.tsx", "r", encoding="utf-8") as f:
    text = f.read()

# Replace the entire Side Metrics div
start_idx = text.find('{/* Side Metrics (Trend & Confidence) */}')
end_idx = text.find('</main>', start_idx)

new_side_metrics = '''{/* Side Metrics (Trend & Confidence) */}
          <div className="flex flex-col gap-6">
            
            {/* Trend Card */}
            <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6 flex flex-col">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-4">Trend</h3>
              <div className="flex items-center gap-4 mt-2">
                <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                  {getTrendIcon(forecast.trend)}
                </div>
                <div>
                  <span className="text-2xl font-bold text-slate-900 block">{forecast.trend}</span>
                  <span className="text-sm text-slate-500">Over {horizon} horizon</span>
                </div>
              </div>
              <div className="mt-auto pt-6">
                <p className="text-xs text-slate-400 bg-slate-50 p-2.5 rounded-md border border-slate-100">
                  Computed by feeding future BDI/Bunker projections (if provided) into the LightGBM model. 
                  Currently assumes static market conditions over the horizon.
                </p>
              </div>
            </div>

            {/* Confidence Card */}
            <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6 flex flex-col flex-1">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-4">Confidence</h3>
              <div className="flex items-center gap-4 mt-2">
                <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                  <ShieldCheck size={24} className={forecast.confidence.includes("Low") ? "text-orange-500" : "text-green-500"} />
                </div>
                <div>
                  <span className={	ext-2xl font-bold block }>
                    {forecast.confidence.includes("Low") ? "<50%" : "95%"}
                  </span>
                  <span className="text-sm text-slate-500">Model Reliability</span>
                </div>
              </div>
              <div className="mt-auto pt-6">
                <p className="text-xs text-slate-400 bg-slate-50 p-2.5 rounded-md border border-slate-100">
                  {forecast.confidence}
                </p>
              </div>
            </div>

          </div>
        </div>
'''

if start_idx != -1 and end_idx != -1:
    text = text[:start_idx] + new_side_metrics + "\n      " + text[end_idx:]
    with open("SIH-FRONTEND/src/pages/forecasting/FreightForecasting.tsx", "w", encoding="utf-8") as f:
        f.write(text)
