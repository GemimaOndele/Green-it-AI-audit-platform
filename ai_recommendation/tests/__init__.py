"""
Unit tests for the AI recommendation engine.
Tests integration with energy_metrics and validation of recommendation rules.
"""

from .test_engine import TestRecommendationEngine
from .test_rules import TestCoolingRules, TestITRules, TestPowerRules

__all__ = [
    'TestRecommendationEngine',
    'TestCoolingRules',
    'TestITRules',
    'TestPowerRules'
]