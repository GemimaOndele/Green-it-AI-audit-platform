"""Case study data loaders.

This module provides a small loader for the Google case study dataset.
It is intentionally lightweight and only used when a caller requests the
"google" case study mode.
"""

import json
import os
from typing import Any, Dict, Optional


def _project_root() -> str:
    """Return the project root directory (one level above ai_recommendation)."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def _case_study_path(filename: str) -> str:
    return os.path.join(_project_root(), "case_study", filename)


def load_case_study(name: str = "google") -> Dict[str, Any]:
    """Load a named case study dataset.

    Currently supported values:
      - "google" (loads `case_study/google_case_study.json`)

    Raises:
        FileNotFoundError: If the case study file doesn't exist.
        ValueError: If the case study name is unknown.
    """
    name = name.lower().strip()

    if name == "google":
        path = _case_study_path("google_case_study.json")
    else:
        raise ValueError(f"Unsupported case study: {name}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_google_baseline_inputs() -> Dict[str, Any]:
    """Return a normalized set of UI-like inputs derived from the Google case study."""
    data = load_case_study("google")
    inputs = data.get("inputs", {})

    # Map fields from the case study to our UI/engine field names.
    return {
        "it_energy_mwh": inputs.get("it_energy_mwh_per_year"),
        "total_energy_mwh": inputs.get("total_energy_mwh_per_year"),
        "carbon_factor": inputs.get("carbon_factor_kg_co2_per_kwh"),
        "servers": inputs.get("num_servers_approx"),
        "cpu_utilization_pct": inputs.get("avg_cpu_utilization_percent"),
        "cooling_setpoint_c": inputs.get("cooling_setpoint_celsius"),
        "has_aisle_containment": inputs.get("aisle_containment"),
        "virtualization_level_pct": 0.0,  # Not provided, default to 0
        "cooling_type": inputs.get("cooling_type"),
    }


def get_case_study_baseline(name: str) -> Dict[str, Any]:
    """Return the baseline section for a given case study."""
    data = load_case_study(name)
    return data.get("computed_metrics", {})
