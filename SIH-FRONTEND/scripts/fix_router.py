import re
with open("SIH-BACKEND/app/api/routes.py", "r") as f:
    text = f.read()

text = re.sub(r'return \{"vessels": res\}', 'return res', text)

with open("SIH-BACKEND/app/api/routes.py", "w") as f:
    f.write(text)
