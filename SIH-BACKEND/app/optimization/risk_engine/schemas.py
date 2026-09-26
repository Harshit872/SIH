"""
Operational risk assessment schemas.
"""

from enum import Enum
from pydantic import BaseModel, Field


class RiskStatus(str, Enum):
    EVALUATED = "EVALUATED"
    NOT_EVALUATED = "NOT_EVALUATED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


class RiskFindingSchema(BaseModel):
    factor: str = Field(description="The risk factor being evaluated.")
    status: RiskStatus = Field(description="Whether this risk could be assessed.")
    finding: str = Field(description="The actual evaluation result.")
    missing_info: str = Field(default="", description="Information needed to evaluate this if it's missing.")


class RiskAssessmentReportSchema(BaseModel):
    findings: list[RiskFindingSchema] = Field(description="List of all evaluated and unevaluated risk factors.")
