"""
Vessel and port feasibility module.

RESPONSIBILITY
--------------
Determine, for each known vessel class, whether that class can physically
serve the requested route (origin + destination ports) for the requested
cargo.  This module is concerned with dimensional and capacity constraints
only.  It does NOT:
  - calculate freight cost
  - score risk
  - predict ETA or deadline feasibility
  - implement ML ranking
  - assume or invent vessel/port specifications

FEASIBILITY OUTCOMES (FeasibilityStatus enum)
---------------------------------------------
  FEASIBLE        — all checked constraints passed using verified data.
  INFEASIBLE      — at least one constraint was checked and failed.
  INSUFFICIENT_DATA — a required constraint field is present in the dataset
                      schema but its value is missing/empty for this
                      port/vessel combination.
  NOT_CONFIGURED  — no usable reference data (vessel master or port berth
                    master) has been loaded at all.

DATA REQUIREMENTS
-----------------
The module reads from two verified project datasets (shipping_dataset.json,
sheets 03_Vessel_Master and 04_Port_Berth_Master) which are present in the
frontend source tree.  In Phase 5+, these will be loaded from a proper data
layer; for now the module accepts the data as Python dicts passed in at call
time so that the module itself has zero I/O coupling.

WHAT THIS MODULE DOES NOT DO
-----------------------------
  - It does not invent port draft limits, LOA limits, or beam limits.
  - Dhamra port berths have empty dimensional fields in the dataset — the
    module returns INSUFFICIENT_DATA for those berths rather than assuming
    compatibility or incompatibility.
  - It does not rank vessels or produce a recommendation; it only classifies
    each vessel type's feasibility status for each relevant destination berth.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Enums and result types
# ---------------------------------------------------------------------------

class FeasibilityStatus(str, Enum):
    FEASIBLE = "FEASIBLE"
    INFEASIBLE = "INFEASIBLE"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    NOT_CONFIGURED = "NOT_CONFIGURED"


@dataclass(frozen=True)
class BerthCheckResult:
    """Result of checking one vessel class against one berth at a port."""

    vessel_type: str
    port: str
    berth: str
    status: FeasibilityStatus
    failed_constraints: list[str] = field(default_factory=list)
    missing_fields: list[str] = field(default_factory=list)
    notes: str = ""


@dataclass(frozen=True)
class VesselClassResult:
    """Aggregated feasibility for one vessel class across all relevant berths."""

    vessel_type: str
    # Overall status is FEASIBLE only if at least one berth is FEASIBLE
    # and none of the relevant berths returned INFEASIBLE.
    # If every berth is INSUFFICIENT_DATA, overall is INSUFFICIENT_DATA.
    overall_status: FeasibilityStatus
    berth_results: list[BerthCheckResult] = field(default_factory=list)
    notes: str = ""


@dataclass(frozen=True)
class FeasibilityReport:
    """Top-level result returned by evaluate_vessel_port_feasibility()."""

    origin: str
    destination: str
    commodity: str
    cargo_mt: float
    vessel_class_results: list[VesselClassResult] = field(default_factory=list)
    data_warnings: list[str] = field(default_factory=list)
    # Summary status across all vessel classes
    summary: str = ""


# ---------------------------------------------------------------------------
# Constraint evaluation helpers
# ---------------------------------------------------------------------------

def _is_numeric(value) -> bool:
    """Return True if value can be used as a number."""
    if value is None or value == "" or value == "NA":
        return False
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def _check_berth(
    vessel: dict,
    berth: dict,
) -> BerthCheckResult:
    """
    Compare one vessel's dimensional data against one berth's limits.

    Uses only fields that are present and numeric.  Any field that is missing
    or non-numeric in either the vessel or berth record causes INSUFFICIENT_DATA
    for that constraint (not a pass and not a fail).

    Returns a BerthCheckResult.
    """
    vessel_type = vessel.get("Vessel Type", "Unknown")
    port_name = berth.get("Port", "Unknown")
    berth_name = berth.get("Berth/Facility", "Unknown")

    failed: list[str] = []
    missing: list[str] = []

    # --- Draft ---
    v_draft = vessel.get("SSW Draft (m)")
    b_draft = berth.get("Max Draft (m)")
    if _is_numeric(v_draft) and _is_numeric(b_draft):
        if float(v_draft) > float(b_draft):
            failed.append(
                f"Draft: vessel {v_draft}m > berth limit {b_draft}m"
            )
    elif not _is_numeric(v_draft):
        missing.append("vessel SSW Draft (m)")
    elif not _is_numeric(b_draft):
        missing.append("berth Max Draft (m)")

    # --- LOA ---
    v_loa = vessel.get("LOA (m)")
    b_loa = berth.get("Max LOA (m)")
    if _is_numeric(v_loa) and _is_numeric(b_loa):
        if float(v_loa) > float(b_loa):
            failed.append(
                f"LOA: vessel {v_loa}m > berth limit {b_loa}m"
            )
    elif not _is_numeric(v_loa):
        missing.append("vessel LOA (m)")
    elif not _is_numeric(b_loa):
        missing.append("berth Max LOA (m)")

    # --- Beam ---
    v_beam = vessel.get("Beam (m)")
    b_beam = berth.get("Max Beam (m)")
    if _is_numeric(v_beam) and _is_numeric(b_beam):
        if float(v_beam) > float(b_beam):
            failed.append(
                f"Beam: vessel {v_beam}m > berth limit {b_beam}m"
            )
    elif not _is_numeric(v_beam):
        missing.append("vessel Beam (m)")
    elif not _is_numeric(b_beam):
        missing.append("berth Max Beam (m)")

    # --- DWT capacity vs cargo_mt is intentionally NOT checked here ---
    # Capacity-to-cargo matching requires a separate cargo_mt parameter
    # and is handled in evaluate_vessel_port_feasibility().

    # Determine status
    if failed:
        status = FeasibilityStatus.INFEASIBLE
    elif missing:
        status = FeasibilityStatus.INSUFFICIENT_DATA
    else:
        status = FeasibilityStatus.FEASIBLE

    return BerthCheckResult(
        vessel_type=vessel_type,
        port=port_name,
        berth=berth_name,
        status=status,
        failed_constraints=failed,
        missing_fields=missing,
    )


def _capacity_check(
    vessel: dict,
    cargo_mt: float,
) -> tuple[FeasibilityStatus, str]:
    """
    Check whether the vessel's DWT covers the requested cargo volume.
    Returns (status, note).
    """
    dwt = vessel.get("DWT (mt)")
    if not _is_numeric(dwt):
        return FeasibilityStatus.INSUFFICIENT_DATA, "DWT (mt) not available for vessel."
    dwt_f = float(dwt)
    if cargo_mt > dwt_f:
        return (
            FeasibilityStatus.INFEASIBLE,
            f"Cargo {cargo_mt} MT exceeds vessel DWT {dwt_f} MT.",
        )
    return FeasibilityStatus.FEASIBLE, ""


def _aggregate_berth_statuses(berth_results: list[BerthCheckResult]) -> FeasibilityStatus:
    """
    Determine the overall status for a vessel class from its per-berth results.

    Rules:
      - FEASIBLE if at least one berth is FEASIBLE.
      - INFEASIBLE if no berth is FEASIBLE and at least one is INFEASIBLE.
      - INSUFFICIENT_DATA if all berths are INSUFFICIENT_DATA.
    """
    if not berth_results:
        return FeasibilityStatus.INSUFFICIENT_DATA

    statuses = {r.status for r in berth_results}

    if FeasibilityStatus.FEASIBLE in statuses:
        return FeasibilityStatus.FEASIBLE
    if FeasibilityStatus.INFEASIBLE in statuses:
        return FeasibilityStatus.INFEASIBLE
    return FeasibilityStatus.INSUFFICIENT_DATA


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def evaluate_vessel_port_feasibility(
    *,
    origin: str,
    destination: str,
    commodity: str,
    cargo_mt: float,
    vessel_master: list[dict],
    port_berth_master: list[dict],
    cargo_master: list[dict],
) -> FeasibilityReport:
    """
    Evaluate whether each known vessel class can serve the requested route.

    Parameters
    ----------
    origin : str
        Origin port name (display label, as stored in the dataset).
    destination : str
        Destination port name (display label, as stored in the dataset).
    commodity : str
        Commodity name (display label, as stored in the dataset).
    cargo_mt : float
        Cargo quantity in metric tonnes.
    vessel_master : list[dict]
        Records from dataset sheet 03_Vessel_Master.
    port_berth_master : list[dict]
        Records from dataset sheet 04_Port_Berth_Master.
    cargo_master : list[dict]
        Records from dataset sheet 05_Cargo_Master.

    Returns
    -------
    FeasibilityReport
    """
    warnings: list[str] = []

    # Guard: no data at all
    if not vessel_master or not port_berth_master:
        empty_results: list[VesselClassResult] = []
        return FeasibilityReport(
            origin=origin,
            destination=destination,
            commodity=commodity,
            cargo_mt=cargo_mt,
            vessel_class_results=empty_results,
            data_warnings=["No vessel master or port berth master data available."],
            summary=(
                "NOT_CONFIGURED: vessel and port reference data have not been loaded. "
                "Feasibility cannot be determined."
            ),
        )

    # Determine candidate vessel types from cargo master
    cargo_record = next(
        (c for c in cargo_master if c.get("Cargo", "").lower() == commodity.lower()),
        None,
    )
    if cargo_record:
        candidate_types_raw: str = cargo_record.get("Candidate Vessel Types", "")
        # Candidate Vessel Types is formatted as "Panamax/Supramax/Handymax" etc.
        candidate_types = [t.strip() for t in candidate_types_raw.replace("/", ",").split(",") if t.strip()]
    else:
        # No cargo record — evaluate all vessel types and add a warning
        candidate_types = [v.get("Vessel Type") for v in vessel_master if v.get("Vessel Type")]
        warnings.append(
            f"Commodity '{commodity}' not found in cargo master. "
            "Evaluating all vessel types without cargo-type filtering."
        )

    # Filter port berth records for the destination port only.
    # NOTE: The dataset only contains East Coast India ports (Paradip, Dhamra).
    # Origin port berth constraints are not available in the current dataset.
    dest_berths = [
        b for b in port_berth_master
        if b.get("Port", "").lower() == destination.lower()
    ]
    if not dest_berths:
        warnings.append(
            f"No port berth data found for destination '{destination}'. "
            "Port feasibility cannot be evaluated for this destination."
        )

    origin_berths = [
        b for b in port_berth_master
        if b.get("Port", "").lower() == origin.lower()
    ]
    if not origin_berths:
        warnings.append(
            f"No port berth data found for origin '{origin}'. "
            "Origin port feasibility is not checked (data not available)."
        )

    # Evaluate each vessel class
    vessel_class_results: list[VesselClassResult] = []

    for vessel in vessel_master:
        v_type = vessel.get("Vessel Type", "Unknown")

        # Filter to candidate types (case-insensitive partial match)
        is_candidate = any(
            ct.lower() in v_type.lower() or v_type.lower() in ct.lower()
            for ct in candidate_types
        )
        if not is_candidate:
            continue

        berth_results: list[BerthCheckResult] = []
        class_notes: list[str] = []

        # --- Capacity check ---
        cap_status, cap_note = _capacity_check(vessel, cargo_mt)
        if cap_status == FeasibilityStatus.INFEASIBLE:
            # If cargo exceeds DWT, no berth-level check is needed — infeasible overall
            vessel_class_results.append(
                VesselClassResult(
                    vessel_type=v_type,
                    overall_status=FeasibilityStatus.INFEASIBLE,
                    berth_results=[],
                    notes=cap_note,
                )
            )
            continue
        elif cap_status == FeasibilityStatus.INSUFFICIENT_DATA:
            class_notes.append(cap_note)

        # --- Destination berth dimensional checks ---
        if dest_berths:
            for berth in dest_berths:
                result = _check_berth(vessel, berth)
                berth_results.append(result)
        else:
            # No berth data for destination — mark as insufficient
            berth_results.append(
                BerthCheckResult(
                    vessel_type=v_type,
                    port=destination,
                    berth="(no data)",
                    status=FeasibilityStatus.INSUFFICIENT_DATA,
                    missing_fields=["all berth fields (port not in dataset)"],
                )
            )

        overall = _aggregate_berth_statuses(berth_results)

        # If capacity check was insufficient, downgrade overall if it was FEASIBLE
        if cap_status == FeasibilityStatus.INSUFFICIENT_DATA and overall == FeasibilityStatus.FEASIBLE:
            overall = FeasibilityStatus.INSUFFICIENT_DATA
            class_notes.append(
                "Marked INSUFFICIENT_DATA because vessel DWT could not be verified."
            )

        vessel_class_results.append(
            VesselClassResult(
                vessel_type=v_type,
                overall_status=overall,
                berth_results=berth_results,
                notes="; ".join(class_notes),
            )
        )

    if not vessel_class_results:
        warnings.append("No candidate vessel types were evaluated.")

    # Build summary string
    feasible_types = [
        r.vessel_type for r in vessel_class_results
        if r.overall_status == FeasibilityStatus.FEASIBLE
    ]
    infeasible_types = [
        r.vessel_type for r in vessel_class_results
        if r.overall_status == FeasibilityStatus.INFEASIBLE
    ]
    insufficient_types = [
        r.vessel_type for r in vessel_class_results
        if r.overall_status == FeasibilityStatus.INSUFFICIENT_DATA
    ]

    summary_parts: list[str] = []
    if feasible_types:
        summary_parts.append(f"Feasible vessel types: {', '.join(feasible_types)}.")
    if infeasible_types:
        summary_parts.append(f"Infeasible vessel types: {', '.join(infeasible_types)}.")
    if insufficient_types:
        summary_parts.append(
            f"Insufficient data for: {', '.join(insufficient_types)} "
            "(one or more required constraint fields are missing in the dataset)."
        )
    if not summary_parts:
        summary_parts.append(
            "No vessel types could be evaluated. Check data availability."
        )

    return FeasibilityReport(
        origin=origin,
        destination=destination,
        commodity=commodity,
        cargo_mt=cargo_mt,
        vessel_class_results=vessel_class_results,
        data_warnings=warnings,
        summary=" ".join(summary_parts),
    )
