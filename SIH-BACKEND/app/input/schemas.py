"""
Input layer: Pydantic request and response schemas for voyage submission.

Schemas live here — separate from route handlers and business logic modules.
Business validation (vessel feasibility, deadline feasibility, cost) is NOT
performed here; those concerns belong in their respective modules.

Frontend sources (confirmed by inspection of VoyageRequirementInput.tsx and
VoyageContext.tsx):
  - laycan is serialised as a free-text string: "DD MMM YYYY - DD MMM YYYY"
    (e.g. "01 Jan 2026 - 15 Jan 2026") using date-fns format("dd MMM yyyy").
  - deliveryDate is serialised as "YYYY-MM-DD" using date-fns format("yyyy-MM-dd").
  - noOfVoyages is calculated by the frontend as ceil(cargoMt / 50000).
    This is a known limitation documented in CONTRACT_NOTES below.
  - origin and destination are the display-label strings (e.g. "Paradip"),
    NOT the internal select key slugs (e.g. "paradip").
"""

import re
from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

# ---------------------------------------------------------------------------
# Known laycan string format emitted by the frontend
# ---------------------------------------------------------------------------
_LAYCAN_RE = re.compile(
    r"^\d{2} [A-Za-z]{3} \d{4} - \d{2} [A-Za-z]{3} \d{4}$"
)

# ---------------------------------------------------------------------------
# CONTRACT_NOTES — documented field decisions
# ---------------------------------------------------------------------------
CONTRACT_NOTES = """
Field contract notes (as of Phase 3 inspection):

noOfVoyages:
  - Origin: calculated by the frontend (ceil(cargoMt / 50,000 MT)).
  - The 50,000 MT denominator is a hardcoded frontend constant (STANDARD_VESSEL_CAPACITY_MT).
  - This value IS accepted by the backend to preserve compatibility,
    but it is NOT authoritative vessel-sizing logic.
  - Future phases should let the backend derive recommended voyage counts
    from real vessel capacity data; the frontend field should become advisory.

laycan:
  - The frontend does not send structured start/end dates as separate fields.
  - It serialises the DateRange picker as a single string: "DD MMM YYYY - DD MMM YYYY".
  - The backend parses this string into laycan_start / laycan_end for internal use.
  - A structured {laycan_start, laycan_end} wire format is preferred long-term;
    listed as a CONTRACT_GAP in the report.

deliveryDate:
  - Serialised as ISO date "YYYY-MM-DD" (date only, no time component).

cargoMt:
  - Unit: metric tonnes (MT).  The frontend label reads "Cargo Volume (MT)".
"""


# ---------------------------------------------------------------------------
# Request schema
# ---------------------------------------------------------------------------

class VoyageSubmitRequest(BaseModel):
    """
    Voyage requirement payload sent by the frontend on form submission.
    All fields are required; no optional fields exist in the current frontend
    contract.
    """

    origin: str = Field(
        ...,
        min_length=1,
        description=(
            "Origin port display name as returned by DatasetService.getUniquePorts(). "
            "Example: 'Paradip'"
        ),
    )
    destination: str = Field(
        ...,
        min_length=1,
        description=(
            "Destination port display name as returned by DatasetService.getUniquePorts(). "
            "Example: 'Paradip'"
        ),
    )
    commodity: str = Field(
        ...,
        min_length=1,
        description=(
            "Commodity display name from DatasetService.getCargoes(). "
            "Example: 'Thermal Coal'"
        ),
    )
    cargoMt: float = Field(
        ...,
        gt=0,
        description="Total cargo quantity in metric tonnes (MT). Must be positive.",
    )
    deliveryDate: date = Field(
        ...,
        description=(
            "Target delivery date. The frontend serialises this as 'YYYY-MM-DD'. "
            "Pydantic parses ISO date strings automatically."
        ),
    )
    contract: str = Field(
        ...,
        min_length=1,
        description=(
            "Contract type label. Accepted values from the frontend: "
            "'Voyage Charter', 'Time Charter', 'Contract of Affreightment (COA)', "
            "'Bareboat Charter'."
        ),
    )
    laycan: str = Field(
        ...,
        description=(
            "Laycan window as a string: 'DD MMM YYYY - DD MMM YYYY'. "
            "Example: '01 Jun 2027 - 10 Jun 2027'. "
            "This is the format the frontend emits; see CONTRACT_NOTES for the "
            "planned migration to a structured format."
        ),
    )
    noOfVoyages: int = Field(
        ...,
        gt=0,
        description=(
            "Number of voyages. Currently calculated by the frontend as "
            "ceil(cargoMt / 50000). Accepted here for compatibility; see CONTRACT_NOTES."
        ),
    )

    @field_validator("laycan")
    @classmethod
    def laycan_format(cls, v: str) -> str:
        """
        Validate that laycan matches 'DD MMM YYYY - DD MMM YYYY'.
        Does NOT validate that the dates are logically coherent; that belongs in
        a business-validation layer, not the schema.
        """
        if not _LAYCAN_RE.match(v):
            raise ValueError(
                "laycan must be in the format 'DD MMM YYYY - DD MMM YYYY', "
                f"e.g. '01 Jun 2027 - 10 Jun 2027'. Got: '{v}'"
            )
        return v

    @model_validator(mode="after")
    def origin_not_same_as_destination(self) -> "VoyageSubmitRequest":
        if self.origin.strip().lower() == self.destination.strip().lower():
            raise ValueError("origin and destination must be different ports.")
        return self


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------

class VoyageSubmitResponse(BaseModel):
    """
    Placeholder response returned by POST /api/v1/voyage/submit.
    The status field is always 'accepted' in this phase.
    No computed results are returned.
    """

    status: Literal["accepted"] = Field(
        description="Fixed value: 'accepted'. Indicates the request was received and validated."
    )
    message: str = Field(description="Human-readable status description.")
    note: str = Field(
        description=(
            "Transparency note explaining that no processing has occurred and "
            "the response does not contain forecasts, costs, or recommendations."
        )
    )
    received: dict = Field(
        description="Echo of the validated and parsed request fields."
    )


# ---------------------------------------------------------------------------
# Provisional placeholder schemas for future endpoints
# (kept here so routes.py imports don't break; will be moved/refined later)
# ---------------------------------------------------------------------------

class _PlaceholderUnavailable(BaseModel):
    """Base for placeholder responses that acknowledge an engine is not yet implemented."""

    implemented: bool = False
    message: str = "Not implemented in this phase."
