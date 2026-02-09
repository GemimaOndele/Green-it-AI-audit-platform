from typing import List, Dict


def simulate_actions(
    total_energy_mwh: float, actions: List[Dict[str, float]]
) -> Dict[str, float]:
    remaining_energy = total_energy_mwh
    total_savings_mwh = 0.0

    for action in actions:
        saving_pct = action["estimated_saving_pct"]
        saved = remaining_energy * (saving_pct / 100.0)
        remaining_energy -= saved
        total_savings_mwh += saved

    return {
        "initial_energy_mwh": total_energy_mwh,
        "remaining_energy_mwh": remaining_energy,
        "total_savings_mwh": total_savings_mwh,
        "total_savings_pct": (total_savings_mwh / total_energy_mwh * 100.0)
        if total_energy_mwh > 0
        else 0.0,
    }
