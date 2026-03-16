
"""
energy_metrics/metrics.py
GreenDC Audit Platform — Energy & Carbon Metrics Module

Author : Mike-Brady Mbolim Mbock
Role   : Data Processing & Energy Metrics Engineer
Team   : GreenAI Systems

Formulas based on Green IT / ISO 50001 standards:
  - PUE  : Power Usage Effectiveness
  - DCiE : Data Center Infrastructure Efficiency
  - CO2  : Carbon emissions from energy consumption
  - Annual energy from IT load
"""

# ---------------------------------------------------------------------------
# 1. PUE — Power Usage Effectiveness
# ---------------------------------------------------------------------------
def calculate_pue(it_energy_mwh: float, total_energy_mwh: float) -> float:
    """
    PUE = Total Facility Energy / IT Equipment Energy
    Ideal value = 1.0  (all energy goes to IT)
    Typical range: 1.2 (excellent) to 2.5+ (poor)

    Args:
        it_energy_mwh    : Energy consumed by IT equipment (MWh/year)
        total_energy_mwh : Total facility energy consumption (MWh/year)

    Returns:
        PUE ratio (float), or 0.0 if inputs are invalid
    """
    if it_energy_mwh <= 0:
        return 0.0
    return round(total_energy_mwh / it_energy_mwh, 4)


# ---------------------------------------------------------------------------
# 2. DCiE — Data Center Infrastructure Efficiency
# ---------------------------------------------------------------------------
def calculate_dcie(it_energy_mwh: float, total_energy_mwh: float) -> float:
    """
    DCiE = (IT Energy / Total Energy) * 100
    DCiE = (1 / PUE) * 100
    Ideal value = 100%

    Args:
        it_energy_mwh    : Energy consumed by IT equipment (MWh/year)
        total_energy_mwh : Total facility energy consumption (MWh/year)

    Returns:
        DCiE percentage (float), or 0.0 if inputs are invalid
    """
    if total_energy_mwh <= 0:
        return 0.0
    return round((it_energy_mwh / total_energy_mwh) * 100.0, 4)


# ---------------------------------------------------------------------------
# 3. CO₂ Emissions
# ---------------------------------------------------------------------------
def calculate_co2_tonnes(
    total_energy_mwh: float, carbon_factor_kg_per_kwh: float
) -> float:
    """
    CO2 (tCO2/year) = Total Energy (MWh) * 1000 * Carbon Factor (kgCO2/kWh) / 1000
                    = Total Energy (MWh) * Carbon Factor (kgCO2/kWh)

    Args:
        total_energy_mwh        : Total energy consumption (MWh/year)
        carbon_factor_kg_per_kwh: Grid carbon intensity (kgCO2/kWh)
                                  e.g. France ~0.057, Germany ~0.400, World avg ~0.475

    Returns:
        CO2 emissions in metric tonnes per year
    """
    total_kwh = total_energy_mwh * 1000.0
    kg_co2 = total_kwh * carbon_factor_kg_per_kwh
    return round(kg_co2 / 1000.0, 4)


# ---------------------------------------------------------------------------
# 4. Annual Energy Consumption from IT Load
# ---------------------------------------------------------------------------
def calculate_annual_energy_mwh(it_power_kw: float) -> float:
    """
    Annual Energy (MWh/year) = IT Power (kW) * 8760 hours/year / 1000

    Assumes the data center runs 24/7/365 (8760 hours per year).

    Args:
        it_power_kw : Average IT equipment power draw (kW)

    Returns:
        Annual IT energy consumption in MWh/year
    """
    if it_power_kw <= 0:
        return 0.0
    hours_per_year = 8760
    return round((it_power_kw * hours_per_year) / 1000.0, 4)


# ---------------------------------------------------------------------------
# 5. PUE Performance Rating
# ---------------------------------------------------------------------------
def get_pue_rating(pue: float) -> dict:
    """
    Returns a human-readable performance rating for a given PUE value.
    Based on Green Grid / EU Code of Conduct thresholds.

    Thresholds:
        < 1.2  : Excellent  (world-class, e.g. Google/Meta hyperscalers)
        1.2–1.5: Good       (energy-efficient, modern DC)
        1.5–2.0: Average    (room for improvement)
        >= 2.0 : Poor       (urgent optimization needed)

    Args:
        pue : PUE value (float)

    Returns:
        dict with keys: rating (str), description (str), action_needed (bool)
    """
    if pue <= 0:
        return {"rating": "Invalid", "description": "PUE must be > 0", "action_needed": True}
    elif pue < 1.2:
        return {"rating": "Excellent", "description": "World-class efficiency", "action_needed": False}
    elif pue < 1.5:
        return {"rating": "Good", "description": "Energy-efficient data center", "action_needed": False}
    elif pue < 2.0:
        return {"rating": "Average", "description": "Moderate efficiency — optimization recommended", "action_needed": True}
    else:
        return {"rating": "Poor", "description": "High energy waste — urgent action required", "action_needed": True}


# ---------------------------------------------------------------------------
# 6. Master Summary Function (used by dashboard & simulation engine)
# ---------------------------------------------------------------------------
def calculate_all_metrics(
    it_power_kw: float,
    total_energy_mwh: float,
    carbon_factor_kg_per_kwh: float,
    it_energy_mwh: float = None
) -> dict:
    """
    Master function — computes all metrics in one call.
    Used by:
      - Gemima's Streamlit dashboard (frontend)
      - Nandaa's simulation engine (baseline state)
      - Joseph's AI recommendation engine (trigger conditions)

    Args:
        it_power_kw              : Average IT power draw (kW)
        total_energy_mwh         : Total facility energy (MWh/year)
        carbon_factor_kg_per_kwh : Grid carbon intensity (kgCO2/kWh)
        it_energy_mwh            : IT energy (MWh/year). If None, computed from it_power_kw.

    Returns:
        dict with all computed metrics
    """
    # Compute IT energy from power if not provided directly
    if it_energy_mwh is None:
        it_energy_mwh = calculate_annual_energy_mwh(it_power_kw)

    pue  = calculate_pue(it_energy_mwh, total_energy_mwh)
    dcie = calculate_dcie(it_energy_mwh, total_energy_mwh)
    co2  = calculate_co2_tonnes(total_energy_mwh, carbon_factor_kg_per_kwh)
    rating = get_pue_rating(pue)

    return {
        "it_power_kw"           : it_power_kw,
        "it_energy_mwh"         : it_energy_mwh,
        "total_energy_mwh"      : total_energy_mwh,
        "carbon_factor"         : carbon_factor_kg_per_kwh,
        "pue"                   : pue,
        "dcie_percent"          : dcie,
        "co2_tonnes_per_year"   : co2,
        "pue_rating"            : rating["rating"],
        "pue_description"       : rating["description"],
        "action_needed"         : rating["action_needed"]
    }
