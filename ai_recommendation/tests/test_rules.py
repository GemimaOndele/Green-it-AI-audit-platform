"""
Unit tests for individual rule modules.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from ai_recommendation.models import AuditContext
from ai_recommendation.rules.cooling_rules import get_cooling_recommendations
from ai_recommendation.rules.it_rules import get_it_recommendations
from ai_recommendation.rules.power_rules import get_power_recommendations


class TestCoolingRules(unittest.TestCase):
    """Test cooling rules"""
    
    def test_low_setpoint_triggers_rule(self):
        context = AuditContext(
            it_power_kw=100,
            it_energy_mwh=876,
            total_energy_mwh=1400,
            carbon_factor_kg_per_kwh=0.3,
            pue=1.6,
            dcie_percent=62.5,
            co2_tonnes_per_year=420,
            pue_rating="Average",
            pue_description="",
            action_needed=True,
            num_servers=300,
            cpu_utilization_pct=30,
            cooling_setpoint_c=18,  # Low
            has_aisle_containment=False,
            virtualization_level_pct=50,
            cooling_type="air"
        )
        
        recs = get_cooling_recommendations(context)
        cooling_recs = [r for r in recs if r.id == "COOL-001"]
        self.assertEqual(len(cooling_recs), 1)
    
    def test_no_containment_triggers_rule(self):
        context = AuditContext(
            it_power_kw=100,
            it_energy_mwh=876,
            total_energy_mwh=1576,  # PUE 1.8
            carbon_factor_kg_per_kwh=0.3,
            pue=1.8,
            dcie_percent=55.6,
            co2_tonnes_per_year=473,
            pue_rating="Average",
            pue_description="",
            action_needed=True,
            num_servers=300,
            cpu_utilization_pct=30,
            cooling_setpoint_c=22,
            has_aisle_containment=False,  # No containment
            virtualization_level_pct=50,
            cooling_type="air"
        )
        
        recs = get_cooling_recommendations(context)
        containment_recs = [r for r in recs if r.id == "COOL-002"]
        self.assertEqual(len(containment_recs), 1)


class TestITRules(unittest.TestCase):
    """Test IT rules"""
    
    def test_low_utilization_triggers_rule(self):
        context = AuditContext(
            it_power_kw=100,
            it_energy_mwh=876,
            total_energy_mwh=1400,
            carbon_factor_kg_per_kwh=0.3,
            pue=1.6,
            dcie_percent=62.5,
            co2_tonnes_per_year=420,
            pue_rating="Average",
            pue_description="",
            action_needed=True,
            num_servers=300,
            cpu_utilization_pct=20,  # Low
            cooling_setpoint_c=22,
            has_aisle_containment=True,
            virtualization_level_pct=50,
            cooling_type="air"
        )
        
        recs = get_it_recommendations(context)
        consolidation_recs = [r for r in recs if r.id == "IT-001"]
        self.assertEqual(len(consolidation_recs), 1)
    
    def test_low_virtualization_triggers_rule(self):
        context = AuditContext(
            it_power_kw=100,
            it_energy_mwh=876,
            total_energy_mwh=1400,
            carbon_factor_kg_per_kwh=0.3,
            pue=1.6,
            dcie_percent=62.5,
            co2_tonnes_per_year=420,
            pue_rating="Average",
            pue_description="",
            action_needed=True,
            num_servers=300,
            cpu_utilization_pct=50,
            cooling_setpoint_c=22,
            has_aisle_containment=True,
            virtualization_level_pct=40,  # Low
            cooling_type="air"
        )
        
        recs = get_it_recommendations(context)
        virt_recs = [r for r in recs if r.id == "IT-002"]
        self.assertEqual(len(virt_recs), 1)


class TestPowerRules(unittest.TestCase):
    """Test power rules"""
    
    def test_high_pue_triggers_rule(self):
        context = AuditContext(
            it_power_kw=100,
            it_energy_mwh=876,
            total_energy_mwh=1840,  # PUE 2.1
            carbon_factor_kg_per_kwh=0.3,
            pue=2.1,
            dcie_percent=47.6,
            co2_tonnes_per_year=552,
            pue_rating="Poor",
            pue_description="",
            action_needed=True,
            num_servers=300,
            cpu_utilization_pct=30,
            cooling_setpoint_c=22,
            has_aisle_containment=False,
            virtualization_level_pct=50,
            cooling_type="air"
        )
        
        recs = get_power_recommendations(context)
        pue_recs = [r for r in recs if r.id == "PWR-001"]
        self.assertEqual(len(pue_recs), 1)


if __name__ == '__main__':
    unittest.main()