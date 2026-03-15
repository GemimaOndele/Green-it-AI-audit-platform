"""
Unit tests for recommendation engine.
Validates integration with Mike-Brady's metrics.
"""

import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from ai_recommendation.engine import RecommendationEngine
from ai_recommendation.models import AuditContext, DifficultyLevel, ImpactLevel
from ai_recommendation.exceptions import InvalidContextError, InsufficientDataError


class TestRecommendationEngine(unittest.TestCase):
    """Test suite for RecommendationEngine"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.engine = RecommendationEngine(verbose=False)
        
        # Sample context from Mike-Brady's sample_input.json
        self.valid_context = AuditContext(
            # From metrics
            it_power_kw=89.0,  # 780 MWh / 8760h * 1000
            it_energy_mwh=780.0,
            total_energy_mwh=1300.0,
            carbon_factor_kg_per_kwh=0.30,
            pue=1.6667,
            dcie_percent=60.0,
            co2_tonnes_per_year=390.0,
            pue_rating="Average",
            pue_description="Moderate efficiency — optimization recommended",
            action_needed=True,
            
            # From UI
            num_servers=320,
            cpu_utilization_pct=18.0,
            cooling_setpoint_c=19.0,
            has_aisle_containment=False,
            virtualization_level_pct=45.0,
            cooling_type="air"
        )
    
    def test_valid_context_generates_recommendations(self):
        """Test that valid context generates recommendations"""
        result = self.engine.generate_recommendations(self.valid_context)
        
        self.assertGreater(len(result.recommendations), 0)
        self.assertIn('total_recommendations', result.summary)
        self.assertIn('target_25pct_achievable', result.summary)
        
        # Check that total savings are calculated and positive
        total_co2_savings = sum(rec.co2_savings_tonnes for rec in result.recommendations)
        total_energy_savings = sum(rec.energy_savings_mwh for rec in result.recommendations)
        total_cost_savings = sum(rec.cost_savings_eur for rec in result.recommendations)

        self.assertGreater(total_co2_savings, 0)
        self.assertGreater(total_energy_savings, 0)
        self.assertGreater(total_cost_savings, 0)

        # Check individual recommendations that should have savings
        for rec in result.recommendations:
            if rec.estimated_saving_pct > 0:
                self.assertGreater(rec.co2_savings_tonnes, 0)
                self.assertGreater(rec.energy_savings_mwh, 0)
                self.assertGreater(rec.cost_savings_eur, 0)
    
    def test_invalid_context_raises_error(self):
        """Test that invalid context raises appropriate error"""
        invalid_context = AuditContext(
            it_power_kw=-1,  # Invalid
            it_energy_mwh=-1,
            total_energy_mwh=0,
            carbon_factor_kg_per_kwh=0,
            pue=0.5,  # Less than 1.0
            dcie_percent=200,  # >100
            co2_tonnes_per_year=-100,
            pue_rating="Invalid",
            pue_description="",
            action_needed=False,
            num_servers=-10,
            cpu_utilization_pct=150,  # >100
            cooling_setpoint_c=5,  # Too low
            has_aisle_containment=False,
            virtualization_level_pct=-5,
            cooling_type="air"
        )
        
        with self.assertRaises(InvalidContextError):
            self.engine.generate_recommendations(invalid_context)
    
    def test_google_benchmark_added_for_high_pue(self):
        """Test that Google benchmark is added for high PUE"""
        # High PUE context
        high_pue_context = AuditContext(
            it_power_kw=100,
            it_energy_mwh=876,
            total_energy_mwh=1752,  # PUE 2.0
            carbon_factor_kg_per_kwh=0.3,
            pue=2.0,
            dcie_percent=50.0,
            co2_tonnes_per_year=525.6,
            pue_rating="Poor",
            pue_description="High energy waste",
            action_needed=True,
            num_servers=400,
            cpu_utilization_pct=20,
            cooling_setpoint_c=18,
            has_aisle_containment=False,
            virtualization_level_pct=30,
            cooling_type="air"
        )
        
        result = self.engine.generate_recommendations(high_pue_context)
        
        # Check for benchmark recommendation
        benchmark_recs = [r for r in result.recommendations if r.id == "BENCH-001"]
        self.assertEqual(len(benchmark_recs), 1)
        
        # Check that Google PUE is mentioned
        self.assertIn("Google", benchmark_recs[0].description)
    
    def test_target_calculation(self):
        """Test that 25% target calculation is correct"""
        result = self.engine.generate_recommendations(self.valid_context)
        
        # Baseline CO2: 390 tons
        # Target 25%: 97.5 tons
        target = self.valid_context.co2_tonnes_per_year * 0.25
        
        self.assertEqual(result.summary['target_25pct_co2_tonnes'], 97.5)
        self.assertIn('target_progress_pct', result.summary)
    
    def test_recommendation_prioritization(self):
        """Test that recommendations are properly prioritized"""
        result = self.engine.generate_recommendations(self.valid_context)
        
        # First recommendation should be easy/medium difficulty
        if result.recommendations:
            first_rec = result.recommendations[0]
            self.assertIn(first_rec.difficulty, [DifficultyLevel.EASY, DifficultyLevel.MEDIUM])
    
    def test_zero_energy_raises_error(self):
        """Test that zero total energy raises error"""
        zero_context = AuditContext(
            it_power_kw=0,
            it_energy_mwh=0,
            total_energy_mwh=0,
            carbon_factor_kg_per_kwh=0.3,
            pue=1.0,  # Valid PUE
            dcie_percent=0,
            co2_tonnes_per_year=0,
            pue_rating="Invalid",
            pue_description="",
            action_needed=False,
            num_servers=0,
            cpu_utilization_pct=0,
            cooling_setpoint_c=20,
            has_aisle_containment=False,
            virtualization_level_pct=0,
            cooling_type="air"
        )
        
        with self.assertRaises(InsufficientDataError):
            self.engine.generate_recommendations(zero_context)


if __name__ == '__main__':
    unittest.main()