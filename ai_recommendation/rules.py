from dataclasses import dataclass
from typing import List


@dataclass
class Recommendation:
    title: str
    reason: str
    estimated_saving_pct: float


def build_recommendations(
    cpu_utilization_pct: float,
    cooling_setpoint_c: float,
    has_aisle_containment: bool,
    virtualization_level_pct: float,
) -> List[Recommendation]:
    recommendations: List[Recommendation] = []

    if cpu_utilization_pct < 30:
        recommendations.append(
            Recommendation(
                title="Server consolidation",
                reason=(
                    "Low CPU utilization. Consolidation reduces the server fleet and"
                    " avoids idle energy losses."
                ),
                estimated_saving_pct=8.0,
            )
        )

    if cooling_setpoint_c < 22:
        recommendations.append(
            Recommendation(
                title="Optimize cooling setpoint",
                reason=(
                    "Current temperature is low. Raising the setpoint can reduce"
                    " cooling consumption."
                ),
                estimated_saving_pct=6.0,
            )
        )

    if not has_aisle_containment:
        recommendations.append(
            Recommendation(
                title="Add hot/cold aisle containment",
                reason=(
                    "Lack of containment increases losses. Aisle containment improves"
                    " cooling efficiency."
                ),
                estimated_saving_pct=5.0,
            )
        )

    if virtualization_level_pct < 60:
        recommendations.append(
            Recommendation(
                title="Increase virtualization",
                reason=(
                    "Low virtualization level. More logical consolidation reduces"
                    " the number of physical servers."
                ),
                estimated_saving_pct=7.0,
            )
        )

    if not recommendations:
        recommendations.append(
            Recommendation(
                title="Maintain best practices",
                reason="Indicators look optimized. Keep continuous monitoring.",
                estimated_saving_pct=0.0,
            )
        )

    return recommendations
