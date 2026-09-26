import re

with open('SIH-BACKEND/app/api/routes.py', 'r') as f:
    text = f.read()

replacement = '''
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
'''

text = re.sub(r'# Transit duration is missing from current request, so ETA won\'t be calculated\s*report = validate_schedule\(laycan_str=req\.laycan, delivery_date_str=req\.deliveryDate\.isoformat\(\)\)', replacement.strip(), text)

with open('SIH-BACKEND/app/api/routes.py', 'w') as f:
    f.write(text)
