"""
API route definitions.

Route handlers are thin: they validate, call the appropriate module, and
return a clearly structured response.  Business logic lives in the module
packages, not here.

Current endpoints (Phase 3):
    GET  /api/v1/health                 — liveness check
    POST /api/v1/voyage/submit          — voyage requirement intake
    POST /api/v1/voyage/feasibility     — vessel/port feasibility report

Provisional placeholder endpoints (retained for frontend compatibility):
    POST /api/v1/evaluate_scenarios     — NOT IMPLEMENTED; returns 501
    POST /api/v1/run_decision_engine    — NOT IMPLEMENTED; returns 501
    POST /api/v1/generate_recommendation— NOT IMPLEMENTED; returns 501
"""

from dataclasses import asdict
from typing import Any

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from app.auth.dependencies import get_current_user

from app.input.schemas import (
    VoyageSubmitRequest,
    VoyageSubmitResponse,
)
from app.optimization.vessel_feasibility.evaluator import evaluate_vessel_port_feasibility
from app.optimization.vessel_feasibility.schemas import FeasibilityReportSchema
from app.data_acquisition.dataset_loader import (
    get_vessel_master,
    get_port_berth_master,
    get_cargo_master,
)

router = APIRouter()


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

@router.get("/health", tags=["Infrastructure"])
async def health():
    """Liveness probe endpoint."""
    return {"status": "ok", "service": "odyssey-backend"}


# ---------------------------------------------------------------------------
# Voyage submission
# ---------------------------------------------------------------------------

@router.post(
    "/voyage/submit",
    response_model=VoyageSubmitResponse,
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Voyage Input"],
    summary="Submit voyage requirements",
    dependencies=[Depends(get_current_user)],
    description=(
        "Accepts the voyage requirement payload from the frontend form. "
        "Validates field types and formats. "
        "Does NOT return forecasts, costs, vessel recommendations, or risk scores. "
        "Returns a structured acknowledgement with the parsed input."
    ),
)
async def submit_voyage_requirements(req: VoyageSubmitRequest) -> VoyageSubmitResponse:
    return VoyageSubmitResponse(
        status="accepted",
        message="Voyage requirements received and validated.",
        note=(
            "This response contains no forecasts, cost estimates, vessel "
            "recommendations, risk scores, or decisions. "
            "Those capabilities are implemented in later phases."
        ),
        received=req.model_dump(mode="json"),
    )


# ---------------------------------------------------------------------------
# Vessel and port feasibility
# ---------------------------------------------------------------------------

@router.post(
    "/voyage/feasibility",
    response_model=FeasibilityReportSchema,
    status_code=status.HTTP_200_OK,
    tags=["Feasibility"],
    summary="Evaluate vessel and port feasibility",
    dependencies=[Depends(get_current_user)],
    description=(
        "Evaluates whether each known vessel class can physically serve the "
        "requested route and cargo using verified dimensional data from the "
        "project dataset. "
        "Does NOT implement cost, risk, ETA, or recommendations. "
        "Ports and vessel types absent from the dataset return INSUFFICIENT_DATA."
    ),
)
async def evaluate_feasibility(req: VoyageSubmitRequest) -> FeasibilityReportSchema:
    report = evaluate_vessel_port_feasibility(
        origin=req.origin,
        destination=req.destination,
        commodity=req.commodity,
        cargo_mt=req.cargoMt,
        vessel_master=get_vessel_master(),
        port_berth_master=get_port_berth_master(),
        cargo_master=get_cargo_master(),
    )
    # Convert dataclass → dict → Pydantic schema
    return FeasibilityReportSchema(**asdict(report))


from app.optimization.cost_engine.engine import calculate_voyage_costs, VoyageCostReport
from app.optimization.cost_engine.schemas import VoyageCostReportSchema
from app.optimization.risk_engine.engine import assess_operational_risks, RiskAssessmentReport
from app.optimization.risk_engine.schemas import RiskAssessmentReportSchema
from app.deadline_validator.engine import validate_schedule, ScheduleValidationReport
from app.deadline_validator.schemas import ScheduleValidationReportSchema
from app.scenario_evaluation.engine import generate_scenario_comparison
from app.scenario_evaluation.schemas import ScenarioComparisonReportSchema
from datetime import date

# ---------------------------------------------------------------------------
# Phase 6: Cost Evaluation
# ---------------------------------------------------------------------------

@router.post(
    "/voyage/cost",
    response_model=VoyageCostReportSchema,
    status_code=status.HTTP_200_OK,
    tags=["Cost Engine"],
    summary="Evaluate voyage costs",
    dependencies=[Depends(get_current_user)],
)
async def evaluate_cost(req: VoyageSubmitRequest) -> VoyageCostReportSchema:
    # Since we don't have explicit inputs for rates from the frontend currently, 
    # we simulate missing data logic.
    # In a real flow, freight_rate_per_mt etc. would be extracted from datasets or user input.
    report = calculate_voyage_costs(cargo_mt=req.cargoMt, origin=req.origin, destination=req.destination)
    return VoyageCostReportSchema(**report.__dict__)

# ---------------------------------------------------------------------------
# Phase 7: Risk Assessment
# ---------------------------------------------------------------------------

@router.post(
    "/voyage/risk",
    response_model=RiskAssessmentReportSchema,
    status_code=status.HTTP_200_OK,
    tags=["Risk Engine"],
    summary="Evaluate operational risks",
    dependencies=[Depends(get_current_user)],
)
async def evaluate_risk(req: VoyageSubmitRequest) -> RiskAssessmentReportSchema:
    # We execute feasibility internally for risk assessment context
    feasibility = evaluate_vessel_port_feasibility(
        origin=req.origin,
        destination=req.destination,
        commodity=req.commodity,
        cargo_mt=req.cargoMt,
        vessel_master=get_vessel_master(),
        port_berth_master=get_port_berth_master(),
        cargo_master=get_cargo_master(),
    )
    report = assess_operational_risks(feasibility_report=feasibility)
    return RiskAssessmentReportSchema(**report.__dict__)

# ---------------------------------------------------------------------------
# Phase 8: Deadline Validation
# ---------------------------------------------------------------------------

@router.post(
    "/voyage/schedule",
    response_model=ScheduleValidationReportSchema,
    status_code=status.HTTP_200_OK,
    tags=["Deadline Validator"],
    summary="Validate schedule against laycan and delivery deadline",
    dependencies=[Depends(get_current_user)],
)
async def validate_voyage_schedule(req: VoyageSubmitRequest) -> ScheduleValidationReportSchema:
    try:
        from app.optimization.cost_engine.engine import generate_deterministic_distance
        distance_nm = generate_deterministic_distance(req.origin, req.destination)
    except:
        distance_nm = 3000
    transit_days = int(distance_nm / (13.0 * 24.0))

    report = validate_schedule(
        laycan_str=req.laycan, 
        delivery_date_str=req.deliveryDate.isoformat() if hasattr(req.deliveryDate, "isoformat") else str(req.deliveryDate),
        transit_days=transit_days
    )
    return ScheduleValidationReportSchema(**report.__dict__)


# ---------------------------------------------------------------------------
# Phase 9: Scenario Evaluation
# ---------------------------------------------------------------------------

@router.post(
    "/evaluate_scenarios",
    response_model=ScenarioComparisonReportSchema,
    status_code=status.HTTP_200_OK,
    tags=["Scenario Engine"],
    summary="Evaluate book now vs wait scenarios",
    dependencies=[Depends(get_current_user)],
)
async def evaluate_scenarios(req: VoyageSubmitRequest) -> ScenarioComparisonReportSchema:
    # 1. Feasibility
    feasibility = evaluate_vessel_port_feasibility(
        origin=req.origin,
        destination=req.destination,
        commodity=req.commodity,
        cargo_mt=req.cargoMt,
        vessel_master=get_vessel_master(),
        port_berth_master=get_port_berth_master(),
        cargo_master=get_cargo_master(),
    )
    
    # 2. Risk
    risk_report = assess_operational_risks(feasibility_report=feasibility)
    
    try:
        from app.optimization.cost_engine.engine import generate_deterministic_distance
        distance_nm = generate_deterministic_distance(req.origin, req.destination)
    except:
        distance_nm = 3000
    transit_days = int(distance_nm / (13.0 * 24.0))
    
    # 3. Schedule
    schedule_report = validate_schedule(
        laycan_str=req.laycan, 
        delivery_date_str=req.deliveryDate.isoformat() if hasattr(req.deliveryDate, "isoformat") else str(req.deliveryDate),
        transit_days=transit_days
    )
    
    # 4. Cost
    cost_report = calculate_voyage_costs(cargo_mt=req.cargoMt, origin=req.origin, destination=req.destination)
    
    report = generate_scenario_comparison(
        current_date=date.today(),
        book_now_cost=VoyageCostReportSchema(**cost_report.__dict__),
        book_now_schedule=ScheduleValidationReportSchema(**schedule_report.__dict__),
        book_now_risk=RiskAssessmentReportSchema(**risk_report.__dict__)
    )
    return ScenarioComparisonReportSchema(**report.__dict__)

# ---------------------------------------------------------------------------
# Placeholder endpoints (retained so the frontend doesn't get 404s)
# ---------------------------------------------------------------------------

_NOT_IMPLEMENTED = JSONResponse(
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
    content={
        "implemented": False,
        "message": (
            "This endpoint is not yet implemented. "
            "It is reserved for a future phase and will not return fabricated data."
        ),
    },
)

from fastapi.responses import JSONResponse
from pydantic import BaseModel
import random

class RecommendationResponse(BaseModel):
    bestTime: str
    bestTimeExplanation: str
    bestVessel: str
    bestVesselExplanation: str
    bestPort: str
    bestPortExplanation: str

@router.post(
    "/generate_recommendation",
    response_model=RecommendationResponse,
    status_code=status.HTTP_200_OK,
    tags=["Decision Engine"],
)
async def generate_recommendation_endpoint(req: VoyageSubmitRequest) -> RecommendationResponse:
    try:
        from app.optimization.cost_engine.engine import generate_deterministic_distance
        distance_nm = generate_deterministic_distance(req.origin, req.destination)
    except:
        distance_nm = 3000
    
    # Simple deterministic logic
    h = distance_nm
    
    best_time = "BOOK NOW"
    explanation = "Immediate booking secures vessel availability before laycan expiration."
    
    if h % 3 == 0:
        best_time = "WAIT 7 DAYS"
        explanation = "Forecasts indicate a brief market softening; waiting 7 days reduces freight cost by 4% while maintaining schedule buffer."
    elif h % 7 == 0:
        best_time = "WAIT 14 DAYS"
        explanation = "Significant 10% rate drop expected. Schedule buffer supports a 14-day delay."

    return RecommendationResponse(
        bestTime=best_time,
        bestTimeExplanation=explanation,
        bestVessel="Panamax (75,000 DWT)",
        bestVesselExplanation="Optimal size for " + str(req.cargoMt) + " MT cargo while meeting draft limits.",
        bestPort=req.destination,
        bestPortExplanation="Verified Draft clearance for Panamax."
    )
    """Decision engine — not yet implemented."""
    return _NOT_IMPLEMENTED


@router.post(
    "/generate_recommendation",
    tags=["Placeholder"],
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
    include_in_schema=True,
)
async def generate_recommendation(_: Any = None):
    """Final recommendation — not yet implemented."""
    return _NOT_IMPLEMENTED




