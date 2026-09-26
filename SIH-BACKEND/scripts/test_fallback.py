import sys
import os
import json
sys.path.append(os.path.abspath('SIH-BACKEND'))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

v_req1 = {"cargo_quantity_mt": 58000, "origin_port": "Gladstone", "destination_port": "Paradip"}
res = client.post("/api/v1/vessel-feasibility", json=v_req1)
print(f"Request (Borderline 58k MT):", json.dumps(v_req1))
print(f"Response:", json.dumps(res.json(), indent=2))
