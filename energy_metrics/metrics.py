def calculate_pue(it_energy_mwh: float, total_energy_mwh: float) -> float:
    if it_energy_mwh <= 0:
        return 0.0
    return total_energy_mwh / it_energy_mwh


def calculate_dcie(it_energy_mwh: float, total_energy_mwh: float) -> float:
    if total_energy_mwh <= 0:
        return 0.0
    return (it_energy_mwh / total_energy_mwh) * 100.0


def calculate_co2_tonnes(
    total_energy_mwh: float, carbon_factor_kg_per_kwh: float
) -> float:
    # MWh -> kWh, then kg CO2, then tonnes.
    total_kwh = total_energy_mwh * 1000.0
    kg_co2 = total_kwh * carbon_factor_kg_per_kwh
    return kg_co2 / 1000.0
