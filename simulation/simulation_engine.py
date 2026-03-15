import json
from .config import (
    SERVER_CONSOLIDATION_PCT,
    VIRTUALIZATION_PCT,
    COOLING_OPTIMIZATION_PUE,
    TARGET_CO2_REDUCTION_PCT,
)


def load_baseline_data(file_path="data/baseline_metrics.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def calculate_co2(total_energy_mwh, carbon_factor):
    return total_energy_mwh * carbon_factor
def simulate_single_action(baseline_data, action_name, saving_pct=0, new_pue=None):
    baseline_it_energy = baseline_data["it_energy_mwh"]
    baseline_total_energy = baseline_data["total_energy_mwh"]
    baseline_co2 = baseline_data["co2_tonnes_per_year"]
    carbon_factor = baseline_data["carbon_factor"]
    baseline_pue = baseline_data["pue"]

    new_it_energy = baseline_it_energy * (1 - saving_pct / 100)
    final_pue = new_pue if new_pue is not None else baseline_pue

    new_total_energy = new_it_energy * final_pue
    new_co2 = calculate_co2(new_total_energy, carbon_factor)

    energy_saved = baseline_total_energy - new_total_energy
    co2_saved = baseline_co2 - new_co2

    return {
        "action_name": action_name,
        "baseline_energy_mwh": baseline_total_energy,
        "optimized_energy_mwh": round(new_total_energy, 3),
        "energy_saved_mwh": round(energy_saved, 3),
        "baseline_co2_tonnes": baseline_co2,
        "optimized_co2_tonnes": round(new_co2, 3),
        "co2_saved_tonnes": round(co2_saved, 3),
    }
def simulate_combined_actions(baseline_data):
    baseline_it_energy = baseline_data["it_energy_mwh"]
    baseline_total_energy = baseline_data["total_energy_mwh"]
    baseline_co2 = baseline_data["co2_tonnes_per_year"]
    carbon_factor = baseline_data["carbon_factor"]

    it_after_consolidation = baseline_it_energy * (1 - SERVER_CONSOLIDATION_PCT / 100)
    it_after_virtualization = it_after_consolidation * (1 - VIRTUALIZATION_PCT / 100)

    final_total_energy = it_after_virtualization * COOLING_OPTIMIZATION_PUE
    final_co2 = calculate_co2(final_total_energy, carbon_factor)

    energy_saved = baseline_total_energy - final_total_energy
    co2_saved = baseline_co2 - final_co2
    reduction_percent = (co2_saved / baseline_co2) * 100 if baseline_co2 else 0

    return {
        "baseline_energy_mwh": baseline_total_energy,
        "optimized_energy_mwh": round(final_total_energy, 3),
        "energy_saved_mwh": round(energy_saved, 3),
        "baseline_co2_tonnes": baseline_co2,
        "optimized_co2_tonnes": round(final_co2, 3),
        "co2_saved_tonnes": round(co2_saved, 3),
        "reduction_percent": round(reduction_percent, 2),
        "target_achieved": reduction_percent >= TARGET_CO2_REDUCTION_PCT,
    }
def run_simulation():
    baseline_data = load_baseline_data()

    single_actions = [
        simulate_single_action(
            baseline_data,
            action_name="Server Consolidation",
            saving_pct=SERVER_CONSOLIDATION_PCT,
        ),
        simulate_single_action(
            baseline_data,
            action_name="Virtualization",
            saving_pct=VIRTUALIZATION_PCT,
        ),
        simulate_single_action(
            baseline_data,
            action_name="Cooling Optimization",
            saving_pct=0,
            new_pue=COOLING_OPTIMIZATION_PUE,
        ),
    ]

    combined = simulate_combined_actions(baseline_data)

    return {
        "baseline": baseline_data,
        "single_actions": single_actions,
        "combined": combined,
    }