import os
import sys

import pandas as pd
import streamlit as st

# Ensure project root is on PYTHONPATH when running via Streamlit.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from ai_recommendation import build_recommendations
from energy_metrics import calculate_co2_tonnes, calculate_dcie, calculate_pue
from simulation import simulate_actions


st.set_page_config(page_title="GreenDC Audit Platform", layout="wide")

st.title("GreenDC Audit Platform")
st.caption("Audit energetique et carbone des data centers industriels")

with st.sidebar:
    st.header("Parametres du data center")
    it_energy_mwh = st.number_input(
        "Energie IT (MWh/an)", min_value=0.0, value=780.0, step=10.0
    )
    total_energy_mwh = st.number_input(
        "Energie totale (MWh/an)", min_value=0.0, value=1300.0, step=10.0
    )
    carbon_factor = st.number_input(
        "Facteur carbone (kg CO2/kWh)", min_value=0.0, value=0.30, step=0.01
    )
    servers = st.number_input("Nombre de serveurs", min_value=0, value=320, step=10)
    cpu_utilization = st.number_input(
        "Utilisation CPU moyenne (%)", min_value=0.0, max_value=100.0, value=18.0
    )
    cooling_setpoint = st.number_input(
        "Consigne de refroidissement (°C)", min_value=10.0, max_value=30.0, value=19.0
    )
    aisle_containment = st.checkbox("Allee chaude/froide en place", value=False)
    virtualization_level = st.number_input(
        "Niveau de virtualisation (%)", min_value=0.0, max_value=100.0, value=45.0
    )

metrics_col, recs_col = st.columns([1, 1])

with metrics_col:
    st.subheader("Indicateurs")
    pue = calculate_pue(it_energy_mwh, total_energy_mwh)
    dcie = calculate_dcie(it_energy_mwh, total_energy_mwh)
    co2_tonnes = calculate_co2_tonnes(total_energy_mwh, carbon_factor)

    st.metric("PUE", f"{pue:.2f}")
    st.metric("DCiE", f"{dcie:.1f} %")
    st.metric("Emissions CO2", f"{co2_tonnes:.1f} tCO2/an")

    st.write(
        f"Serveurs: {servers} | Utilisation CPU: {cpu_utilization:.1f}%"
        f" | Consigne: {cooling_setpoint:.1f} °C"
    )

with recs_col:
    st.subheader("Recommandations")
    recommendations = build_recommendations(
        cpu_utilization_pct=cpu_utilization,
        cooling_setpoint_c=cooling_setpoint,
        has_aisle_containment=aisle_containment,
        virtualization_level_pct=virtualization_level,
    )
    recs_data = [
        {
            "Action": r.title,
            "Justification": r.reason,
            "Gain estime (%)": r.estimated_saving_pct,
        }
        for r in recommendations
    ]
    st.dataframe(pd.DataFrame(recs_data), use_container_width=True)

st.subheader("Simulation avant / apres")
actions = [{"estimated_saving_pct": r.estimated_saving_pct} for r in recommendations]
simulation = simulate_actions(total_energy_mwh, actions)

sim_df = pd.DataFrame(
    [
        {"Scenario": "Initial", "Energie (MWh/an)": simulation["initial_energy_mwh"]},
        {
            "Scenario": "Apres actions",
            "Energie (MWh/an)": simulation["remaining_energy_mwh"],
        },
    ]
)
st.bar_chart(sim_df.set_index("Scenario"))

st.write(
    f"Gain total estime: {simulation['total_savings_mwh']:.1f} MWh/an"
    f" ({simulation['total_savings_pct']:.1f}%)"
)
if simulation["total_savings_pct"] >= 25:
    st.success("Objectif -25% CO2 atteignable avec ces actions.")
else:
    st.info("Objectif -25% CO2 non atteint, ajuster les actions.")
