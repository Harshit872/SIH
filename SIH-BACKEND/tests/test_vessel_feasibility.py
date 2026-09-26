"""
Tests for the vessel/port feasibility module (evaluator.py).

All vessel and port records used here are TEST FIXTURES only.
They do not represent real vessel specifications or real port data.

Tests verify module behaviour, not data correctness.
"""

import pytest
from app.optimization.vessel_feasibility.evaluator import (
    evaluate_vessel_port_feasibility,
    FeasibilityStatus,
)

# ---------------------------------------------------------------------------
# TEST FIXTURES — clearly labelled, isolated from production data
# ---------------------------------------------------------------------------

# A single test vessel that fits within typical berth limits
VESSEL_FITS = {
    "Vessel Type": "TestHandysize",
    "DWT (mt)": 38000,
    "SSW Draft (m)": 10.0,
    "LOA (m)": 175.0,
    "Beam (m)": 28.0,
    "Grain Capacity (cbm)": 45000,
    "Laden Speed (kn)": 14,
    "Ballast Speed (kn)": 14,
    "Max Age (yr)": 15,
    "Geared": True,
    "Source": "TEST FIXTURE — not real data",
}

# A vessel too large in draft and LOA
VESSEL_TOO_LARGE = {
    "Vessel Type": "TestCapesize",
    "DWT (mt)": 180000,
    "SSW Draft (m)": 19.0,
    "LOA (m)": 295.0,
    "Beam (m)": 48.0,
    "Grain Capacity (cbm)": 200000,
    "Laden Speed (kn)": 14,
    "Ballast Speed (kn)": 15,
    "Max Age (yr)": 10,
    "Geared": False,
    "Source": "TEST FIXTURE — not real data",
}

# A vessel with no DWT info
VESSEL_MISSING_DWT = {
    "Vessel Type": "TestMissingDWT",
    "DWT (mt)": "",
    "SSW Draft (m)": 10.0,
    "LOA (m)": 170.0,
    "Beam (m)": 28.0,
    "Source": "TEST FIXTURE — not real data",
}

# A port berth with complete, tight limits — only small vessels fit
BERTH_TIGHT = {
    "Port": "TestPortA",
    "Berth/Facility": "BerthTight",
    "Commodity": "Coal",
    "Max LOA (m)": 180.0,
    "Max Beam (m)": 30.0,
    "Max Draft (m)": 11.0,
    "High Tide Qualification": False,
    "Handling / Facility": "Mechanised",
    "Source": "TEST FIXTURE — not real data",
    "Remarks": "",
}

# A port berth with generous limits — most vessels fit
BERTH_GENEROUS = {
    "Port": "TestPortA",
    "Berth/Facility": "BerthGenerous",
    "Commodity": "Coal",
    "Max LOA (m)": 300.0,
    "Max Beam (m)": 50.0,
    "Max Draft (m)": 18.0,
    "High Tide Qualification": False,
    "Handling / Facility": "Mechanised",
    "Source": "TEST FIXTURE — not real data",
    "Remarks": "",
}

# A berth with missing dimensional data (like Dhamra in real dataset)
BERTH_MISSING_DIMS = {
    "Port": "TestPortB",
    "Berth/Facility": "BerthNoDims",
    "Commodity": "Coal",
    "Max LOA (m)": "",
    "Max Beam (m)": "",
    "Max Draft (m)": "",
    "High Tide Qualification": "",
    "Handling / Facility": "Deep-draft multi-cargo",
    "Source": "TEST FIXTURE — not real data",
    "Remarks": "",
}

# Cargo master entry that allows TestHandysize
CARGO_COAL = {
    "Cargo": "Thermal Coal",
    "Cargo Class": "Dry bulk",
    "Use": "Test",
    "Example Quantity": 50000,
    "Unit": "mt",
    "Origin Example": "TestOrigin",
    "Destination Example": "TestPortA",
    "Candidate Vessel Types": "TestHandysize/TestCapesize",
    "Source": "TEST FIXTURE",
    "Status": "Test",
}


# ---------------------------------------------------------------------------
# Tests: NOT_CONFIGURED — no data loaded
# ---------------------------------------------------------------------------

class TestNotConfigured:
    def test_no_data_returns_not_configured_summary(self):
        report = evaluate_vessel_port_feasibility(
            origin="Anywhere",
            destination="TestPortA",
            commodity="Thermal Coal",
            cargo_mt=10000,
            vessel_master=[],
            port_berth_master=[],
            cargo_master=[],
        )
        assert "NOT_CONFIGURED" in report.summary

    def test_no_data_has_no_vessel_results(self):
        report = evaluate_vessel_port_feasibility(
            origin="Anywhere",
            destination="TestPortA",
            commodity="Thermal Coal",
            cargo_mt=10000,
            vessel_master=[],
            port_berth_master=[],
            cargo_master=[],
        )
        assert len(report.vessel_class_results) == 0

    def test_no_data_warns(self):
        report = evaluate_vessel_port_feasibility(
            origin="Anywhere",
            destination="TestPortA",
            commodity="Thermal Coal",
            cargo_mt=10000,
            vessel_master=[],
            port_berth_master=[],
            cargo_master=[],
        )
        assert len(report.data_warnings) > 0


# ---------------------------------------------------------------------------
# Tests: INSUFFICIENT_DATA — berths have empty dimensional fields
# ---------------------------------------------------------------------------

class TestInsufficientData:
    def test_missing_berth_dims_does_not_return_feasible(self):
        """A berth with empty LOA/beam/draft must not produce FEASIBLE."""
        report = evaluate_vessel_port_feasibility(
            origin="Anywhere",
            destination="TestPortB",
            commodity="Thermal Coal",
            cargo_mt=10000,
            vessel_master=[VESSEL_FITS],
            port_berth_master=[BERTH_MISSING_DIMS],
            cargo_master=[CARGO_COAL],
        )
        for vc in report.vessel_class_results:
            assert vc.overall_status != FeasibilityStatus.FEASIBLE, (
                f"Vessel type {vc.vessel_type!r} was marked FEASIBLE despite missing berth dims"
            )

    def test_missing_berth_dims_returns_insufficient_data(self):
        report = evaluate_vessel_port_feasibility(
            origin="Anywhere",
            destination="TestPortB",
            commodity="Thermal Coal",
            cargo_mt=10000,
            vessel_master=[VESSEL_FITS],
            port_berth_master=[BERTH_MISSING_DIMS],
            cargo_master=[CARGO_COAL],
        )
        assert any(
            vc.overall_status == FeasibilityStatus.INSUFFICIENT_DATA
            for vc in report.vessel_class_results
        )

    def test_unknown_destination_does_not_return_feasible(self):
        """Destination not in dataset → not FEASIBLE."""
        report = evaluate_vessel_port_feasibility(
            origin="Anywhere",
            destination="UnknownPort",
            commodity="Thermal Coal",
            cargo_mt=10000,
            vessel_master=[VESSEL_FITS],
            port_berth_master=[BERTH_TIGHT],
            cargo_master=[CARGO_COAL],
        )
        for vc in report.vessel_class_results:
            assert vc.overall_status != FeasibilityStatus.FEASIBLE

    def test_missing_vessel_dwt_prevents_feasible_verdict(self):
        report = evaluate_vessel_port_feasibility(
            origin="Anywhere",
            destination="TestPortA",
            commodity="Thermal Coal",
            cargo_mt=10000,
            vessel_master=[VESSEL_MISSING_DWT],
            port_berth_master=[BERTH_GENEROUS],
            cargo_master=[
                {**CARGO_COAL, "Candidate Vessel Types": "TestMissingDWT"}
            ],
        )
        for vc in report.vessel_class_results:
            assert vc.overall_status != FeasibilityStatus.FEASIBLE


# ---------------------------------------------------------------------------
# Tests: INFEASIBLE — a known constraint fails
# ---------------------------------------------------------------------------

class TestInfeasible:
    def test_oversized_vessel_is_infeasible(self):
        """VESSEL_TOO_LARGE has draft 19m but berth allows 11m → INFEASIBLE."""
        report = evaluate_vessel_port_feasibility(
            origin="Anywhere",
            destination="TestPortA",
            commodity="Thermal Coal",
            cargo_mt=10000,
            vessel_master=[VESSEL_TOO_LARGE],
            port_berth_master=[BERTH_TIGHT],
            cargo_master=[CARGO_COAL],
        )
        assert any(
            vc.overall_status == FeasibilityStatus.INFEASIBLE
            for vc in report.vessel_class_results
        )

    def test_cargo_exceeds_dwt_is_infeasible(self):
        """Requesting more cargo than a vessel's DWT must produce INFEASIBLE."""
        report = evaluate_vessel_port_feasibility(
            origin="Anywhere",
            destination="TestPortA",
            commodity="Thermal Coal",
            cargo_mt=999_999,   # Deliberately exceeds VESSEL_FITS DWT of 38000
            vessel_master=[VESSEL_FITS],
            port_berth_master=[BERTH_GENEROUS],
            cargo_master=[CARGO_COAL],
        )
        assert any(
            vc.overall_status == FeasibilityStatus.INFEASIBLE
            for vc in report.vessel_class_results
        )

    def test_infeasible_result_lists_failed_constraints(self):
        report = evaluate_vessel_port_feasibility(
            origin="Anywhere",
            destination="TestPortA",
            commodity="Thermal Coal",
            cargo_mt=10000,
            vessel_master=[VESSEL_TOO_LARGE],
            port_berth_master=[BERTH_TIGHT],
            cargo_master=[CARGO_COAL],
        )
        for vc in report.vessel_class_results:
            if vc.overall_status == FeasibilityStatus.INFEASIBLE:
                # At least one berth result should name a specific failed constraint
                all_failed = [
                    c
                    for br in vc.berth_results
                    for c in br.failed_constraints
                ]
                assert len(all_failed) > 0


# ---------------------------------------------------------------------------
# Tests: FEASIBLE — all constraints pass using verified data
# ---------------------------------------------------------------------------

class TestFeasible:
    def test_small_vessel_generous_berth_is_feasible(self):
        """VESSEL_FITS fits inside BERTH_GENEROUS on every constraint."""
        report = evaluate_vessel_port_feasibility(
            origin="Anywhere",
            destination="TestPortA",
            commodity="Thermal Coal",
            cargo_mt=20000,   # Below DWT of 38000
            vessel_master=[VESSEL_FITS],
            port_berth_master=[BERTH_GENEROUS],
            cargo_master=[CARGO_COAL],
        )
        assert any(
            vc.overall_status == FeasibilityStatus.FEASIBLE
            for vc in report.vessel_class_results
        )

    def test_feasible_requires_all_constraints_checked(self):
        """
        If FEASIBLE is returned, berth results must NOT list any missing fields
        for that berth (because missing fields lead to INSUFFICIENT_DATA, not FEASIBLE).
        """
        report = evaluate_vessel_port_feasibility(
            origin="Anywhere",
            destination="TestPortA",
            commodity="Thermal Coal",
            cargo_mt=20000,
            vessel_master=[VESSEL_FITS],
            port_berth_master=[BERTH_GENEROUS],
            cargo_master=[CARGO_COAL],
        )
        for vc in report.vessel_class_results:
            if vc.overall_status == FeasibilityStatus.FEASIBLE:
                for br in vc.berth_results:
                    assert br.status == FeasibilityStatus.FEASIBLE
                    assert len(br.missing_fields) == 0

    def test_vessel_fits_at_least_one_berth_is_feasible(self):
        """
        With one tight berth and one generous berth, the vessel should be FEASIBLE overall
        because it fits the generous berth (at least one berth passing → FEASIBLE).
        """
        report = evaluate_vessel_port_feasibility(
            origin="Anywhere",
            destination="TestPortA",
            commodity="Thermal Coal",
            cargo_mt=20000,
            vessel_master=[VESSEL_FITS],
            port_berth_master=[BERTH_TIGHT, BERTH_GENEROUS],
            cargo_master=[CARGO_COAL],
        )
        test_type_results = [
            vc for vc in report.vessel_class_results
            if vc.vessel_type == "TestHandysize"
        ]
        assert len(test_type_results) == 1
        assert test_type_results[0].overall_status == FeasibilityStatus.FEASIBLE


# ---------------------------------------------------------------------------
# Tests: using real project data (integration smoke tests)
# ---------------------------------------------------------------------------

class TestWithRealDataSmoke:
    """
    Smoke tests that load the actual shipping_dataset.json.
    These tests verify the module is integrated with real data without
    asserting specific outcomes (which depend on the dataset contents).
    """

    @pytest.fixture
    def real_data(self):
        from app.data_acquisition.dataset_loader import (
            get_vessel_master,
            get_port_berth_master,
            get_cargo_master,
        )
        return {
            "vessels": get_vessel_master(),
            "ports": get_port_berth_master(),
            "cargoes": get_cargo_master(),
        }

    def test_real_data_loads(self, real_data):
        assert len(real_data["vessels"]) > 0
        assert len(real_data["ports"]) > 0
        assert len(real_data["cargoes"]) > 0

    def test_thermal_coal_to_paradip_returns_report(self, real_data):
        """Known route: Thermal Coal → Paradip. Dataset has Paradip berths."""
        report = evaluate_vessel_port_feasibility(
            origin="Australia",   # Not in port master; origin check expected to warn
            destination="Paradip",
            commodity="Thermal Coal",
            cargo_mt=70000,
            vessel_master=real_data["vessels"],
            port_berth_master=real_data["ports"],
            cargo_master=real_data["cargoes"],
        )
        assert report is not None
        assert len(report.vessel_class_results) > 0

    def test_capesize_paradip_is_infeasible(self, real_data):
        """
        Per the real compatibility sheet (09_Compatibility), Capesize is
        incompatible with all Paradip berths (draft exceeds limits).
        """
        report = evaluate_vessel_port_feasibility(
            origin="Australia",
            destination="Paradip",
            commodity="Thermal Coal",
            cargo_mt=70000,
            vessel_master=real_data["vessels"],
            port_berth_master=real_data["ports"],
            cargo_master=real_data["cargoes"],
        )
        capesize_results = [
            vc for vc in report.vessel_class_results
            if "capesize" in vc.vessel_type.lower()
        ]
        # Only assert if a Capesize was evaluated (cargo master must list it)
        if capesize_results:
            assert capesize_results[0].overall_status == FeasibilityStatus.INFEASIBLE, (
                "Capesize should be INFEASIBLE at Paradip based on draft constraints in dataset"
            )

    def test_dhamra_returns_insufficient_data(self, real_data):
        """
        Dhamra berths have empty dimensional fields in the dataset.
        Must produce INSUFFICIENT_DATA, never FEASIBLE.
        """
        report = evaluate_vessel_port_feasibility(
            origin="Australia",
            destination="Dhamra",
            commodity="Thermal Coal",
            cargo_mt=50000,
            vessel_master=real_data["vessels"],
            port_berth_master=real_data["ports"],
            cargo_master=real_data["cargoes"],
        )
        for vc in report.vessel_class_results:
            assert vc.overall_status != FeasibilityStatus.FEASIBLE, (
                f"Vessel {vc.vessel_type!r} must not be FEASIBLE for Dhamra "
                "because Dhamra berth dimensions are missing in the dataset"
            )




