import urllib.request
import json

url = "http://localhost:8000/api/v1/evaluate_scenarios"
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
data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        print("Status:", response.status)
        print(json.dumps(json.loads(response.read().decode()), indent=2))
except urllib.error.HTTPError as e:
    print("HTTPError:", e.code)
    print(e.read().decode())
except Exception as e:
    print(e)
