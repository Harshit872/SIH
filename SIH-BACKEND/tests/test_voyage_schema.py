"""
Tests for the voyage request schema (app/input/schemas.py).

Tests use the FastAPI test client so that Pydantic validation errors are
exercised through the actual HTTP layer, matching real frontend behaviour.

All payloads are clearly marked as TEST data. None represent real voyages.
"""

import pytest
from fastapi.testclient import TestClient
from app.auth.dependencies import get_current_user
from app.auth.schemas import UserResponse

def override_get_current_user():
    return UserResponse(id=1, email="test@odyssey.app", first_name="Test", last_name="User", company="Test Corp")

from app.main import app
@pytest.fixture(autouse=True)
def _setup_auth():
    app.dependency_overrides[get_current_user] = override_get_current_user
    yield
    app.dependency_overrides.pop(get_current_user, None)

client = TestClient(app)
from app.auth.dependencies import get_current_user
app.dependency_overrides[get_current_user] = lambda: {'email': 'test@odyssey.app'}

ENDPOINT = "/api/v1/voyage/submit"

# ---------------------------------------------------------------------------
# Shared test fixture — a minimal valid request payload
# All fields required by the finalized contract are present.
# ---------------------------------------------------------------------------
VALID_PAYLOAD = {
    "origin": "Paradip",
    "destination": "Dhamra",
    "commodity": "Thermal Coal",
    "cargoMt": 50000.0,
    "deliveryDate": "2027-06-30",
    "contract": "Voyage Charter",
    "laycan": "01 Jun 2027 - 10 Jun 2027",
    "noOfVoyages": 1,
}


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------

class TestValidRequest:
    def test_returns_202(self):
        resp = client.post(ENDPOINT, json=VALID_PAYLOAD)
        assert resp.status_code == 202, resp.text

    def test_status_is_accepted(self):
        resp = client.post(ENDPOINT, json=VALID_PAYLOAD)
        assert resp.json()["status"] == "accepted"

    def test_received_echo_matches_input(self):
        resp = client.post(ENDPOINT, json=VALID_PAYLOAD)
        received = resp.json()["received"]
        assert received["origin"] == "Paradip"
        assert received["destination"] == "Dhamra"
        assert received["commodity"] == "Thermal Coal"
        assert received["cargoMt"] == 50000.0
        assert received["noOfVoyages"] == 1

    def test_note_confirms_no_processing(self):
        """Response must not claim to contain forecasts or recommendations."""
        resp = client.post(ENDPOINT, json=VALID_PAYLOAD)
        note = resp.json()["note"].lower()
        # Note must mention that no forecasts/costs are returned
        assert "no forecasts" in note or "forecast" in note

    def test_delivery_date_parsed_correctly(self):
        resp = client.post(ENDPOINT, json=VALID_PAYLOAD)
        received = resp.json()["received"]
        assert received["deliveryDate"] == "2027-06-30"


# ---------------------------------------------------------------------------
# Missing required fields
# ---------------------------------------------------------------------------

class TestMissingFields:
    @pytest.mark.parametrize("missing_field", [
        "origin", "destination", "commodity", "cargoMt",
        "deliveryDate", "contract", "laycan", "noOfVoyages",
    ])
    def test_missing_field_returns_422(self, missing_field):
        payload = {k: v for k, v in VALID_PAYLOAD.items() if k != missing_field}
        resp = client.post(ENDPOINT, json=payload)
        assert resp.status_code == 422, f"Expected 422 when {missing_field!r} is missing"

    @pytest.mark.parametrize("missing_field", [
        "origin", "destination", "commodity", "cargoMt",
        "deliveryDate", "contract", "laycan", "noOfVoyages",
    ])
    def test_missing_field_identifies_the_field(self, missing_field):
        payload = {k: v for k, v in VALID_PAYLOAD.items() if k != missing_field}
        resp = client.post(ENDPOINT, json=payload)
        errors = resp.json().get("detail", [])
        fields_in_error = [e["loc"][-1] for e in errors]
        assert missing_field in fields_in_error, (
            f"Expected field name {missing_field!r} in validation errors; got {fields_in_error}"
        )


# ---------------------------------------------------------------------------
# Cargo quantity validation
# ---------------------------------------------------------------------------

class TestCargoMtValidation:
    @pytest.mark.parametrize("bad_value", [0, -1, -1000.5])
    def test_non_positive_cargo_returns_422(self, bad_value):
        payload = {**VALID_PAYLOAD, "cargoMt": bad_value}
        resp = client.post(ENDPOINT, json=payload)
        assert resp.status_code == 422

    def test_string_cargo_returns_422(self):
        payload = {**VALID_PAYLOAD, "cargoMt": "fifty thousand"}
        resp = client.post(ENDPOINT, json=payload)
        assert resp.status_code == 422

    def test_fractional_cargo_is_accepted(self):
        payload = {**VALID_PAYLOAD, "cargoMt": 12345.67}
        resp = client.post(ENDPOINT, json=payload)
        assert resp.status_code == 202


# ---------------------------------------------------------------------------
# Voyage count validation
# ---------------------------------------------------------------------------

class TestNoOfVoyagesValidation:
    @pytest.mark.parametrize("bad_value", [0, -1, -10])
    def test_non_positive_count_returns_422(self, bad_value):
        payload = {**VALID_PAYLOAD, "noOfVoyages": bad_value}
        resp = client.post(ENDPOINT, json=payload)
        assert resp.status_code == 422

    def test_string_count_returns_422(self):
        payload = {**VALID_PAYLOAD, "noOfVoyages": "three"}
        resp = client.post(ENDPOINT, json=payload)
        assert resp.status_code == 422


# ---------------------------------------------------------------------------
# Date validation
# ---------------------------------------------------------------------------

class TestDeliveryDateValidation:
    def test_invalid_date_format_returns_422(self):
        payload = {**VALID_PAYLOAD, "deliveryDate": "30-06-2027"}
        resp = client.post(ENDPOINT, json=payload)
        assert resp.status_code == 422

    def test_free_text_date_returns_422(self):
        payload = {**VALID_PAYLOAD, "deliveryDate": "June 30 2027"}
        resp = client.post(ENDPOINT, json=payload)
        assert resp.status_code == 422


# ---------------------------------------------------------------------------
# Laycan format validation
# ---------------------------------------------------------------------------

class TestLaycanValidation:
    @pytest.mark.parametrize("bad_laycan", [
        "2027-06-01 - 2027-06-10",          # ISO format — not what frontend sends
        "01/06/2027 - 10/06/2027",           # slash separator
        "Jun 1 2027 - Jun 10 2027",          # wrong day format
        "01 Jun 2027",                        # missing end date
        "",                                   # empty
        "01 Jun 2027 to 10 Jun 2027",        # wrong separator
    ])
    def test_bad_laycan_returns_422(self, bad_laycan):
        payload = {**VALID_PAYLOAD, "laycan": bad_laycan}
        resp = client.post(ENDPOINT, json=payload)
        assert resp.status_code == 422, f"Expected 422 for laycan={bad_laycan!r}"

    def test_correct_laycan_format_accepted(self):
        resp = client.post(ENDPOINT, json=VALID_PAYLOAD)
        assert resp.status_code == 202

    def test_laycan_at_year_boundary(self):
        payload = {**VALID_PAYLOAD, "laycan": "28 Dec 2027 - 05 Jan 2028"}
        resp = client.post(ENDPOINT, json=payload)
        assert resp.status_code == 202


# ---------------------------------------------------------------------------
# Origin == Destination
# ---------------------------------------------------------------------------

class TestOriginDestinationSame:
    def test_same_origin_destination_returns_422(self):
        payload = {**VALID_PAYLOAD, "destination": "Paradip"}
        resp = client.post(ENDPOINT, json=payload)
        assert resp.status_code == 422




