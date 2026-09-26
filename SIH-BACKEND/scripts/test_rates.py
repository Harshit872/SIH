import sys
import os
import json
sys.path.append(os.path.abspath('SIH-BACKEND'))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

req1 = {
    "origin_port": "Newcastle", "destination_port": "Haldia",
    "vessel_class": "Panamax", "cargo_type": "Coking Coal",
    "quantity_mt": 45000, "route_distance_nm": 5000,
    "bunker_price_usd_per_mt": 850, "bdi_value": 1500,
    "port_turnaround_days": 4.5, "demurrage_rate": 20000,
    "laycan_start_date": "2026-10-01", "required_delivery_date": "2026-10-25"
}

req2 = {
    "origin_port": "Newcastle", "destination_port": "Haldia",
    "vessel_class": "Panamax", "cargo_type": "Coking Coal",
    "quantity_mt": 456700, "route_distance_nm": 5000,
    "bunker_price_usd_per_mt": 850, "bdi_value": 1500,
    "port_turnaround_days": 4.5, "demurrage_rate": 20000,
    "laycan_start_date": "2026-10-01", "required_delivery_date": "2026-10-25"
}

r1 = client.post("/api/v1/forecast/freight-rate", json=req1).json()
r2 = client.post("/api/v1/forecast/freight-rate", json=req2).json()

print("R1 (Normal Cargo):", r1['predicted_freight_rate_usd_per_mt'], "| Confidence:", r1['confidence_flag'])
print("R2 (Massive Cargo):", r2['predicted_freight_rate_usd_per_mt'], "| Confidence:", r2['confidence_flag'])
