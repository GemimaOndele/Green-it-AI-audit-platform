"""
Cooling system recommendations.
Based on ASHRAE guidelines and Google case study benchmarks.
"""

from typing import List
from ..models import (
    AuditContext, Recommendation, 
    DifficultyLevel, ImpactLevel, Category
)


def get_cooling_recommendations(context: AuditContext) -> List[Recommendation]:
    """
    Generate cooling-related recommendations.
    
    Rule thresholds validated by Mike-Brady's test cases (TD-01 to TD-06)
    and aligned with Google case study benchmarks.
    """
    recommendations = []
    
    # ===== RULE 1: Raise cooling setpoint =====
    # Based on ASHRAE guidelines: 24-27°C recommended range
    # Google operates at 27°C in some facilities
    if context.cooling_setpoint_c < 24 and context.cooling_type in ["air", "hybrid"]:
        # Calculate savings: 4% per degree up to 27°C, max 12%
        degrees_to_raise = min(27 - context.cooling_setpoint_c, 3)  # Max 3°C increase
        savings_pct = min(4 * degrees_to_raise, 12)  # 4% per degree, max 12%
        
        target_temp = min(context.cooling_setpoint_c + degrees_to_raise, 27)
        
        recommendations.append(
            Recommendation(
                id="COOL-001",
                title="Increase Cooling Setpoint",
                description=(
                    f"Raise temperature from {context.cooling_setpoint_c:.0f}°C to "
                    f"{target_temp:.0f}°C (ASHRAE recommended range: 24-27°C). "
                    f"This could reduce cooling energy by {savings_pct:.0f}%."
                ),
                category=Category.COOLING.value,
                estimated_saving_pct=savings_pct,
                difficulty=DifficultyLevel.EASY,
                impact_level=ImpactLevel.MEDIUM if savings_pct > 8 else ImpactLevel.LOW,
                prerequisites=[
                    "Adjustable cooling system",
                    "Temperature monitoring in place",
                    "No equipment near thermal limits"
                ],
                steps=[
                    f"Increase setpoint by 1°C per week from {context.cooling_setpoint_c:.0f}°C",
                    "Monitor hot spots and server inlet temperatures after each change",
                    f"Target {target_temp:.0f}°C if equipment allows",
                    "Document temperature changes and energy savings"
                ],
                logic_explanation=(
                    f"ASHRAE TC 9.9 allows up to 27°C for most equipment classes (A1-A4). "
                    f"Each 1°C increase reduces cooling energy by 3-5%. "
                    f"Google operates at 27°C in some facilities, achieving PUE 1.1."
                ),
                references=[
                    "ASHRAE TC 9.9 Thermal Guidelines (2021)",
                    "Google Environmental Report 2024",
                    "TD-01, TD-02 (Mike-Brady's validation)"
                ],
                implementation_time_months=1,
                roi_months=0  # Immediate
            )
        )
    
    # ===== RULE 2: Implement aisle containment =====
    if not context.has_aisle_containment and context.pue > 1.5:
        recommendations.append(
            Recommendation(
                id="COOL-002",
                title="Implement Hot/Cold Aisle Containment",
                description=(
                    "Install physical barriers to separate hot and cold air streams, "
                    "preventing mixing and improving cooling efficiency by 15-30%."
                ),
                category=Category.COOLING.value,
                estimated_saving_pct=8.0,  # Conservative estimate
                difficulty=DifficultyLevel.MEDIUM,
                impact_level=ImpactLevel.HIGH,
                prerequisites=[
                    "Server airflow is front-to-back",
                    "Sufficient ceiling height or raised floor",
                    "Cable management in place"
                ],
                steps=[
                    "Audit current airflow patterns and identify bypass paths",
                    "Design containment solution (chimneys, curtains, or hard panels)",
                    "Install physical barriers in pilot row first",
                    "Seal all cable openings and bypass airflow paths",
                    "Verify temperature separation with thermal imaging",
                    "Roll out to remaining rows"
                ],
                logic_explanation=(
                    "Aisle containment prevents mixing of hot and cold air, "
                    "allowing higher return temperatures and reducing fan speeds. "
                    "Can improve cooling efficiency by 15-30% and reduce PUE by 0.1-0.3. "
                    f"Your current PUE of {context.pue:.2f} indicates significant mixing losses."
                ),
                references=[
                    "The Green Grid - Containment Best Practices",
                    "Google's data center efficiency white papers",
                    "TD-05, TD-06 (Google case study)"
                ],
                implementation_time_months=2,
                roi_months=12
            )
        )
    
    # ===== RULE 3: Upgrade to efficient cooling =====
    if context.pue > 1.6 and context.cooling_type == "air":
        recommendations.append(
            Recommendation(
                id="COOL-003",
                title="Upgrade to Efficient Cooling System",
                description=(
                    "Consider evaporative cooling, water-side economizers, or hybrid cooling "
                    "to reduce mechanical cooling energy. Google's water-based cooling "
                    "achieves PUE 1.1."
                ),
                category=Category.COOLING.value,
                estimated_saving_pct=15.0,
                difficulty=DifficultyLevel.HARD,
                impact_level=ImpactLevel.HIGH,
                prerequisites=[
                    "Facility has access to water",
                    "Climate suitable for economizers",
                    "Capital budget available",
                    "Space for additional equipment"
                ],
                steps=[
                    "Evaluate free cooling hours in your climate",
                    "Study Google's water-based cooling approach",
                    "Conduct feasibility study and ROI analysis",
                    "Design upgrade with qualified engineers",
                    "Implement in phases to minimize downtime",
                    "Validate performance with before/after PUE measurement"
                ],
                logic_explanation=(
                    f"Your current PUE of {context.pue:.2f} is significantly above "
                    f"Google's {RecommendationEngine.GOOGLE_PUE:.1f}. Air-cooled facilities "
                    "typically achieve PUE 1.4-1.6 at best. Water/hybrid cooling can reach 1.1-1.2. "
                    "The 15% energy reduction estimate is conservative for this upgrade."
                ),
                references=[
                    "Google Environmental Report 2024",
                    "EU Code of Conduct for Data Centres",
                    "ASHRAE - Liquid Cooling Guidelines"
                ],
                implementation_time_months=12,
                roi_months=24
            )
        )
    
    # ===== RULE 4: Free cooling optimization =====
    if context.cooling_type == "air" and context.pue > 1.4:
        recommendations.append(
            Recommendation(
                id="COOL-004",
                title="Optimize Free Cooling Hours",
                description=(
                    "Increase use of outside air when conditions permit, "
                    "reducing mechanical cooling requirements."
                ),
                category=Category.COOLING.value,
                estimated_saving_pct=5.0,
                difficulty=DifficultyLevel.MEDIUM,
                impact_level=ImpactLevel.MEDIUM,
                prerequisites=[
                    "Air-side or water-side economizers installed",
                    "Climate with sufficient cool hours",
                    "Controls capable of automated switching"
                ],
                steps=[
                    "Analyze local climate data for free cooling hours",
                    "Adjust control algorithms to maximize economizer use",
                    "Implement temperature/humidity deadbands",
                    "Monitor compressor run hours reduction"
                ],
                logic_explanation=(
                    "Many data centers underutilize free cooling. Increasing economizer hours "
                    "by 20% can reduce cooling energy by 5-10% with minimal investment."
                ),
                references=[
                    "The Green Grid - Economizer Best Practices",
                    "ASHRAE - Free Cooling Guidelines"
                ],
                implementation_time_months=3,
                roi_months=6
            )
        )
    
    return recommendations