"""
Cost calculation engine schemas for API layer.
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class CostStatus(str, Enum):
    CALCULATED = "CALCULATED"
    MISSING_INPUT = "MISSING_INPUT"
    UNSUPPORTED = "UNSUPPORTED"


class CostComponentSchema(BaseModel):
    name: str = Field(description="Name of the cost component (e.g. 'Freight', 'Port Charges').")
    status: CostStatus = Field(description="Status of the calculation.")
    amount: Optional[float] = Field(None, description="Calculated amount, if available.")
    currency: Optional[str] = Field(None, description="Currency code, e.g., 'USD'.")
    note: str = Field(description="Explanation of calculation or reason for unavailability.")


class VoyageCostReportSchema(BaseModel):
    components: list[CostComponentSchema]
    is_total_complete: bool = Field(description="True if all components were successfully calculated.")
    total_amount: Optional[float] = Field(None, description="Sum of calculated components (may be partial).")
    currency: Optional[str] = Field(None, description="Currency of the total.")
    notes: str = Field(description="Overall summary or warnings about partial totals.")
