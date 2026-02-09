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
                title="Consolidation des serveurs",
                reason=(
                    "Faible taux d'utilisation CPU. Consolider permet de reduire le parc"
                    " et les pertes d'energie."
                ),
                estimated_saving_pct=8.0,
            )
        )

    if cooling_setpoint_c < 22:
        recommendations.append(
            Recommendation(
                title="Optimisation du point de consigne de refroidissement",
                reason=(
                    "La temperature est basse. Un setpoint plus eleve peut reduire la"
                    " consommation de refroidissement."
                ),
                estimated_saving_pct=6.0,
            )
        )

    if not has_aisle_containment:
        recommendations.append(
            Recommendation(
                title="Mise en place d'allee chaude/froide",
                reason=(
                    "L'absence de confinement augmente les pertes. L'ajout d'allee"
                    " chaude/froide ameliore l'efficacite du refroidissement."
                ),
                estimated_saving_pct=5.0,
            )
        )

    if virtualization_level_pct < 60:
        recommendations.append(
            Recommendation(
                title="Renforcer la virtualisation",
                reason=(
                    "Niveau de virtualisation faible. Plus de consolidation logique"
                    " reduit le nombre de serveurs physiques."
                ),
                estimated_saving_pct=7.0,
            )
        )

    if not recommendations:
        recommendations.append(
            Recommendation(
                title="Maintenir les bonnes pratiques",
                reason="Les indicateurs sont deja optimises. Continuer le suivi.",
                estimated_saving_pct=0.0,
            )
        )

    return recommendations
