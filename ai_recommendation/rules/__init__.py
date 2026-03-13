"""
Rule modules for different recommendation categories.
"""

from .cooling_rules import get_cooling_recommendations
from .it_rules import get_it_recommendations
from .power_rules import get_power_recommendations

__all__ = [
    "get_cooling_recommendations",
    "get_it_recommendations",
    "get_power_recommendations"
]