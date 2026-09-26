"""
Static dataset loader for The Odyssey backend.

Reads shipping_dataset.json from the FRONTEND source tree (the only location
where the processed dataset currently exists) and exposes typed accessor
functions identical in purpose to DatasetService.ts on the frontend.

IMPORTANT: This module performs file I/O at import time using a path relative
to the repository root.  When a proper data layer is introduced (Phase 5+),
replace this with a database call or a configurable data path.

The dataset path can be overridden via the environment variable:
    ODYSSEY_DATASET_PATH=<absolute path to shipping_dataset.json>
"""

import json
import os
from pathlib import Path
from functools import lru_cache

_DEFAULT_DATASET_RELATIVE = (
    Path(__file__).resolve().parents[3]  # reaches SIH root (SIH-BACKEND/../)
    / "SIH-FRONTEND"
    / "src"
    / "data"
    / "generated"
    / "shipping_dataset.json"
)


def _load_raw() -> dict:
    path_env = os.environ.get("ODYSSEY_DATASET_PATH")
    dataset_path = Path(path_env) if path_env else _DEFAULT_DATASET_RELATIVE
    if not dataset_path.exists():
        raise FileNotFoundError(
            f"shipping_dataset.json not found at {dataset_path}. "
            "Set the ODYSSEY_DATASET_PATH environment variable to the correct path."
        )
    with open(dataset_path, encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def _dataset() -> dict:
    return _load_raw()


def get_vessel_master() -> list[dict]:
    """Returns all records from sheet 03_Vessel_Master."""
    return _dataset().get("03_Vessel_Master", [])


def get_port_berth_master() -> list[dict]:
    """Returns all records from sheet 04_Port_Berth_Master."""
    return _dataset().get("04_Port_Berth_Master", [])


def get_cargo_master() -> list[dict]:
    """Returns all records from sheet 05_Cargo_Master."""
    return _dataset().get("05_Cargo_Master", [])


def get_route_benchmarks() -> list[dict]:
    """Returns all records from sheet 06_Route_Benchmarks."""
    return _dataset().get("06_Route_Benchmarks", [])


def get_unique_port_names() -> list[str]:
    """Returns sorted unique port names from the port berth master."""
    return sorted({r.get("Port", "") for r in get_port_berth_master() if r.get("Port")})
