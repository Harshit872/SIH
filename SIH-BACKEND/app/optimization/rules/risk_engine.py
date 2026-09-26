from app.optimization.rules.schemas import RiskFactor

# Configurable Risk Weights
RISK_WEIGHTS = {
    "low_confidence_freight": 30,
    "deadline_infeasible": 50,      # buffer < 0
    "deadline_tight": 20,           # 0 <= buffer < 2
    "estimated_port_cost": 10,
    "deadfreight_triggered": 15
}

def calculate_risk_score(freight_confidence: str, buffer_days: int, port_cost_source: str, vessel_mode: str):
    score = 0
    breakdown = []
    
    if freight_confidence == "low_confidence_out_of_range":
        pts = RISK_WEIGHTS["low_confidence_freight"]
        score += pts
        breakdown.append(RiskFactor(factor="freight_rate_confidence", points=pts, description="Model prediction out of training bounds."))
        
    if buffer_days < 0:
        pts = RISK_WEIGHTS["deadline_infeasible"]
        score += pts
        breakdown.append(RiskFactor(factor="deadline_buffer", points=pts, description=f"Negative buffer ({buffer_days} days). Delivery infeasible."))
    elif buffer_days < 2:
        pts = RISK_WEIGHTS["deadline_tight"]
        score += pts
        breakdown.append(RiskFactor(factor="deadline_buffer", points=pts, description=f"Tight buffer ({buffer_days} days). High risk of delay."))
        
    if port_cost_source == "estimated_fallback":
        pts = RISK_WEIGHTS["estimated_port_cost"]
        score += pts
        breakdown.append(RiskFactor(factor="port_cost_source", points=pts, description="Port cost relies on a generic estimation fallback, not real tariff rates."))
        
    if vessel_mode == "deadfreight":
        pts = RISK_WEIGHTS["deadfreight_triggered"]
        score += pts
        breakdown.append(RiskFactor(factor="vessel_feasibility", points=pts, description="Vessel selection requires paying deadfreight for unused capacity."))
    elif vessel_mode == "infeasible":
        pts = 50
        score += pts
        breakdown.append(RiskFactor(factor="vessel_feasibility", points=pts, description="No feasible vessel options identified."))
        
    # Tier classification
    if score < 25:
        tier = "Low"
    elif score < 50:
        tier = "Medium"
    else:
        tier = "High"
        
    return {
        "risk_score": score,
        "risk_tier": tier,
        "breakdown": breakdown
    }
