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

st.markdown(
    """
    <style>
    .hero {
        background: radial-gradient(120% 120% at 10% 10%, #1f3b73 0%, #0b1226 45%, #060914 100%);
        color: #f7f7f7;
        padding: 28px 32px;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.35);
        border: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 20px;
    }
    .hero h1 { margin: 0 0 6px 0; font-size: 32px; }
    .hero p { margin: 0; opacity: 0.9; }
    .card {
        background: linear-gradient(180deg, #121a33 0%, #0c1224 100%);
        color: #eef1ff;
        padding: 16px 18px;
        border-radius: 14px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.25);
        border: 1px solid rgba(255,255,255,0.06);
    }
    .card h3 { margin: 0 0 6px 0; font-size: 14px; text-transform: uppercase; letter-spacing: 0.08em; color: #9fb2ff; }
    .card .value { font-size: 26px; font-weight: 700; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>GreenDC Audit Platform</h1>
        <p>AI-assisted energy & carbon audit for industrial data centers — modern, 3D-inspired, and Green IT compliant.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Data Center Inputs")
    it_energy_mwh = st.number_input(
        "IT Energy (MWh/year)", min_value=0.0, value=780.0, step=10.0
    )
    total_energy_mwh = st.number_input(
        "Total Energy (MWh/year)", min_value=0.0, value=1300.0, step=10.0
    )
    carbon_factor = st.number_input(
        "Carbon Factor (kg CO2/kWh)", min_value=0.0, value=0.30, step=0.01
    )
    servers = st.number_input("Number of Servers", min_value=0, value=320, step=10)
    cpu_utilization = st.number_input(
        "Average CPU Utilization (%)", min_value=0.0, max_value=100.0, value=18.0
    )
    cooling_setpoint = st.number_input(
        "Cooling Setpoint (°C)", min_value=10.0, max_value=30.0, value=19.0
    )
    aisle_containment = st.checkbox("Hot/Cold Aisle Containment in place", value=False)
    virtualization_level = st.number_input(
        "Virtualization Level (%)", min_value=0.0, max_value=100.0, value=45.0
    )

metrics_col, recs_col = st.columns([1, 1])

with metrics_col:
    st.subheader("Key Metrics")
    pue = calculate_pue(it_energy_mwh, total_energy_mwh)
    dcie = calculate_dcie(it_energy_mwh, total_energy_mwh)
    co2_tonnes = calculate_co2_tonnes(total_energy_mwh, carbon_factor)

    metric_cols = st.columns(3)
    with metric_cols[0]:
        st.markdown(
            f"<div class='card'><h3>PUE</h3><div class='value'>{pue:.2f}</div></div>",
            unsafe_allow_html=True,
        )
    with metric_cols[1]:
        st.markdown(
            f"<div class='card'><h3>DCiE</h3><div class='value'>{dcie:.1f}%</div></div>",
            unsafe_allow_html=True,
        )
    with metric_cols[2]:
        st.markdown(
            f"<div class='card'><h3>CO2</h3><div class='value'>{co2_tonnes:.1f} t/y</div></div>",
            unsafe_allow_html=True,
        )

    st.write(
        f"Servers: {servers} | CPU Utilization: {cpu_utilization:.1f}%"
        f" | Cooling Setpoint: {cooling_setpoint:.1f} °C"
    )

with recs_col:
    st.subheader("AI Recommendations")
    recommendations = build_recommendations(
        cpu_utilization_pct=cpu_utilization,
        cooling_setpoint_c=cooling_setpoint,
        has_aisle_containment=aisle_containment,
        virtualization_level_pct=virtualization_level,
    )
    recs_data = [
        {
            "Action": r.title,
            "Why it helps": r.reason,
            "Estimated Saving (%)": r.estimated_saving_pct,
        }
        for r in recommendations
    ]
    st.dataframe(pd.DataFrame(recs_data), use_container_width=True)

st.subheader("Before / After Simulation")
actions = [{"estimated_saving_pct": r.estimated_saving_pct} for r in recommendations]
simulation = simulate_actions(total_energy_mwh, actions)

sim_df = pd.DataFrame(
    [
        {"Scenario": "Baseline", "Energy (MWh/year)": simulation["initial_energy_mwh"]},
        {
            "Scenario": "After Actions",
            "Energy (MWh/year)": simulation["remaining_energy_mwh"],
        },
    ]
)
st.bar_chart(sim_df.set_index("Scenario"))

st.write(
    f"Estimated total savings: {simulation['total_savings_mwh']:.1f} MWh/year"
    f" ({simulation['total_savings_pct']:.1f}%)"
)
if simulation["total_savings_pct"] >= 25:
    st.success("Target -25% CO2 is achievable with these actions.")
else:
    st.info("Target -25% CO2 not reached. Adjust the action set.")
