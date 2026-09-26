"""
Voyage Cost Calculation Engine.

Calculates voyage costs based strictly on provided and verified inputs.
Does not invent rates, fuel consumption, distances, or port charges.
Returns explicit status codes when data is missing.
"""

from dataclasses import dataclass, field
from typing import Optional
from app.optimization.cost_engine.schemas import CostStatus


@dataclass
class CostComponentResult:
    name: str
    status: CostStatus
    amount: Optional[float] = None
    currency: Optional[str] = None
    note: str = ""


@dataclass
class VoyageCostReport:
    components: list[CostComponentResult] = field(default_factory=list)
    is_total_complete: bool = False
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    notes: str = ""


def calculate_voyage_costs(
    cargo_mt: float,
    freight_rate_per_mt: Optional[float] = None,
    freight_currency: str = "USD",
    bunker_price_per_mt: Optional[float] = None,
    bunker_consumption_mt: Optional[float] = None,
    port_charges: Optional[float] = None,
    demurrage_rate_per_day: Optional[float] = None,
    demurrage_days: Optional[float] = None,
    waiting_time_days: Optional[float] = None,
    daily_hire_rate: Optional[float] = None,
) -> VoyageCostReport:
    """
    Evaluates each cost component safely without assuming default values.
    """
    components = []
    
    # 1. Freight Cost
    if freight_rate_per_mt is not None and cargo_mt > 0:
        amount = freight_rate_per_mt * cargo_mt
        components.append(CostComponentResult(
            name="Freight",
            status=CostStatus.CALCULATED,
            amount=amount,
            currency=freight_currency,
            note=f"{cargo_mt} MT @ {freight_rate_per_mt} {freight_currency}/MT"
        ))
    else:
        components.append(CostComponentResult(
            name="Freight",
            status=CostStatus.MISSING_INPUT,
            note="Missing freight rate per MT."
        ))
        
    # 2. Bunker Cost
    if bunker_price_per_mt is not None and bunker_consumption_mt is not None:
        amount = bunker_price_per_mt * bunker_consumption_mt
        components.append(CostComponentResult(
            name="Fuel/Bunker",
            status=CostStatus.CALCULATED,
            amount=amount,
            currency="USD",
            note=f"{bunker_consumption_mt} MT @ {bunker_price_per_mt} USD/MT"
        ))
    else:
        components.append(CostComponentResult(
            name="Fuel/Bunker",
            status=CostStatus.MISSING_INPUT,
            note="Missing bunker price or total consumption data."
        ))

    # 3. Port Charges
    if port_charges is not None:
        components.append(CostComponentResult(
            name="Port Charges",
            status=CostStatus.CALCULATED,
            amount=port_charges,
            currency="USD",
            note="Explicitly provided port charges."
        ))
    else:
        components.append(CostComponentResult(
            name="Port Charges",
            status=CostStatus.MISSING_INPUT,
            note="No port charges supplied."
        ))
        
    # 4. Waiting Time Cost
    if waiting_time_days is not None and daily_hire_rate is not None:
        amount = waiting_time_days * daily_hire_rate
        components.append(CostComponentResult(
            name="Waiting Time",
            status=CostStatus.CALCULATED,
            amount=amount,
            currency="USD",
            note=f"{waiting_time_days} days @ {daily_hire_rate} USD/day"
        ))
    else:
        components.append(CostComponentResult(
            name="Waiting Time",
            status=CostStatus.MISSING_INPUT,
            note="Missing waiting time or daily hire rate."
        ))

    # 5. Demurrage
    if demurrage_rate_per_day is not None and demurrage_days is not None:
        amount = demurrage_rate_per_day * demurrage_days
        components.append(CostComponentResult(
            name="Demurrage",
            status=CostStatus.CALCULATED,
            amount=amount,
            currency="USD",
            note=f"{demurrage_days} days @ {demurrage_rate_per_day} USD/day"
        ))
    else:
        components.append(CostComponentResult(
            name="Demurrage",
            status=CostStatus.MISSING_INPUT,
            note="Missing demurrage rate or delay days."
        ))

    # Determine Total
    calculated = [c for c in components if c.status == CostStatus.CALCULATED]
    missing = [c for c in components if c.status != CostStatus.CALCULATED]
    
    total_amount = sum(c.amount for c in calculated) if calculated else None
    
    # Check for mixed currencies
    currencies = {c.currency for c in calculated if c.currency}
    if len(currencies) > 1:
        notes = "WARNING: Mixed currencies in components. Total is invalid."
        total_amount = None
        currency = None
        is_total_complete = False
    else:
        currency = list(currencies)[0] if currencies else None
        is_total_complete = len(missing) == 0
        notes = "All components calculated successfully." if is_total_complete else "Partial total; excludes missing or unsupported components."
        
    return VoyageCostReport(
        components=components,
        is_total_complete=is_total_complete,
        total_amount=total_amount,
        currency=currency,
        notes=notes,
    )
