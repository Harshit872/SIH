from pydantic import BaseModel
from typing import List

class FreightForecastRequest(BaseModel):
    origin_port: str
    destination_port: str
    vessel_class: str
    cargo_type: str
    quantity_mt: float
    route_distance_nm: float
    bunker_price_usd_per_mt: float
    bdi_value: float

class FreightForecastResponse(BaseModel):
    predicted_freight_rate_usd_per_mt: float
    confidence_flag: str
    out_of_range_features: List[str]
    model_version: str
    is_model_trained_on_synthetic_data: bool
