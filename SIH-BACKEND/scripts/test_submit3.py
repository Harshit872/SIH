from fastapi import FastAPI
from app.main import app

import json
from fastapi.testclient import TestClient
client = TestClient(app)
# Need to override get_current_user
from app.auth.dependencies import get_current_user
app.dependency_overrides[get_current_user] = lambda: {"id": 1, "email": "test@test.com"}

payload = {
    "origin": "Gladstone",
    "destination": "West Australia",
    "commodity": "Iron Ore",
    "cargoMt": 56789,
    "deliveryDate": "2026-10-15",
    "contract": "Bareboat Charter",
    "laycan": "21 Oct 2026 - 27 Oct 2026",
    "noOfVoyages": 2
}
response = client.post("/api/v1/voyage/submit", json=payload)
print(response.status_code)
print(json.dumps(response.json(), indent=2))
