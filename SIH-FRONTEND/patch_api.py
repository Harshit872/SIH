import os

with open("src/services/api.ts", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("http://localhost:8000/api/v1", "http://localhost:8080/api/v1")

with open("src/services/api.ts", "w", encoding="utf-8") as f:
    f.write(text)
