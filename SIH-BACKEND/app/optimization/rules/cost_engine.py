VESSEL_SPECS = {
    'Handysize': {'speed': 13.5, 'consumption': 21},
    'Handymax': {'speed': 13.5, 'consumption': 26},
    'Supramax': {'speed': 13.5, 'consumption': 26},
    'Panamax': {'speed': 13.5, 'consumption': 30},
    'Capesize': {'speed': 14.5, 'consumption': 45}
}

def calculate_voyage_cost(origin: str, dest: str, rate: float, qty: float, bunker_price: float, distance: float, v_class: str, port_days: float, demurrage: float):
    notes = []
    freight_cost = rate * qty
    
    specs = VESSEL_SPECS.get(v_class)
    if not specs:
        specs = {'speed': 13.5, 'consumption': 30} # Default fallback
        notes.append(f"Vessel class '{v_class}' not found in reference. Defaulting to 13.5kn / 30t/day.")
        
    voyage_days = distance / (specs['speed'] * 24)
    bunker_cost = voyage_days * specs['consumption'] * bunker_price
    
    origin_lower = origin.lower() if origin else ""
    dest_lower = dest.lower() if dest else ""
    
    if "paradip" in origin_lower or "paradip" in dest_lower:
        grt_proxy = qty * 0.5
        notes.append("Paradip port costs calculated using GRT proxy (0.5 * quantity_mt).")
        port_dues = grt_proxy * 0.45
        pilotage = grt_proxy * 1.00
        berth_hire = grt_proxy * 0.009 * (port_days * 24)
        port_cost = port_dues + pilotage + berth_hire
        port_cost_source = "real_reference"
    else:
        port_cost = port_days * 10000
        notes.append("Port not found in port_cost_specifications.csv. Estimated base cost of ,000/day applied.")
        port_cost_source = "estimated_fallback"
    
    total_cost = freight_cost + bunker_cost + port_cost
    
    return {
        "freight_cost_usd": float(freight_cost),
        "bunker_cost_usd": float(bunker_cost),
        "port_cost_usd": float(port_cost),
        "total_cost_usd": float(total_cost),
        "port_cost_source": port_cost_source,
        "notes": notes
    }
