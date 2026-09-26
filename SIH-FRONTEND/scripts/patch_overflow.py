import re

with open("src/pages/forecasting/FreightForecasting.tsx", "r", encoding="utf-8") as f:
    text = f.read()

# Fix Trend Card
trend_old = '''<div className="flex items-center gap-4 mt-2">
                <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                  {getTrendIcon(forecast.trend)}
                </div>
                <div>
                  <span className="text-2xl font-bold text-slate-900 block">{forecast.trend}</span>
                  <span className="text-sm text-slate-500">Over {horizon} horizon</span>
                </div>
              </div>'''

trend_new = '''<div className="flex items-center gap-3 xl:gap-4 mt-2">
                <div className="p-3 bg-slate-50 rounded-xl border border-slate-100 shrink-0">
                  {getTrendIcon(forecast.trend)}
                </div>
                <div className="min-w-0 flex-1">
                  <span className="text-xl xl:text-2xl font-bold text-slate-900 block truncate">{forecast.trend}</span>
                  <span className="text-sm text-slate-500 block truncate">Over {horizon} horizon</span>
                </div>
              </div>'''
text = text.replace(trend_old, trend_new)

# Fix Confidence Card
conf_old = '''<div className="flex items-center gap-4 mt-2">
                <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                  <ShieldCheck size={24} className={forecast.confidence.includes("Low") ? "text-orange-500" : "text-green-500"} />
                </div>
                <div>
                  <span className={	ext-2xl font-bold block }>
                    {forecast.confidence.includes("Low") ? "<50%" : "95%"}
                  </span>
                  <span className="text-sm text-slate-500">Model Reliability</span>
                </div>
              </div>'''

conf_new = '''<div className="flex items-center gap-3 xl:gap-4 mt-2">
                <div className="p-3 bg-slate-50 rounded-xl border border-slate-100 shrink-0">
                  <ShieldCheck size={24} className={forecast.confidence.includes("Low") ? "text-orange-500" : "text-green-500"} />
                </div>
                <div className="min-w-0 flex-1">
                  <span className={	ext-xl xl:text-2xl font-bold block truncate }>
                    {forecast.confidence.includes("Low") ? "<50%" : "95%"}
                  </span>
                  <span className="text-sm text-slate-500 block truncate">Model Reliability</span>
                </div>
              </div>'''
text = text.replace(conf_old, conf_new)

with open("src/pages/forecasting/FreightForecasting.tsx", "w", encoding="utf-8") as f:
    f.write(text)
