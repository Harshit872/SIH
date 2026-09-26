import sys
import os
import json
sys.path.append(os.path.abspath('SIH-BACKEND'))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

case1 = {
    "origin_port": "Port Hedland, Australia",
    "destination_port": "Visakhapatnam, India",
    "vessel_class": "Panamax",
    "cargo_type": "Iron Ore",
    "quantity_mt": 80000,
    "route_distance_nm": 5300,
    "bunker_price_usd_per_mt": 850,
    "bdi_value": 1500
}

case2 = {
    "origin_port": "Port Hedland, Australia",
    "destination_port": "Visakhapatnam, India",
    "vessel_class": "Panamax",
    "cargo_type": "Iron Ore",
    "quantity_mt": 80000,
    "route_distance_nm": 5300,
    "bunker_price_usd_per_mt": 850,
    "bdi_value": 10000
}

case3 = {
    "origin_port": "Port Hedland, Australia",
    "destination_port": "Visakhapatnam, India",
    "vessel_class": "Panamax",
    "cargo_type": "Iron Ore",
    "route_distance_nm": 5300,
    "bunker_price_usd_per_mt": 850,
    "bdi_value": 1500
}

for i, payload in enumerate([case1, case2, case3], 1):
    resp = client.post("/api/v1/forecast/freight-rate", json=payload)
    print(f"--- Case {i} ---")
    print("Status:", resp.status_code)
    print("Response:", json.dumps(resp.json(), indent=2))
