import requests
import json

base_url = "http://localhost:8000/api/v1"
headers = {"Content-Type": "application/json"}

# Use test payload
payload = {
    "origin": "Port Hedland/Dampier",
    "destination": "Paradip",
    "commodity": "Coal",
    "cargoMt": 80000,
    "deliveryDate": "2026-10-15",
    "contract": "Voyage Charter",
    "laycan": "01 Oct 2026 - 10 Oct 2026",
    "noOfVoyages": 1
}

print("Testing /evaluate_scenarios ...")
r = requests.post(f"{base_url}/evaluate_scenarios", json=payload, headers=headers)
print("Status:", r.status_code)
if r.status_code == 200:
    print(json.dumps(r.json(), indent=2))
else:
    print(r.text)

print("\nTesting /voyage/submit ...")
r2 = requests.post(f"{base_url}/voyage/submit", json=payload, headers=headers)
print("Status:", r2.status_code)
if r2.status_code == 202:
    print(json.dumps(r2.json(), indent=2))

