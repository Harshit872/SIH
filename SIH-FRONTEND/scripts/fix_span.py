import re

with open("src/pages/forecasting/FreightForecasting.tsx", "r", encoding="utf-8") as f:
    text = f.read()

# I will just replace the specific tab byte with backtick t
text = text.replace('className={	ext-2xl font-bold block }', 'className={	ext-2xl font-bold block }')

with open("src/pages/forecasting/FreightForecasting.tsx", "w", encoding="utf-8") as f:
    f.write(text)
