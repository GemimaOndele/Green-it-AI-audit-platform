"""
GreenDC Audit Platform - AI Recommendation Engine
Author: Joseph Fabrice Tsapfack
Role: AI & Recommendation Engine Lead
Team: GreenAI Systems

This module provides rule-based, explainable recommendations for data center
energy optimization, integrated with Mike-Brady's energy metrics module.
"""

from .engine import RecommendationEngine
from typing import Any

from .models import AuditContext, Recommendation, DifficultyLevel, ImpactLevel
from .prioritizer import prioritize_recommendations
from .exceptions import InsufficientDataError, InvalidContextError

# Keep backward compatibility with Gemima's original code
from .rules import build_recommendations as original_build_recommendations

# Case study support
from .case_study import get_google_baseline_inputs, load_case_study


def build_recommendations(
    case_study: str | None = None,
    **kwargs: Any,
) -> list[Recommendation]:
    """Build recommendations.

    When `case_study` is provided (e.g. "google"), the engine will use the
    corresponding baseline inputs (from `case_study/google_case_study.json`).

    This keeps the output consistent with the front-end's expectations, while
    allowing the AI engine to be run against a known case-study baseline.

    Parameters:
        case_study: Optional case study name ("google").
        kwargs: Same keyword arguments as the original build_recommendations.

    Returns:
        A list of Recommendation objects (same shape as the legacy rules engine).
    """

    if case_study is not None:
        # Base inputs come from the case study dataset.
        inputs = get_google_baseline_inputs() if case_study.lower().strip() == "google" else {}
        # Allow callers to override specific fields (UI override behavior).
        inputs.update(kwargs)
        return original_build_recommendations(**inputs)

    # Default behavior: behave like the legacy module.
    return original_build_recommendations(**kwargs)

__all__ = [
    # Main engine
    "RecommendationEngine",
    "AuditContext",
    "Recommendation",

    # Utilities
    "build_recommendations",
    "prioritize_recommendations",
    "DifficultyLevel",
    "ImpactLevel",

    # Exceptions
    "InsufficientDataError",
    "InvalidContextError",

    # Backward compatibility (for Gemima's existing code)
    "original_build_recommendations",
    "load_case_study",
]

__version__ = "1.0.0"