from datetime import date, timedelta
from app.scenario_evaluation.schemas import ScenarioComparisonReportSchema, ScenarioSchema
from app.optimization.cost_engine.schemas import VoyageCostReportSchema
from app.deadline_validator.schemas import ScheduleValidationReportSchema
from app.optimization.risk_engine.schemas import RiskAssessmentReportSchema

def generate_scenario_comparison(
    current_date: date,
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
    
    # Generate derived values for Wait 7 and 14 days
    import copy
    
    # 2. Wait 7 Days
    wait_7_cost = copy.deepcopy(book_now_cost) if book_now_cost else None
    if wait_7_cost and wait_7_cost.total_amount:
        wait_7_cost.total_amount *= 0.96  # Simulate 4% freight drop
        
    wait_7_sched = copy.deepcopy(book_now_schedule) if book_now_schedule else None
    if wait_7_sched and wait_7_sched.buffer_days is not None:
        wait_7_sched.buffer_days -= 7  # 7 days later
        
    wait_7_risk = copy.deepcopy(book_now_risk) if book_now_risk else None
    if wait_7_risk and wait_7_risk.score:
        wait_7_risk.score += 15  # Risk goes up due to tightness
    
    scenarios.append(ScenarioSchema(
        name="Wait 7 Days",
        assumed_booking_date=(current_date + timedelta(days=7)).isoformat(),
        is_evaluable=len(missing_now) == 0,
        missing_inputs=[],
        cost_report=wait_7_cost,
        schedule_report=wait_7_sched,
        risk_report=wait_7_risk
    ))
    
    # 3. Wait 14 Days
    wait_14_cost = copy.deepcopy(book_now_cost) if book_now_cost else None
    if wait_14_cost and wait_14_cost.total_amount:
        wait_14_cost.total_amount *= 0.90  # Simulate 10% freight drop
        
    wait_14_sched = copy.deepcopy(book_now_schedule) if book_now_schedule else None
    if wait_14_sched and wait_14_sched.buffer_days is not None:
        wait_14_sched.buffer_days -= 14
        
    wait_14_risk = copy.deepcopy(book_now_risk) if book_now_risk else None
    if wait_14_risk and wait_14_risk.score:
        wait_14_risk.score += 35
        
    scenarios.append(ScenarioSchema(
        name="Wait 14 Days",
        assumed_booking_date=(current_date + timedelta(days=14)).isoformat(),
        is_evaluable=len(missing_now) == 0,
        missing_inputs=[],
        cost_report=wait_14_cost,
        schedule_report=wait_14_sched,
        risk_report=wait_14_risk
    ))
    
    return ScenarioComparisonReportSchema(
        base_date=current_date.isoformat(),
        scenarios=scenarios
    )
