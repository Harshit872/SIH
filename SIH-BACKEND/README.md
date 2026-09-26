# The Odyssey - Backend

Backend API for "The Odyssey" — a freight forecasting and charter optimization system.

## Project Structure & Status

| Module | Status | Notes |
|---|---|---|
| `api/` | Implemented | Core route definitions |
| `input/` | Implemented | Validated Pydantic request/response schemas |
| `config/` | Implemented | Environment-aware settings (`pydantic-settings`) |
| `data_acquisition/` | Implemented | Reads verified `shipping_dataset.json` from frontend tree |
| `optimization/vessel_feasibility/` | Implemented | Physical/dimensional constraint evaluation module |
| `optimization/cost_engine/` | Implemented | Modular voyage cost evaluation |
| `optimization/risk_engine/` | Implemented | Rule-based operational risk assessment |
| `deadline_validator/` | Implemented | Validates laycan and deadlines without inventing ETAs |
| `scenario_evaluation/` | Implemented | Compares Book Now vs Wait scenarios |

## Endpoints Overview

1. **`POST /api/v1/voyage/submit`**: Validates request inputs.
2. **`POST /api/v1/voyage/feasibility`**: Evaluates physical dimensional constraints.
3. **`POST /api/v1/voyage/cost`**: Modular calculation of freight, bunker, port charges, demurrage. Explicitly marks unavailable data as `MISSING_INPUT` or `UNSUPPORTED`.
4. **`POST /api/v1/voyage/risk`**: Evaluates explicitly provided risks (schedule buffer, feasibility, cost completion) without assuming weather or market fluctuations.
5. **`POST /api/v1/voyage/schedule`**: Validates `laycan` against `deliveryDate`.
6. **`POST /api/v1/evaluate_scenarios`**: Compares "Book Now", "Wait 7 Days", and "Wait 14 Days" based on data availability.

## Limitations & Missing Data Rules
- The backend does **not** assume default operational rates (e.g. daily demurrage, waiting time) or future freight rates. 
- If transit, loading, and discharge days are absent, ETA calculation correctly yields `INSUFFICIENT_DATA`.
- Mixed-currency totals or partially supported costs explicitly trigger warnings rather than silent sums.

## Running the Backend and Tests

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run API server (dev mode)
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Run all tests
python -m pytest tests/ -v
```
