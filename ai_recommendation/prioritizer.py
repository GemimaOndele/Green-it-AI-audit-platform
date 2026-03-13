"""
Recommendation prioritization logic for Nandaa's simulation engine.
"""

from typing import List
from .models import Recommendation, AuditContext, DifficultyLevel


def prioritize_recommendations(
    recommendations: List[Recommendation],
    context: AuditContext
) -> List[Recommendation]:
    """
    Prioritize recommendations for Nandaa's simulation engine.
    
    Prioritization strategy:
    1. Quick wins (high impact, easy to implement) come first
    2. Then medium impact, medium difficulty
    3. Long-term investments last
    
    Args:
        recommendations: List of all recommendations
        context: Audit context for baseline values
    
    Returns:
        Sorted list of recommendations by priority
    """
    
    def calculate_priority_score(rec: Recommendation) -> float:
        """
        Calculate priority score (higher = better)
        
        Score formula:
        - Impact: % of 25% CO2 target achieved (capped at 1.0)
        - Difficulty multiplier: Easy (1.0), Medium (0.7), Hard (0.4)
        - Quick win bonus: +0.2 for easy + high impact
        """
        
        # Impact score (0-1) based on contribution to 25% target
        target_co2 = context.co2_tonnes_per_year * 0.25
        if target_co2 > 0:
            impact_score = min(rec.co2_savings_tonnes / target_co2, 1.0)
        else:
            impact_score = 0
        
        # Difficulty multiplier (easier = higher score)
        difficulty_mult = {
            DifficultyLevel.EASY: 1.0,
            DifficultyLevel.MEDIUM: 0.7,
            DifficultyLevel.HARD: 0.4
        }.get(rec.difficulty, 0.5)
        
        # Quick win bonus (easy + high impact)
        quick_win_bonus = 0.0
        if (rec.difficulty == DifficultyLevel.EASY and 
            rec.impact_level.value == "high" and
            impact_score > 0.3):
            quick_win_bonus = 0.2
        
        # Base score
        score = impact_score * difficulty_mult + quick_win_bonus
        
        return score
    
    # Sort by priority score descending
    sorted_recs = sorted(
        recommendations,
        key=calculate_priority_score,
        reverse=True
    )
    
    return sorted_recs


def get_quick_wins(
    recommendations: List[Recommendation],
    min_co2_savings: float = 10.0  # Minimum 10 tons CO2
) -> List[Recommendation]:
    """
    Extract quick win recommendations (easy + high impact)
    
    Args:
        recommendations: List of recommendations
        min_co2_savings: Minimum CO2 savings to qualify
    
    Returns:
        List of quick win recommendations
    """
    quick_wins = []
    
    for rec in recommendations:
        if (rec.difficulty == DifficultyLevel.EASY and
            rec.impact_level.value == "high" and
            rec.co2_savings_tonnes >= min_co2_savings):
            quick_wins.append(rec)
    
    return quick_wins


def get_recommendations_by_category(
    recommendations: List[Recommendation],
    category: str
) -> List[Recommendation]:
    """
    Filter recommendations by category
    
    Args:
        recommendations: List of recommendations
        category: Category to filter by
    
    Returns:
        Filtered recommendations
    """
    return [r for r in recommendations if r.category == category]


def format_for_simulation(
    recommendations: List[Recommendation]
) -> List[dict]:
    """
    Format recommendations for Nandaa's simulation module.
    
    Args:
        recommendations: Prioritized recommendations
    
    Returns:
        List of dicts ready for simulation
    """
    simulation_inputs = []
    
    for i, rec in enumerate(recommendations):
        simulation_inputs.append({
            'id': rec.id,
            'title': rec.title,
            'saving_pct': rec.estimated_saving_pct,
            'energy_savings_mwh': rec.energy_savings_mwh,
            'co2_savings_tonnes': rec.co2_savings_tonnes,
            'cost_savings_eur': rec.cost_savings_eur,
            'difficulty': rec.difficulty.value,
            'category': rec.category,
            'implementation_order': i + 1,
            'dependencies': rec.prerequisites  # For simulation sequencing
        })
    
    return simulation_inputs