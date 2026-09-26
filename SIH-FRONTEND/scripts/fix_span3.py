import re

with open("src/pages/forecasting/FreightForecasting.tsx", "r", encoding="utf-8") as f:
    text = f.read()

# Replace the mangled span with the correct one
text = re.sub(
    r'<span className=\{[^}]*ext-2xl font-bold block \}>', 
    '<span className={`text-2xl font-bold block ${forecast.confidence.includes("Low") ? "text-orange-600" : "text-green-600"}`}>', 
    text
)

# And fix line 147 missing <main> issue if it exists (wait, tsc said "JSX element 'main' has no corresponding closing tag"!)
# Oh! The problem is I deleted the </main> tag when I did string slicing.

with open("src/pages/forecasting/FreightForecasting.tsx", "w", encoding="utf-8") as f:
    f.write(text)
