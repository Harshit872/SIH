import sys
import os
import json
sys.path.append(os.path.abspath('SIH-BACKEND'))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print("--- IDLE CHECK TEST ---")
req = {
    "current_voyage_arrival_date": "2026-10-24",
    "next_laycan_start_date": "2026-10-28"
}
res = client.post("/api/v1/idle-check", json=req)
print("Request:", json.dumps(req))
print("Response:", json.dumps(res.json(), indent=2))
