"""
Main recommendation engine orchestrator.
Integrates with Mike-Brady's energy metrics and prepares data for Nandaa's simulation.
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from .models import (
    AuditContext, Recommendation, RecommendationResult,
    DifficultyLevel, ImpactLevel, Category,
    GOOGLE_PUE, INDUSTRY_AVG_PUE
)
from .rules.cooling_rules import get_cooling_recommendations
from .rules.it_rules import get_it_recommendations
from .rules.power_rules import get_power_recommendations
from .prioritizer import prioritize_recommendations
from .exceptions import InsufficientDataError, InvalidContextError


class RecommendationEngine:
    """
    Main AI recommendation engine.
    
    This engine:
    1. Takes validated metrics from Mike-Brady's module
    2. Applies rule-based logic to generate recommendations
    3. Calculates absolute savings (CO2, energy, cost)
    4. Prioritizes for Nandaa's simulation
    5. Formats for Gemima's frontend
    """
    
    def __init__(self, verbose: bool = False):
        """
        Initialize the recommendation engine.
        
        Args:
            verbose: Enable detailed logging
        """
        self.logger = logging.getLogger(__name__)
        if verbose:
            self.logger.setLevel(logging.DEBUG)
        
        self.logger.info("Initializing RecommendationEngine")
    
    def generate_recommendations(self, context: AuditContext) -> RecommendationResult:
        """
        Generate prioritized recommendations based on audit context.
        
        Args:
            context: Complete audit context (from Mike-Brady's metrics + UI)
            
        Returns:
            RecommendationResult with recommendations, summary, and target analysis
            
        Raises:
            InsufficientDataError: If required data is missing
            InvalidContextError: If context validation fails
        """
        self.logger.info(f"Generating recommendations for PUE: {context.pue:.2f}")
        
        # Step 1: Validate input data
        validation_issues = context.validate()
        if validation_issues:
            error_msg = f"Invalid audit context: {', '.join(validation_issues)}"
            self.logger.error(error_msg)
            raise InvalidContextError(error_msg)
        
        if context.total_energy_mwh <= 0:
            raise InsufficientDataError("total_energy_mwh must be positive")
        
        # Step 2: Gather all recommendations from rule modules
        all_recs = []
        all_recs.extend(get_cooling_recommendations(context))
        all_recs.extend(get_it_recommendations(context))
        all_recs.extend(get_power_recommendations(context))
        
        self.logger.debug(f"Generated {len(all_recs)} raw recommendations")
        
        # Step 3: Calculate absolute savings using Mike-Brady's metrics
        for rec in all_recs:
            # CO2 savings = total CO2 * saving percentage
            rec.co2_savings_tonnes = context.co2_tonnes_per_year * (rec.estimated_saving_pct / 100)
            
            # Energy savings = total energy * saving percentage
            rec.energy_savings_mwh = context.total_energy_mwh * (rec.estimated_saving_pct / 100)
            
            # Cost savings = energy savings * cost per kWh * 1000 (MWh to kWh)
            rec.cost_savings_eur = rec.energy_savings_mwh * 1000 * context.energy_cost_per_kwh
        
        # Step 4: Add benchmark comparison if relevant
        if context.pue > self.INDUSTRY_AVG_PUE:
            self._add_benchmark_comparison(all_recs, context)
        
        # Step 5: Prioritize for Nandaa's simulation
        prioritized = prioritize_recommendations(all_recs, context)
        
        # Step 6: Check if 25% CO2 reduction target is achievable
        total_co2_savings = sum(r.co2_savings_tonnes for r in prioritized)
        target_25pct = context.co2_tonnes_per_year * 0.25
        target_achievable = total_co2_savings >= target_25pct
        
        # Step 7: Prepare summary statistics
        summary = self._create_summary(prioritized, context, target_25pct, total_co2_savings)
        
        # Step 8: Prepare context for frontend
        context_summary = self._create_context_summary(context)
        
        self.logger.info(f"Generated {len(prioritized)} prioritized recommendations")
        self.logger.info(f"Total CO2 savings: {total_co2_savings:.1f} tons ({total_co2_savings/context.co2_tonnes_per_year*100:.1f}%)")
        self.logger.info(f"Target 25% achievable: {target_achievable}")
        
        return RecommendationResult(
            recommendations=prioritized,
            summary=summary,
            context=context_summary,
            target_achievable=target_achievable
        )
    
    def _add_benchmark_comparison(self, recommendations: List[Recommendation], context: AuditContext):
        """Add benchmark comparison to industry leaders"""
        
        # Only add for inefficient data centers
        if context.pue > 1.5:
            benchmark_rec = Recommendation(
                id="BENCH-001",
                title="Benchmark Against Industry Leaders",
                description=(
                    f"Your PUE of {context.pue:.2f} is above Google's {self.GOOGLE_PUE} "
                    f"and industry average of {self.INDUSTRY_AVG_PUE}. Study their best practices: "
                    "free cooling, aisle containment, and AI-based optimization."
                ),
                category=Category.BENCHMARK.value,
                estimated_saving_pct=0.0,  # Informational only
                difficulty=DifficultyLevel.EASY,
                impact_level=ImpactLevel.LOW,
                prerequisites=[],
                steps=[
                    "Review Google's environmental report",
                    "Audit current cooling infrastructure",
                    "Identify gaps vs. best practices",
                    "Create improvement roadmap"
                ],
                logic_explanation=(
                    f"Industry leaders like Google achieve PUE {self.GOOGLE_PUE} through "
                    "comprehensive optimization. Learning from them can help identify "
                    "improvement opportunities for your facility."
                ),
                references=[
                    "Google Environmental Report 2024",
                    "The Green Grid - Data Center Efficiency Benchmarks"
                ],
                implementation_time_months=1,
                roi_months=None  # Informational only
            )
            recommendations.append(benchmark_rec)
    
    def _create_summary(self, 
                        recommendations: List[Recommendation], 
                        context: AuditContext,
                        target_25pct: float,
                        total_co2_savings: float) -> Dict[str, Any]:
        """Create summary statistics for frontend"""
        
        # Group by difficulty
        by_difficulty = {
            'easy': len([r for r in recommendations if r.difficulty == DifficultyLevel.EASY]),
            'medium': len([r for r in recommendations if r.difficulty == DifficultyLevel.MEDIUM]),
            'hard': len([r for r in recommendations if r.difficulty == DifficultyLevel.HARD])
        }
        
        # Group by category
        by_category = {}
        for rec in recommendations:
            if rec.category not in by_category:
                by_category[rec.category] = 0
            by_category[rec.category] += 1
        
        # Calculate top recommendations
        top_3 = recommendations[:3] if recommendations else []
        
        return {
            'total_recommendations': len(recommendations),
            'total_co2_savings_tonnes': round(total_co2_savings, 2),
            'total_energy_savings_mwh': round(sum(r.energy_savings_mwh for r in recommendations), 2),
            'total_cost_savings_eur': round(sum(r.cost_savings_eur for r in recommendations), 2),
            'target_25pct_co2_tonnes': round(target_25pct, 2),
            'target_gap_tonnes': round(max(0, target_25pct - total_co2_savings), 2),
            'target_progress_pct': round(min(100, (total_co2_savings / target_25pct * 100) if target_25pct > 0 else 0), 1),
            'by_difficulty': by_difficulty,
            'by_category': by_category,
            'top_recommendations': [r.title for r in top_3],
            'pue_rating': context.pue_rating,
            'action_needed': context.action_needed
        }
    
    def _create_context_summary(self, context: AuditContext) -> Dict[str, Any]:
        """Create context summary for frontend"""
        return {
            'baseline_pue': round(context.pue, 2),
            'baseline_dcie': round(context.dcie_percent, 1),
            'baseline_co2_tonnes': round(context.co2_tonnes_per_year, 1),
            'total_energy_mwh': round(context.total_energy_mwh, 1),
            'it_energy_mwh': round(context.it_energy_mwh, 1),
            'num_servers': context.num_servers,
            'cpu_utilization_pct': context.cpu_utilization_pct,
            'cooling_setpoint_c': context.cooling_setpoint_c,
            'has_aisle_containment': context.has_aisle_containment,
            'virtualization_level_pct': context.virtualization_level_pct,
            'google_benchmark_pue': self.GOOGLE_PUE,
            'industry_avg_pue': self.INDUSTRY_AVG_PUE,
            'generated_at': datetime.now().isoformat()
        }