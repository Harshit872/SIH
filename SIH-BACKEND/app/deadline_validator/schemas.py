"""
Deadline validation schemas.
"""

from enum import Enum
from pydantic import BaseModel, Field


class ScheduleStatus(str, Enum):
    FEASIBLE = "FEASIBLE"
    INFEASIBLE = "INFEASIBLE"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


class ScheduleValidationReportSchema(BaseModel):
    status: ScheduleStatus = Field(description="Overall schedule status.")
    laycan_start: str = Field(description="Parsed laycan start date.")
    laycan_end: str = Field(description="Parsed laycan end date.")
    delivery_deadline: str = Field(description="Target delivery date.")
    estimated_arrival: str = Field(default="", description="ETA if calculable, otherwise empty.")
    note: str = Field(description="Explanation of the evaluation.")
