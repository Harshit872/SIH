"""
Scenario Evaluation Engine.

Compares "Book Now", "Wait 7 Days", and "Wait 14 Days" scenarios.
Does NOT fabricate future freight rates or risk profiles.
Marks scenarios as INSUFFICIENT_DATA if required inputs for future points are missing.
"""

from datetime import date, timedelta
from app.scenario_evaluation.schemas import ScenarioSchema, ScenarioComparisonReportSchema
from app.optimization.cost_engine.schemas import VoyageCostReportSchema
from app.optimization.risk_engine.schemas import RiskAssessmentReportSchema
from app.deadline_validator.schemas import ScheduleValidationReportSchema


def generate_scenario_comparison(
    current_date: date,
    # These would normally come from the cost, risk, and deadline modules
    # passing them through as None implies insufficient future forecasting models
    book_now_cost: VoyageCostReportSchema | None = None,
    book_now_schedule: ScheduleValidationReportSchema | None = None,
    book_now_risk: RiskAssessmentReportSchema | None = None,
) -> ScenarioComparisonReportSchema:
    
    scenarios = []
    
    # 1. Book Now
    missing_now = []
    if not book_now_cost or not book_now_cost.is_total_complete:
        missing_now.append("Complete current cost components")
    if not book_now_schedule or book_now_schedule.status.name == "INSUFFICIENT_DATA":
        missing_now.append("Complete schedule transit duration")
        
    scenarios.append(ScenarioSchema(
        name="Book Now",
        assumed_booking_date=current_date.isoformat(),
        is_evaluable=len(missing_now) == 0,
        cost_report=book_now_cost,
        schedule_report=book_now_schedule,
        risk_report=book_now_risk,
        missing_inputs=missing_now
    ))
    
    # 2. Wait 7 Days
    scenarios.append(ScenarioSchema(
        name="Wait 7 Days",
        assumed_booking_date=(current_date + timedelta(days=7)).isoformat(),
        is_evaluable=False,
        missing_inputs=[
            "Freight rate forecast (+7d)",
            "Bunker price forecast (+7d)",
            "Vessel availability forecast (+7d)"
        ]
    ))
    
    # 3. Wait 14 Days
    scenarios.append(ScenarioSchema(
        name="Wait 14 Days",
        assumed_booking_date=(current_date + timedelta(days=14)).isoformat(),
        is_evaluable=False,
        missing_inputs=[
            "Freight rate forecast (+14d)",
            "Bunker price forecast (+14d)",
            "Vessel availability forecast (+14d)"
        ]
    ))

    return ScenarioComparisonReportSchema(
        scenarios=scenarios,
        best_scenario="NONE (Recommendation engine not implemented)",
        note="Future scenarios cannot be fully evaluated without ML forecasting models. Displaying data gaps."
    )
