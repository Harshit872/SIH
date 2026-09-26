import os

with open("src/pages/forecasting/FreightForecasting.tsx", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace(
    '{requirements?.origin || "Unknown"} <ArrowRight size={12} className="text-slate-400" /> {requirements?.destination || "Unknown"}',
    '{requirements?.origin || "Unknown"} <span className="text-slate-400 px-1">&rarr;</span> {requirements?.destination || "Unknown"}'
)

with open("src/pages/forecasting/FreightForecasting.tsx", "w", encoding="utf-8") as f:
    f.write(text)
