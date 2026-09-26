import os

with open(".env", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("http://localhost:8000", "http://localhost:8080")

with open(".env", "w", encoding="utf-8") as f:
    f.write(text)
