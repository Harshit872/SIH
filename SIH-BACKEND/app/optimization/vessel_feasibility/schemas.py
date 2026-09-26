"""
Vessel feasibility schemas for API layer.

These Pydantic models serialise the dataclass results from evaluator.py
into JSON-safe API responses.
"""

from typing import Optional
from pydantic import BaseModel

from app.optimization.vessel_feasibility.evaluator import FeasibilityStatus


class BerthCheckResultSchema(BaseModel):
    vessel_type: str
    port: str
    berth: str
    status: FeasibilityStatus
    failed_constraints: list[str]
    missing_fields: list[str]
    notes: str


class VesselClassResultSchema(BaseModel):
    vessel_type: str
    overall_status: FeasibilityStatus
    berth_results: list[BerthCheckResultSchema]
    notes: str


class FeasibilityReportSchema(BaseModel):
    origin: str
    destination: str
    commodity: str
    cargo_mt: float
    vessel_class_results: list[VesselClassResultSchema]
    data_warnings: list[str]
    summary: str
