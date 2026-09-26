import re

with open("src/pages/forecasting/FreightForecasting.tsx", "r", encoding="utf-8") as f:
    text = f.read()

# Replace the mangled span with the correct one
text = re.sub(
    r'<span className=\{[^}]*ext-2xl font-bold block \}>', 
    '<span className={	ext-2xl font-bold block }>', 
    text
)

with open("src/pages/forecasting/FreightForecasting.tsx", "w", encoding="utf-8") as f:
    f.write(text)
