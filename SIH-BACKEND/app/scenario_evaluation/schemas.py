"""
Scenario comparison schemas.
"""

from typing import Optional
from pydantic import BaseModel, Field
from app.optimization.cost_engine.schemas import VoyageCostReportSchema
from app.optimization.risk_engine.schemas import RiskAssessmentReportSchema
from app.deadline_validator.schemas import ScheduleValidationReportSchema


class ScenarioSchema(BaseModel):
    name: str = Field(description="Scenario name, e.g., 'Book Now', 'Wait 7 Days'.")
    assumed_booking_date: str = Field(description="Date the booking action is assumed to happen.")
    is_evaluable: bool = Field(description="True if scenario has enough data to be meaningfully compared.")
    cost_report: Optional[VoyageCostReportSchema] = None
    schedule_report: Optional[ScheduleValidationReportSchema] = None
    risk_report: Optional[RiskAssessmentReportSchema] = None
    missing_inputs: list[str] = Field(default_factory=list, description="Missing required inputs that prevent full evaluation.")


class ScenarioComparisonReportSchema(BaseModel):
    scenarios: list[ScenarioSchema]
    best_scenario: str = Field(default="NONE", description="Not decided in this phase. Kept for future engine.")
    note: str = Field(description="Summary of comparison.")
