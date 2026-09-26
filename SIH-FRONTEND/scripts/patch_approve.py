import re

with open("SIH-BACKEND/app/api/routes.py", "r", encoding="utf-8") as f:
    text = f.read()

# Replace the old approve_plan logic
# Remove the old one entirely first
old_func_pattern = r'@router\.post\("/plan/approve".*?return \{\n\s+"plan_id": plan_id,\n\s+"status": "stored",\n\s+"chosen_scenario": chosen_scenario_name,\n\s+"total_cost_usd": chosen_scenario\["total_cost_usd"\],\n\s+"risk_tier": chosen_scenario\["risk_tier"\]\n\s+\}'
text = re.sub(old_func_pattern, '', text, flags=re.DOTALL)

# Now add the new logic
new_logic = '''
from app.auth.dependencies import get_current_user
from app.optimization.rules.decision_engine import compute_what_if_scenarios
from app.optimization.rules.schemas import WhatIfRequest

@router.post("/plan/approve", response_model=ApprovedPlanResponse, tags=["Plan"])
async def approve_plan(req: ApprovePlanRequest, db: sqlite3.Connection = Depends(get_db), current_user: dict = Depends(get_current_user)):
    chosen_scenario_name = req.what_if_response.get("recommended_scenario") if req.user_decision == "approve" else req.modified_scenario
    
    if not chosen_scenario_name:
        raise HTTPException(status_code=400, detail="No scenario provided")
        
    # Re-run the What-If Engine to ensure data is authentic and not spoofed by frontend
    wi_req = WhatIfRequest(**req.voyage_details)
    fresh_what_if = compute_what_if_scenarios(wi_req)
    
    chosen_scenario = next((s for s in fresh_what_if["scenarios"] if s.scenario_name == chosen_scenario_name), None)
    if not chosen_scenario:
        raise HTTPException(status_code=400, detail="Invalid scenario chosen")
        
    plan_id = str(uuid.uuid4())
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO approved_plans (plan_id, user_email, voyage_details, chosen_scenario, total_cost_usd, risk_tier) VALUES (?, ?, ?, ?, ?, ?)",
        (
            plan_id,
            current_user["sub"],
            json.dumps(req.voyage_details),
            chosen_scenario.model_dump_json(),
            chosen_scenario.total_cost_usd,
            chosen_scenario.risk_tier
        )
    )
    db.commit()
    
    return {
        "plan_id": plan_id,
        "status": "stored",
        "chosen_scenario": chosen_scenario_name,
        "total_cost_usd": chosen_scenario.total_cost_usd,
        "risk_tier": chosen_scenario.risk_tier
    }
'''

with open("SIH-BACKEND/app/api/routes.py", "w", encoding="utf-8") as f:
    f.write(text + new_logic)

