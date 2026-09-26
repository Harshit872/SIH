from app.optimization.rules.schemas import VesselFeasibilityItem, NearestFeasibleOption

VESSELS = {
    'Handysize': {'dwt_min': 10000, 'dwt_max': 39999},
    'Handymax': {'dwt_min': 40000, 'dwt_max': 59999},
    'Supramax': {'dwt_min': 40000, 'dwt_max': 59999},
    'Panamax': {'dwt_min': 60000, 'dwt_max': 99999},
    'Capesize': {'dwt_min': 100000, 'dwt_max': 180000}
}

def evaluate_vessel_feasibility(cargo_quantity_mt: float, origin: str, dest: str):
    results = []
    any_feasible = False
    
    for v_class, specs in VESSELS.items():
        if cargo_quantity_mt < specs['dwt_min']:
            results.append({
                'vessel_class': v_class, 'feasible': False, 'wasted': float('inf'),
                'reason': f"Cargo ({cargo_quantity_mt} MT) is too small for class minimum ({specs['dwt_min']} MT)."
            })
        elif cargo_quantity_mt > specs['dwt_max'] * 0.95:
            results.append({
                'vessel_class': v_class, 'feasible': False, 'wasted': float('inf'),
                'reason': f"Cargo ({cargo_quantity_mt} MT) exceeds safe capacity of {specs['dwt_max']*0.95} MT."
            })
        else:
            any_feasible = True
            wasted = specs['dwt_max'] - cargo_quantity_mt
            results.append({
                'vessel_class': v_class, 'feasible': True, 'wasted': wasted,
                'reason': "Feasible"
            })
            
    results.sort(key=lambda x: (not x['feasible'], x['wasted']))
    items = [VesselFeasibilityItem(vessel_class=r['vessel_class'], feasible=r['feasible'], reason=r['reason']) for r in results]
    
    nearest_option = None
    if not any_feasible:
        # User request: "identify the closest feasible option by nearest class minimum"
        best_diff = float('inf')
        best_class = None
        mode = "deadfreight"
        
        for v_class, specs in VESSELS.items():
            if cargo_quantity_mt < specs['dwt_min']:
                diff = specs['dwt_min'] - cargo_quantity_mt
                if diff < best_diff:
                    best_diff = diff
                    best_class = v_class
        
        if best_class:
            wasted_mt = best_diff
            note = f"Cargo does not fill any class cleanly. {best_class} is the nearest option; charterer would pay for {wasted_mt} MT of unused capacity (deadfreight)."
            nearest_option = NearestFeasibleOption(
                vessel_class=best_class,
                mode=mode,
                wasted_capacity_mt=wasted_mt,
                note=note
            )
            
    return {"vessels": items, "nearest_feasible_option": nearest_option}
