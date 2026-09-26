from datetime import timedelta
from app.optimization.freight_forecasting.ml_service import predict_freight_rate
from app.optimization.rules.vessel_feasibility import evaluate_vessel_feasibility
from app.optimization.rules.cost_engine import calculate_voyage_cost, VESSEL_SPECS
from app.optimization.rules.deadline_validator import check_deadline
from app.optimization.rules.risk_engine import calculate_risk_score
from app.optimization.rules.schemas import ScenarioResult

def compute_what_if_scenarios(req):
    scenarios_to_run = [
        {"name": "Book Now", "offset_days": 0},
        {"name": "Wait 7 Days", "offset_days": 7},
        {"name": "Wait 14 Days", "offset_days": 14}
    ]
    
    results = []
    for s in scenarios_to_run:
        name = s["name"]
        laycan = req.laycan_start_date + timedelta(days=s["offset_days"])
        
        # Scenario Overrides
        bunker = req.bunker_price_usd_per_mt
        bdi = req.bdi_value
        assumptions = []
        
        if req.scenario_overrides and name in req.scenario_overrides:
            override = req.scenario_overrides[name]
            if override.bunker_price_usd_per_mt is not None:
                bunker = override.bunker_price_usd_per_mt
            if override.bdi_value is not None:
                bdi = override.bdi_value
        else:
            assumptions.append("Assuming BDI and Bunker prices remain constant for this time horizon as no user projections were provided.")
            
        # 1. Freight Prediction
        f_pred = predict_freight_rate(
            req.origin_port, req.destination_port, req.vessel_class, req.cargo_type, 
            req.quantity_mt, req.route_distance_nm, bunker, bdi
        )
        
        # 2. Voyage Cost
        cost = calculate_voyage_cost(
            req.origin_port, req.destination_port, f_pred['predicted_freight_rate_usd_per_mt'],
            req.quantity_mt, bunker, req.route_distance_nm, req.vessel_class, req.port_turnaround_days, req.demurrage_rate
        )
        
        # 3. Deadline Check
        speed = VESSEL_SPECS.get(req.vessel_class, {}).get('speed', 13.5)
        deadline = check_deadline(
            req.route_distance_nm, speed, req.port_turnaround_days, laycan, req.required_delivery_date
        )
        
        # 4. Feasibility Mode
        vessel_res = evaluate_vessel_feasibility(req.quantity_mt, req.origin_port, req.destination_port)
        vessel_mode = "infeasible"
        if any(v.vessel_class == req.vessel_class and v.feasible for v in vessel_res['vessels']):
            vessel_mode = "direct_feasible"
        elif vessel_res['nearest_feasible_option'] and vessel_res['nearest_feasible_option'].vessel_class == req.vessel_class:
            vessel_mode = vessel_res['nearest_feasible_option'].mode
            
        # 5. Risk Score
        risk = calculate_risk_score(
            f_pred['confidence_flag'], deadline['buffer_days'], cost['port_cost_source'], vessel_mode
        )
        
        results.append(ScenarioResult(
            scenario_name=name,
            laycan_start_date=laycan,
            estimated_arrival_date=deadline['estimated_arrival_date'],
            total_cost_usd=cost['total_cost_usd'],
            deadline_feasible=deadline['feasible'],
            risk_tier=risk['risk_tier'],
            risk_score=risk['risk_score'],
            assumptions_noted=assumptions
        ))
        
    # Recommendation Logic
    feasible_scenarios = [s for s in results if s.deadline_feasible]
    if feasible_scenarios:
        best = min(feasible_scenarios, key=lambda x: x.total_cost_usd)
        rec = best.scenario_name
        basis = "Lowest total cost among deadline-feasible options."
    else:
        rec = None
        basis = "No scenarios are deadline-feasible. Recommendation cannot be made."
        
    return {
        "scenarios": results,
        "recommended_scenario": rec,
        "recommendation_basis": basis
    }
