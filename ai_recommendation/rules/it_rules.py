"""
IT equipment and virtualization recommendations.
Based on industry best practices and Google case study benchmarks.
"""

from typing import List
from ..models import (
    AuditContext, Recommendation, 
    DifficultyLevel, ImpactLevel, Category
)


def get_it_recommendations(context: AuditContext) -> List[Recommendation]:
    """
    Generate IT equipment and virtualization recommendations.
    """
    recommendations = []
    
    # ===== RULE 1: Server consolidation (low utilization) =====
    # Google's avg CPU utilization is 55% (from google_case_study.csv)
    if context.cpu_utilization_pct < 30:
        # Calculate potential server reduction
        current_servers = context.num_servers
        target_utilization = 60  # Target 60% utilization
        target_servers = int(current_servers * (context.cpu_utilization_pct / target_utilization))
        servers_to_remove = current_servers - target_servers
        
        savings_pct = 8.0  # Base savings
        
        rec_description = (
            f"CPU utilization is only {context.cpu_utilization_pct:.0f}% "
            f"(Google benchmark: 55%). Consolidation could remove ~{servers_to_remove} "
            f"physical servers, saving energy and cooling."
        )
        
        recommendations.append(
            Recommendation(
                id="IT-001",
                title="Consolidate Underutilized Servers",
                description=rec_description,
                category=Category.IT.value,
                estimated_saving_pct=savings_pct,
                difficulty=DifficultyLevel.MEDIUM,
                impact_level=ImpactLevel.HIGH,
                prerequisites=[
                    "Virtualization platform in place (VMware, Hyper-V, KVM)",
                    "Workload compatibility analysis needed",
                    "Storage capacity for consolidated workloads",
                    "Network bandwidth assessment"
                ],
                steps=[
                    f"Identify servers with <20% CPU utilization (target: {servers_to_remove} servers)",
                    "Analyze workload patterns and dependencies",
                    "Plan migration schedule with minimal disruption",
                    "Migrate workloads to remaining servers",
                    "Decommission empty servers (power off, remove)",
                    "Update power management settings on remaining servers",
                    "Validate performance post-consolidation"
                ],
                logic_explanation=(
                    f"At {context.cpu_utilization_pct:.0f}% utilization, you're wasting "
                    f"energy on idle servers. Google targets 55% utilization. "
                    f"Consolidating {servers_to_remove} servers could reduce IT energy by "
                    f"{savings_pct:.0f}% and cooling load proportionally."
                ),
                references=[
                    "VMware TCO/ROI Studies",
                    "The Green Grid - Server Efficiency",
                    "Google Environmental Report 2024 (55% utilization benchmark)"
                ],
                implementation_time_months=4,
                roi_months=15
            )
        )
    
    # ===== RULE 2: Increase virtualization ratio =====
    if context.virtualization_level_pct < 60:
        savings_pct = 7.0
        
        recommendations.append(
            Recommendation(
                id="IT-002",
                title="Increase Virtualization Ratio",
                description=(
                    f"Current virtualization: {context.virtualization_level_pct:.0f}%. "
                    f"Target 80%+ to reduce physical footprint by up to 50%."
                ),
                category=Category.IT.value,
                estimated_saving_pct=savings_pct,
                difficulty=DifficultyLevel.MEDIUM,
                impact_level=ImpactLevel.HIGH,
                prerequisites=[
                    "Compatible applications (no physical dependencies)",
                    "Sufficient storage capacity",
                    "Network bandwidth for migration",
                    "Virtualization platform licenses"
                ],
                steps=[
                    "Audit all workloads for virtualization potential",
                    "Identify physical servers with <50% utilization",
                    "Prioritize workloads by ease of migration",
                    "Plan migration schedule in waves",
                    "Execute migrations during maintenance windows",
                    "Monitor performance post-migration",
                    "Decommission original physical servers"
                ],
                logic_explanation=(
                    "Virtualization allows multiple workloads on one physical server, "
                    "reducing energy, cooling, and space requirements. Each 10% increase "
                    "in virtualization ratio typically reduces energy by 3-5%."
                ),
                references=[
                    "VMware - The Economics of Server Virtualization",
                    "Green IT Best Practices - Server Consolidation"
                ],
                implementation_time_months=3,
                roi_months=12
            )
        )
    
    # ===== RULE 3: Upgrade to efficient servers =====
    if context.avg_server_age_years and context.avg_server_age_years > 4:
        recommendations.append(
            Recommendation(
                id="IT-003",
                title="Upgrade to Energy-Efficient Servers",
                description=(
                    f"Average server age is {context.avg_server_age_years:.0f} years. "
                    "Newer servers offer 2-3x better performance per watt."
                ),
                category=Category.IT.value,
                estimated_saving_pct=12.0,
                difficulty=DifficultyLevel.HARD,
                impact_level=ImpactLevel.HIGH,
                prerequisites=[
                    "Capital budget for hardware refresh",
                    "Application compatibility with new hardware",
                    "Migration plan"
                ],
                steps=[
                    "Audit current server inventory and age",
                    "Identify refresh candidates (oldest, least efficient)",
                    "Benchmark current vs. new server efficiency",
                    "Phase refresh over 12-24 months",
                    "Decommission old servers promptly"
                ],
                logic_explanation=(
                    "Server efficiency doubles every 3-4 years. Replacing 5+ year old "
                    "servers can reduce IT energy by 30-50% for the same workload."
                ),
                references=[
                    "SPECpower Benchmark Results",
                    "The Green Grid - Server Efficiency Metrics"
                ],
                implementation_time_months=12,
                roi_months=24
            )
        )
    
    # ===== RULE 4: Implement power management =====
    if context.cpu_utilization_pct < 40:
        recommendations.append(
            Recommendation(
                id="IT-004",
                title="Enable Advanced Power Management",
                description=(
                    "Configure power management features (C-states, P-states) "
                    "to reduce idle power consumption."
                ),
                category=Category.IT.value,
                estimated_saving_pct=4.0,
                difficulty=DifficultyLevel.EASY,
                impact_level=ImpactLevel.MEDIUM,
                prerequisites=[
                    "BIOS/firmware supports power management",
                    "OS/driver compatibility",
                    "Performance requirements allow power saving"
                ],
                steps=[
                    "Audit current power management settings",
                    "Enable C-states and P-states in BIOS",
                    "Configure OS power policies",
                    "Monitor for performance impact",
                    "Adjust as needed"
                ],
                logic_explanation=(
                    "Modern servers can reduce idle power by 30-50% with proper power "
                    "management. At low utilization, this significantly improves efficiency."
                ),
                references=[
                    "SPEC - Server Power Management Guidelines",
                    "Intel - Power Management Features"
                ],
                implementation_time_months=1,
                roi_months=3
            )
        )
    
    return recommendations