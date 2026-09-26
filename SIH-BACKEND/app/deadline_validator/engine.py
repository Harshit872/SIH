"""
Delivery Deadline and Schedule Validator.

Validates dates strictly based on logical relationships and provided transit inputs.
Does NOT fabricate ETAs if voyage duration is unknown.
"""

import re
from datetime import date, datetime, timedelta
from dataclasses import dataclass
from app.deadline_validator.schemas import ScheduleStatus

_LAYCAN_RE = re.compile(r"^(\d{2} [A-Za-z]{3} \d{4}) - (\d{2} [A-Za-z]{3} \d{4})$")

@dataclass
class ScheduleValidationReport:
    status: ScheduleStatus
    laycan_start: str
    laycan_end: str
    delivery_deadline: str
    estimated_arrival: str = ""
    note: str = ""


def _parse_date(d_str: str, fmt: str) -> date:
    return datetime.strptime(d_str, fmt).date()


def validate_schedule(
    laycan_str: str,
    delivery_date_str: str,
    transit_days: int | None = None,
    loading_days: int | None = None,
    discharge_days: int | None = None,
) -> ScheduleValidationReport:
    # Parse laycan (format: "DD MMM YYYY - DD MMM YYYY")
    match = _LAYCAN_RE.match(laycan_str)
    if not match:
        return ScheduleValidationReport(
            status=ScheduleStatus.INFEASIBLE,
            laycan_start="", laycan_end="", delivery_deadline=delivery_date_str,
            note=f"Invalid laycan format: {laycan_str}"
        )
        
    try:
        l_start = _parse_date(match.group(1), "%d %b %Y")
        l_end = _parse_date(match.group(2), "%d %b %Y")
        delivery = _parse_date(delivery_date_str, "%Y-%m-%d")
    except ValueError as e:
        return ScheduleValidationReport(
            status=ScheduleStatus.INFEASIBLE,
            laycan_start="", laycan_end="", delivery_deadline=delivery_date_str,
            note=f"Date parsing error: {e}"
        )

    # Basic logical check
    if l_start > l_end:
        return ScheduleValidationReport(
            status=ScheduleStatus.INFEASIBLE,
            laycan_start=l_start.isoformat(), laycan_end=l_end.isoformat(), delivery_deadline=delivery.isoformat(),
            note="Laycan start is after laycan end."
        )

    if l_start > delivery:
        return ScheduleValidationReport(
            status=ScheduleStatus.INFEASIBLE,
            laycan_start=l_start.isoformat(), laycan_end=l_end.isoformat(), delivery_deadline=delivery.isoformat(),
            note="Laycan start is after delivery deadline. Impossible to meet."
        )

    # Determine if we can calculate ETA
    if transit_days is None or loading_days is None or discharge_days is None:
        return ScheduleValidationReport(
            status=ScheduleStatus.INSUFFICIENT_DATA,
            laycan_start=l_start.isoformat(), laycan_end=l_end.isoformat(), delivery_deadline=delivery.isoformat(),
            note="Dates are logically valid, but cannot calculate ETA due to missing transit/loading/discharge duration."
        )

    # Calculate worst-case ETA (assume loading starts on the last laycan day)
    total_duration_days = transit_days + loading_days + discharge_days
    worst_case_eta = l_end + timedelta(days=total_duration_days)

    if worst_case_eta > delivery:
        return ScheduleValidationReport(
            status=ScheduleStatus.INFEASIBLE,
            laycan_start=l_start.isoformat(), laycan_end=l_end.isoformat(), delivery_deadline=delivery.isoformat(),
            estimated_arrival=worst_case_eta.isoformat(),
            note=f"Estimated arrival {worst_case_eta.isoformat()} misses deadline of {delivery.isoformat()}."
        )
    else:
        return ScheduleValidationReport(
            status=ScheduleStatus.FEASIBLE,
            laycan_start=l_start.isoformat(), laycan_end=l_end.isoformat(), delivery_deadline=delivery.isoformat(),
            estimated_arrival=worst_case_eta.isoformat(),
            note="Worst-case estimated arrival meets delivery deadline."
        )
