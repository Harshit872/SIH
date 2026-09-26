import sys
import os
sys.path.append(os.path.abspath('SIH-BACKEND'))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Case 1: Normal
case1 = {
    "origin_port": "Gladstone, Australia",
    "destination_port": "Visakhapatnam, India",
    "vessel_class": "Capesize",
    "cargo_type": "Coal",
    "quantity_mt": 150000,
    "route_distance_nm": 5500,
    "bunker_price_usd_per_mt": 850.0,
    "bdi_value": 1500
}

# Case 2: BDI shock
case2 = {
    "origin_port": "Port Hedland, Australia",
    "destination_port": "Visakhapatnam, India",
    "vessel_class": "Panamax",
    "cargo_type": "Iron Ore",
    "quantity_mt": 75000,
    "route_distance_nm": 5300,
    "bunker_price_usd_per_mt": 800.0,
    "bdi_value": 10000
}

# Case 3: Bunker shock
case3 = {
    "origin_port": "Richards Bay, South Africa",
    "destination_port": "Visakhapatnam, India",
    "vessel_class": "Handysize",
    "cargo_type": "Coal",
    "quantity_mt": 25000,
    "route_distance_nm": 4600,
    "bunker_price_usd_per_mt": 2500.0,
    "bdi_value": 1200
}

for i, payload in enumerate([case1, case2, case3], 1):
    resp = client.post("/api/v1/forecast/freight-rate", json=payload)
    print(f"--- Case {i} ---")
    if resp.status_code == 200:
        data = resp.json()
        print(f"Pred: ")
        print(f"Flag: {data['confidence_flag']}")
        print(f"Out of range: {data['out_of_range_features']}")
    else:
        print(f"Error {resp.status_code}: {resp.text}")
