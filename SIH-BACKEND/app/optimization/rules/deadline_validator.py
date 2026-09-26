from datetime import date, timedelta

def check_deadline(distance: float, speed: float, port_days: float, laycan_start: date, req_delivery: date):
    sea_days = distance / (speed * 24)
    total_days = sea_days + port_days
    
    est_arrival = laycan_start + timedelta(days=total_days)
    buffer = (req_delivery - est_arrival).days
    
    return {
        "estimated_arrival_date": est_arrival,
        "feasible": buffer >= 0,
        "buffer_days": buffer
    }
