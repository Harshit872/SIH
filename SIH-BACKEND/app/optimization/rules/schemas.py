from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import date, timedelta

# 1. Vessel Feasibility
class VesselFeasibilityRequest(BaseModel):
    cargo_quantity_mt: float
    origin_port: str
    destination_port: str

class VesselFeasibilityItem(BaseModel):
    vessel_class: str
    feasible: bool
    reason: str

class NearestFeasibleOption(BaseModel):
    vessel_class: str
    mode: str
    wasted_capacity_mt: float
    note: str

class VesselFeasibilityResponse(BaseModel):
    vessels: List[VesselFeasibilityItem]
    nearest_feasible_option: Optional[NearestFeasibleOption] = None

# 2. Voyage Cost
class VoyageCostRequest(BaseModel):
    origin_port: str
    destination_port: str
    freight_rate_usd_per_mt: float
    quantity_mt: float
    bunker_price_usd_per_mt: float
    route_distance_nm: float
    vessel_class: str
    port_turnaround_days: float
    demurrage_rate: float

class VoyageCostResponse(BaseModel):
    freight_cost_usd: float
    bunker_cost_usd: float
    port_cost_usd: float
    total_cost_usd: float
    port_cost_source: str
    notes: List[str]

# 3. Deadline Check
class DeadlineCheckRequest(BaseModel):
    route_distance_nm: float
    vessel_speed_knots: float
    port_turnaround_days: float
    laycan_start_date: date
    required_delivery_date: date

class DeadlineCheckResponse(BaseModel):
    estimated_arrival_date: date
    feasible: bool
    buffer_days: int

# 4. Risk Score
class RiskScoreRequest(BaseModel):
    freight_rate_confidence_flag: str
    deadline_buffer_days: int
    port_cost_source: str
    vessel_feasibility_mode: str  # "direct_feasible", "deadfreight", "infeasible"

class RiskFactor(BaseModel):
    factor: str
    points: int
    description: str

class RiskScoreResponse(BaseModel):
    risk_score: int
    risk_tier: str
    breakdown: List[RiskFactor]

# 5. What-If Engine
class ScenarioInputOverride(BaseModel):
    bunker_price_usd_per_mt: Optional[float] = None
    bdi_value: Optional[float] = None

class WhatIfRequest(BaseModel):
    origin_port: str
    destination_port: str
    vessel_class: str
    cargo_type: str
    quantity_mt: float
    route_distance_nm: float
    bunker_price_usd_per_mt: float
    bdi_value: float
    port_turnaround_days: float
    demurrage_rate: float
    laycan_start_date: date
    required_delivery_date: date
    # Optional scenario overrides if user provides them
    scenario_overrides: Optional[Dict[str, ScenarioInputOverride]] = None

class ScenarioResult(BaseModel):
    scenario_name: str
    laycan_start_date: date
    estimated_arrival_date: date
    total_cost_usd: float
    deadline_feasible: bool
    risk_tier: str
    risk_score: int
    assumptions_noted: List[str]

class WhatIfResponse(BaseModel):
    scenarios: List[ScenarioResult]
    recommended_scenario: Optional[str]
    recommendation_basis: str
import json
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ApprovePlanRequest(BaseModel):
    user_decision: str  # "approve" or "modify"
    voyage_details: Dict[str, Any]
    what_if_response: Dict[str, Any]
    modified_scenario: Optional[str] = None # e.g. "Wait 7 Days"

class ApprovedPlanResponse(BaseModel):
    plan_id: str
    status: str
    chosen_scenario: str
    total_cost_usd: float
    risk_tier: str

class IdleCheckRequest(BaseModel):
    current_voyage_arrival_date: date
    next_laycan_start_date: Optional[date] = None

class IdleCheckResponse(BaseModel):
    idle_days: Optional[int]
    status: str
    note: str
