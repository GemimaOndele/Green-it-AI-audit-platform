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
    .stApp {
        background: radial-gradient(140% 140% at 0% 0%, #0f1d3b 0%, #0a1022 55%, #060914 100%);
    }
    .hero {
        background: linear-gradient(145deg, rgba(28,45,94,0.9), rgba(10,16,34,0.95));
        color: #f7f7f7;
        padding: 28px 32px;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.35);
        border: 1px solid rgba(255,255,255,0.12);
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }
    .hero h1 { margin: 0 0 6px 0; font-size: 32px; }
    .hero p { margin: 0; opacity: 0.9; }
    .hero::after {
        content: "";
        position: absolute;
        right: -80px;
        top: -80px;
        width: 220px;
        height: 220px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(110,140,255,0.35), rgba(110,140,255,0.0) 60%);
        filter: blur(2px);
    }
    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        background: rgba(140, 170, 255, 0.14);
        border: 1px solid rgba(140, 170, 255, 0.35);
        color: #cfd8ff;
        font-size: 12px;
        letter-spacing: 0.04em;
        margin-right: 8px;
    }
    .glass {
        background: rgba(18, 26, 51, 0.55);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow: 0 12px 24px rgba(0,0,0,0.25);
        border-radius: 16px;
        padding: 16px 18px;
    }
    .metric-card {
        background: linear-gradient(180deg, rgba(22,32,66,0.92) 0%, rgba(10,16,34,0.95) 100%);
        color: #eef1ff;
        padding: 16px 18px;
        border-radius: 14px;
        box-shadow: 0 10px 24px rgba(0,0,0,0.35);
        border: 1px solid rgba(255,255,255,0.12);
    }
    .metric-card h3 { margin: 0 0 6px 0; font-size: 12px; text-transform: uppercase; letter-spacing: 0.1em; color: #9fb2ff; }
    .metric-card .value { font-size: 26px; font-weight: 700; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>GreenDC Audit Platform</h1>
        <p>AI-assisted energy & carbon audit for industrial data centers — modern, 3D-inspired, and Green IT compliant.</p>
        <div style="margin-top: 12px;">
            <span class="badge">Green IT</span>
            <span class="badge">Green Coding</span>
            <span class="badge">ISO 50001 Ready</span>
            <span class="badge">-25% CO2 Target</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

dashboard_tab, about_tab = st.tabs(["Dashboard", "About"])

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

with dashboard_tab:
    metrics_col, recs_col = st.columns([1, 1])

    with metrics_col:
        st.subheader("Key Metrics")
        pue = calculate_pue(it_energy_mwh, total_energy_mwh)
        dcie = calculate_dcie(it_energy_mwh, total_energy_mwh)
        co2_tonnes = calculate_co2_tonnes(total_energy_mwh, carbon_factor)

        metric_cols = st.columns(3)
        with metric_cols[0]:
            st.markdown(
                f"<div class='metric-card'><h3>⚡ PUE</h3><div class='value'>{pue:.2f}</div></div>",
                unsafe_allow_html=True,
            )
        with metric_cols[1]:
            st.markdown(
                f"<div class='metric-card'><h3>📈 DCiE</h3><div class='value'>{dcie:.1f}%</div></div>",
                unsafe_allow_html=True,
            )
        with metric_cols[2]:
            st.markdown(
                f"<div class='metric-card'><h3>🌍 CO2</h3><div class='value'>{co2_tonnes:.1f} t/y</div></div>",
                unsafe_allow_html=True,
            )

        st.markdown(
            f"<div class='glass'>Servers: <b>{servers}</b> | CPU Utilization: <b>{cpu_utilization:.1f}%</b>"
            f" | Cooling Setpoint: <b>{cooling_setpoint:.1f} °C</b></div>",
            unsafe_allow_html=True,
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

    st.markdown(
        f"<div class='glass'>Estimated total savings: <b>{simulation['total_savings_mwh']:.1f} MWh/year</b>"
        f" ({simulation['total_savings_pct']:.1f}%)</div>",
        unsafe_allow_html=True,
    )
    if simulation["total_savings_pct"] >= 25:
        st.success("Target -25% CO2 is achievable with these actions.")
    else:
        st.info("Target -25% CO2 not reached. Adjust the action set.")

with about_tab:
    st.subheader("About the Platform")
    st.markdown(
        """
        <div class="glass">
            <b>Mission:</b> Provide an audit-ready, measurable path to cut data center CO2 by 25%.
            <br><br>
            <b>Principles:</b> Digital sobriety, proportional computing, and continuous measurement.
            <br><br>
            <b>Scope:</b> PUE, DCiE, CO2, recommendations, and scenario validation.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("")
    st.markdown(
        """
        <div class="glass">
            <b>How to use:</b>
            <ol>
                <li>Enter data center inputs in the sidebar.</li>
                <li>Review metrics and AI recommendations.</li>
                <li>Validate the -25% target with the simulation panel.</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )
