import pytest
from datetime import date
from app.optimization.cost_engine.engine import calculate_voyage_costs, CostStatus
from app.optimization.risk_engine.engine import assess_operational_risks, RiskStatus
from app.optimization.vessel_feasibility.evaluator import FeasibilityReport, VesselClassResult, FeasibilityStatus
from app.deadline_validator.engine import validate_schedule, ScheduleStatus
from app.scenario_evaluation.engine import generate_scenario_comparison

# --- Cost Engine Tests ---
def test_cost_engine_valid_inputs():
    report = calculate_voyage_costs(
        cargo_mt=50000,
        freight_rate_per_mt=15.0,
        freight_currency="USD",
        bunker_price_per_mt=600.0,
        bunker_consumption_mt=500.0,
        port_charges=25000.0,
        demurrage_rate_per_day=15000.0,
        demurrage_days=2.0,
        waiting_time_days=3.0,
        daily_hire_rate=12000.0
    )
    assert report.is_total_complete is True
    assert report.total_amount == (50000 * 15.0) + (600.0 * 500.0) + 25000.0 + (15000.0 * 2.0) + (3.0 * 12000.0)
    assert report.currency == "USD"
    for comp in report.components:
        assert comp.status == CostStatus.CALCULATED

def test_cost_engine_missing_inputs():
    report = calculate_voyage_costs(cargo_mt=50000, freight_rate_per_mt=15.0)
    assert report.is_total_complete is False
    assert report.total_amount == 50000 * 15.0  # Only partial total
    
    freight = next(c for c in report.components if c.name == "Freight")
    assert freight.status == CostStatus.CALCULATED
    
    bunker = next(c for c in report.components if c.name == "Fuel/Bunker")
    assert bunker.status == CostStatus.MISSING_INPUT


# --- Risk Engine Tests ---
def test_risk_engine_infeasible():
    feasibility = FeasibilityReport(
        origin="Port A", destination="Port B", commodity="Coal", cargo_mt=50000,
        vessel_class_results=[
            VesselClassResult(vessel_type="Panamax", overall_status=FeasibilityStatus.INFEASIBLE)
        ],
        summary="INFEASIBLE summary"
    )
    report = assess_operational_risks(feasibility_report=feasibility)
    vessel_risk = next(f for f in report.findings if f.factor == "Vessel/Port Compatibility")
    assert vessel_risk.status == RiskStatus.EVALUATED
    assert "No feasible vessel types" in vessel_risk.finding


def test_risk_engine_missing_data():
    feasibility = FeasibilityReport(
        origin="Port A", destination="Port B", commodity="Coal", cargo_mt=50000,
        summary="NOT_CONFIGURED: no data"
    )
    report = assess_operational_risks(feasibility_report=feasibility)
    vessel_risk = next(f for f in report.findings if f.factor == "Vessel/Port Compatibility")
    assert vessel_risk.status == RiskStatus.INSUFFICIENT_DATA


# --- Deadline Validator Tests ---
def test_deadline_validator_valid():
    # Transit data provided
    report = validate_schedule(
        laycan_str="01 Jun 2027 - 05 Jun 2027",
        delivery_date_str="2027-06-25",
        transit_days=10,
        loading_days=2,
        discharge_days=3
    )
    # Worst case: 05 Jun + 15 days = 20 Jun < 25 Jun
    assert report.status == ScheduleStatus.FEASIBLE

def test_deadline_validator_infeasible():
    report = validate_schedule(
        laycan_str="01 Jun 2027 - 05 Jun 2027",
        delivery_date_str="2027-06-15",
        transit_days=10,
        loading_days=3,
        discharge_days=3
    )
    # Worst case: 05 Jun + 16 days = 21 Jun > 15 Jun
    assert report.status == ScheduleStatus.INFEASIBLE

def test_deadline_validator_insufficient_data():
    # Missing transit days
    report = validate_schedule(
        laycan_str="01 Jun 2027 - 05 Jun 2027",
        delivery_date_str="2027-06-25"
    )
    assert report.status == ScheduleStatus.INSUFFICIENT_DATA


# --- Scenario Comparison Tests ---
def test_scenario_comparison():
    report = generate_scenario_comparison(current_date=date(2027, 6, 1))
    
    book_now = next(s for s in report.scenarios if s.name == "Book Now")
    assert book_now.is_evaluable is False
    assert len(book_now.missing_inputs) > 0
    
    wait_7 = next(s for s in report.scenarios if s.name == "Wait 7 Days")
    assert wait_7.is_evaluable is False
    assert "Freight rate forecast (+7d)" in wait_7.missing_inputs



