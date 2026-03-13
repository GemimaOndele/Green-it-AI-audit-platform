"""
GreenDC Audit Platform - AI Recommendation Engine
Author: Joseph Fabrice Tsapfack
Role: AI & Recommendation Engine Lead
Team: GreenAI Systems

This module provides rule-based, explainable recommendations for data center
energy optimization, integrated with Mike-Brady's energy metrics module.
"""

from .engine import RecommendationEngine
from .models import AuditContext, Recommendation, DifficultyLevel, ImpactLevel
from .prioritizer import prioritize_recommendations
from .exceptions import InsufficientDataError, InvalidContextError

# Keep backward compatibility with Gemima's original code
from .rules import build_recommendations as original_build_recommendations

__all__ = [
    # Main engine
    "RecommendationEngine",
    "AuditContext",
    "Recommendation",
    
    # Utilities
    "prioritize_recommendations",
    "DifficultyLevel",
    "ImpactLevel",
    
    # Exceptions
    "InsufficientDataError",
    "InvalidContextError",
    
    # Backward compatibility (for Gemima's existing code)
    "original_build_recommendations"
]

__version__ = "1.0.0"