"""
Power infrastructure and PUE optimization recommendations.
Based on industry benchmarks and Mike-Brady's metrics.
"""

from typing import List
from ..models import (
    AuditContext, Recommendation, 
    DifficultyLevel, ImpactLevel, Category
)


def get_power_recommendations(context: AuditContext) -> List[Recommendation]:
    """
    Generate power infrastructure and PUE optimization recommendations.
    """
    recommendations = []
    
    # ===== RULE 1: Address high PUE =====
    if context.pue > 1.8:  # Poor PUE threshold from Mike-Brady's get_pue_rating()
        recommendations.append(
            Recommendation(
                id="PWR-001",
                title="Urgent PUE Reduction Program",
                description=(
                    f"Your PUE of {context.pue:.2f} is in the 'Poor' range. "
                    f"Immediate action needed to reduce energy waste."
                ),
                category=Category.POWER.value,
                estimated_saving_pct=15.0,  # Aggressive savings for poor PUE
                difficulty=DifficultyLevel.HARD,
                impact_level=ImpactLevel.HIGH,
                prerequisites=[
                    "Executive sponsorship",
                    "Energy audit budget",
                    "Engineering resources"
                ],
                steps=[
                    "Conduct comprehensive energy audit",
                    "Identify top 3 PUE contributors",
                    "Create 12-month improvement roadmap",
                    "Implement quick wins first",
                    "Track PUE monthly",
                    "Report progress to stakeholders"
                ],
                logic_explanation=(
                    f"Your PUE of {context.pue:.2f} indicates significant non-IT energy waste. "
                    f"The industry average is {RecommendationEngine.INDUSTRY_AVG_PUE}. "
                    "Reducing to 1.5 could save 15-20% of total energy."
                ),
                references=[
                    "Mike-Brady's get_pue_rating() thresholds",
                    "The Green Grid - PUE Best Practices"
                ],
                implementation_time_months=12,
                roi_months=18
            )
        )
    
    # ===== RULE 2: Improve power distribution efficiency =====
    if context.pue > 1.5:
        recommendations.append(
            Recommendation(
                id="PWR-002",
                title="Optimize Power Distribution",
                description=(
                    "Audit UPS, PDU, and power distribution losses. "
                    "Upgrade to high-efficiency components where beneficial."
                ),
                category=Category.POWER.value,
                estimated_saving_pct=3.0,
                difficulty=DifficultyLevel.MEDIUM,
                impact_level=ImpactLevel.MEDIUM,
                prerequisites=[
                    "Access to power monitoring data",
                    "Budget for equipment upgrades"
                ],
                steps=[
                    "Measure UPS efficiency at current load",
                    "Audit PDU and distribution losses",
                    "Identify oversized or inefficient equipment",
                    "Plan targeted upgrades",
                    "Consider modular UPS for better load matching"
                ],
                logic_explanation=(
                    "Power distribution losses typically account for 5-8% of total energy. "
                    "Optimizing can recover 2-4% of total facility energy."
                ),
                references=[
                    "UPS Efficiency Regulations (EU/US)",
                    "The Green Grid - Power Chain Efficiency"
                ],
                implementation_time_months=6,
                roi_months=24
            )
        )
    
    # ===== RULE 3: Renewable energy procurement =====
    if context.carbon_factor_kg_per_kwh > 0.2:  # High carbon grid
        current_co2 = context.co2_tonnes_per_year
        renewable_savings = current_co2 * 0.5  # Assume 50% renewable
        
        recommendations.append(
            Recommendation(
                id="PWR-003",
                title="Procure Renewable Energy",
                description=(
                    f"Your grid carbon factor is {context.carbon_factor_kg_per_kwh:.3f} kgCO2/kWh. "
                    "Switching to renewable energy could reduce emissions significantly."
                ),
                category=Category.POWER.value,
                estimated_saving_pct=0.0,  # Energy use unchanged, CO2 improves
                difficulty=DifficultyLevel.MEDIUM,
                impact_level=ImpactLevel.HIGH,
                prerequisites=[
                    "Renewable energy available in market",
                    "PPA or green tariff options",
                    "Sustainability budget"
                ],
                steps=[
                    "Research renewable energy options (PPAs, green tariffs, RECs)",
                    "Calculate cost vs. carbon reduction",
                    "Present business case to leadership",
                    "Execute procurement agreement",
                    "Report on carbon reduction"
                ],
                logic_explanation=(
                    f"Switching to 50% renewable energy could reduce your carbon footprint "
                    f"by {renewable_savings:.0f} tons CO2/year without changing energy use."
                ),
                references=[
                    "RE100 - Renewable Energy Procurement Guide",
                    "Google's 100% renewable energy case study"
                ],
                implementation_time_months=6,
                roi_months=None  # May increase cost
            )
        )
    
    return recommendations