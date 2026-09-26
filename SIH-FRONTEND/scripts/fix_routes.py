import re
with open("SIH-BACKEND/app/api/routes.py", "r") as f:
    text = f.read()
# Replace the old router patch
text = re.sub(r'from app\.optimization\.rules\.schemas import.*', '', text, flags=re.DOTALL)
with open("SIH-BACKEND/app/api/routes.py", "w") as f:
    f.write(text)

router_patch = '''
from app.optimization.rules.schemas import (
    VesselFeasibilityRequest, VesselFeasibilityResponse,
    VoyageCostRequest, VoyageCostResponse,
    DeadlineCheckRequest, DeadlineCheckResponse
)
from app.optimization.rules.vessel_feasibility import evaluate_vessel_feasibility
from app.optimization.rules.cost_engine import calculate_voyage_cost
from app.optimization.rules.deadline_validator import check_deadline

@router.post("/vessel-feasibility", response_model=VesselFeasibilityResponse, tags=["Rules"])
async def vessel_feasibility(req: VesselFeasibilityRequest):
    res = evaluate_vessel_feasibility(req.cargo_quantity_mt, req.origin_port, req.destination_port)
    return {"vessels": res}

@router.post("/voyage-cost", response_model=VoyageCostResponse, tags=["Rules"])
async def voyage_cost(req: VoyageCostRequest):
    res = calculate_voyage_cost(
        req.origin_port, req.destination_port,
        req.freight_rate_usd_per_mt, req.quantity_mt, req.bunker_price_usd_per_mt,
        req.route_distance_nm, req.vessel_class, req.port_turnaround_days, req.demurrage_rate
    )
    return res

@router.post("/deadline-check", response_model=DeadlineCheckResponse, tags=["Rules"])
async def deadline_check(req: DeadlineCheckRequest):
    res = check_deadline(
        req.route_distance_nm, req.vessel_speed_knots, req.port_turnaround_days,
        req.laycan_start_date, req.required_delivery_date
    )
    return res
'''
with open("SIH-BACKEND/app/api/routes.py", "a") as f:
    f.write(router_patch)
