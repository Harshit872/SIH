import re

with open("SIH-BACKEND/app/api/routes.py", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace('current_user["sub"]', 'current_user["email"]')

with open("SIH-BACKEND/app/api/routes.py", "w", encoding="utf-8") as f:
    f.write(text)

