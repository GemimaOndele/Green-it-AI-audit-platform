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
    h1, h2, h3, h4, h5, p, li, label, span, div {
        color: #e9edff;
    }
    a { color: #bcd0ff; }
    [data-testid="stMetricValue"] { color: #ffffff !important; text-shadow: 0 2px 6px rgba(0,0,0,0.45); }
    [data-testid="stMetricLabel"] { color: #c9d4ff !important; }
    .section-title {
        font-size: 18px;
        font-weight: 700;
        letter-spacing: 0.02em;
        margin: 6px 0 10px 0;
        color: #eaf0ff;
        text-shadow: 0 2px 6px rgba(0,0,0,0.4);
    }
    .topbar {
        position: sticky;
        top: 0;
        z-index: 999;
        background: rgba(10, 16, 34, 0.75);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 10px 14px;
        margin: 6px 0 16px 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.35);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
    }
    .nav a {
        text-decoration: none;
        margin-right: 12px;
        padding: 6px 10px;
        border-radius: 10px;
        background: rgba(20, 30, 60, 0.6);
        border: 1px solid rgba(255,255,255,0.08);
        color: #dbe6ff;
        font-size: 12px;
    }
    .nav a:hover {
        background: rgba(52, 75, 140, 0.7);
        color: #ffffff;
    }
    .subtle {
        opacity: 0.8;
        font-size: 13px;
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
        background: rgba(140, 170, 255, 0.2);
        border: 1px solid rgba(140, 170, 255, 0.35);
        color: #cfd8ff;
        font-size: 12px;
        letter-spacing: 0.04em;
        margin-right: 8px;
    }
    .badge-solid {
        background: rgba(76, 214, 180, 0.18);
        border: 1px solid rgba(76, 214, 180, 0.45);
        color: #c9fff2;
    }
    .glass {
        background: rgba(26, 36, 72, 0.65);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow: 0 12px 24px rgba(0,0,0,0.25);
        border-radius: 16px;
        padding: 16px 18px;
    }
    .metric-card {
        background: linear-gradient(180deg, rgba(32,48,96,0.98) 0%, rgba(16,24,48,0.98) 100%);
        color: #eef1ff;
        padding: 16px 18px;
        border-radius: 14px;
        box-shadow: 0 12px 28px rgba(0,0,0,0.45);
        border: 1px solid rgba(255,255,255,0.12);
    }
    .metric-card h3 { margin: 0 0 6px 0; font-size: 12px; text-transform: uppercase; letter-spacing: 0.1em; color: #c9d4ff; }
    .metric-card .value { font-size: 28px; font-weight: 800; color: #ffffff; text-shadow: 0 2px 6px rgba(0,0,0,0.5); }
    .stSidebar > div:first-child {
        background: linear-gradient(180deg, rgba(14,21,42,0.98), rgba(9,14,29,0.98));
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    .stSidebar label, .stSidebar span, .stSidebar p {
        color: #e9edff !important;
    }
    .sidebar-title {
        font-weight: 800;
        font-size: 14px;
        letter-spacing: 0.08em;
        margin-bottom: 8px;
        color: #cfe0ff;
    }
    .stSidebar [data-testid="stExpander"] {
        background: rgba(18, 26, 51, 0.6);
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.08);
        padding: 6px;
    }
    .stSidebar [data-testid="stExpander"] summary {
        color: #e9edff;
        font-weight: 600;
    }
    .stDataFrame, .stTable {
        background: rgba(20, 30, 60, 0.35);
        border-radius: 12px;
        padding: 6px;
    }
    .stDataFrame div[role="grid"] {
        background: rgba(16, 24, 48, 0.9);
        color: #e9edff;
    }
    .stDataFrame div[role="grid"] * {
        color: #e9edff !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #c9d4ff;
        background: rgba(20, 30, 60, 0.5);
        border-radius: 12px;
        margin-right: 6px;
        padding: 8px 14px;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .stTabs [aria-selected="true"] {
        background: rgba(52, 75, 140, 0.7);
        color: #ffffff;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 6px 16px rgba(0,0,0,0.35);
    }
    .footer {
        margin-top: 20px;
        padding: 12px 16px;
        border-radius: 12px;
        background: rgba(12, 18, 38, 0.7);
        border: 1px solid rgba(255,255,255,0.08);
        font-size: 12px;
        color: #b7c3ff;
    }
    .rec-card {
        background: linear-gradient(180deg, rgba(24, 36, 72, 0.95) 0%, rgba(12, 20, 40, 0.98) 100%);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 10px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.35);
    }
    .rec-title {
        font-weight: 700;
        font-size: 14px;
        margin-bottom: 6px;
        color: #f1f4ff;
    }
    .rec-meta {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 999px;
        background: rgba(120, 210, 255, 0.15);
        border: 1px solid rgba(120, 210, 255, 0.35);
        color: #d9f0ff;
        font-size: 11px;
        margin-top: 8px;
    }
    .svg-icon {
        vertical-align: middle;
        margin-right: 6px;
    }
    .action-icon {
        vertical-align: middle;
        margin-right: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("<div class='sidebar-title'>CONTROL PANEL</div>", unsafe_allow_html=True)
    page = st.radio("Navigation", ["Landing", "Dashboard", "About"])
    with st.expander("Energy Inputs", expanded=True):
        it_energy_mwh = st.number_input(
            "IT Energy (MWh/year)", min_value=0.0, value=780.0, step=10.0
        )
        total_energy_mwh = st.number_input(
            "Total Energy (MWh/year)", min_value=0.0, value=1300.0, step=10.0
        )
        carbon_factor = st.number_input(
            "Carbon Factor (kg CO2/kWh)", min_value=0.0, value=0.30, step=0.01
        )
    with st.expander("Infrastructure Inputs", expanded=True):
        servers = st.number_input("Number of Servers", min_value=0, value=320, step=10)
        cpu_utilization = st.number_input(
            "Average CPU Utilization (%)", min_value=0.0, max_value=100.0, value=18.0
        )
        virtualization_level = st.number_input(
            "Virtualization Level (%)", min_value=0.0, max_value=100.0, value=45.0
        )
    with st.expander("Cooling & Facilities", expanded=True):
        cooling_setpoint = st.number_input(
            "Cooling Setpoint (°C)", min_value=10.0, max_value=30.0, value=19.0
        )
        aisle_containment = st.checkbox("Hot/Cold Aisle Containment in place", value=False)


def action_icon_svg(action_title: str) -> str:
    title = action_title.lower()
    if "consolidation" in title:
        return (
            "<svg class='action-icon' width='16' height='16' viewBox='0 0 24 24' fill='none' "
            "xmlns='http://www.w3.org/2000/svg'><path d='M4 4h16v6H4z' fill='#cfe0ff'/>"
            "<path d='M6 13h12v7H6z' fill='#9fb2ff'/></svg>"
        )
    if "cooling" in title:
        return (
            "<svg class='action-icon' width='16' height='16' viewBox='0 0 24 24' fill='none' "
            "xmlns='http://www.w3.org/2000/svg'><path d='M12 3v18' stroke='#cfe0ff' stroke-width='2'/>"
            "<path d='M8 7h8M8 12h8M8 17h8' stroke='#cfe0ff' stroke-width='2'/></svg>"
        )
    if "aisle" in title:
        return (
            "<svg class='action-icon' width='16' height='16' viewBox='0 0 24 24' fill='none' "
            "xmlns='http://www.w3.org/2000/svg'><path d='M4 4h6v16H4z' fill='#cfe0ff'/>"
            "<path d='M14 4h6v16h-6z' fill='#9fb2ff'/></svg>"
        )
    if "virtualization" in title:
        return (
            "<svg class='action-icon' width='16' height='16' viewBox='0 0 24 24' fill='none' "
            "xmlns='http://www.w3.org/2000/svg'><rect x='4' y='4' width='7' height='7' fill='#cfe0ff'/>"
            "<rect x='13' y='4' width='7' height='7' fill='#9fb2ff'/>"
            "<rect x='4' y='13' width='7' height='7' fill='#9fb2ff'/></svg>"
        )
    return (
        "<svg class='action-icon' width='16' height='16' viewBox='0 0 24 24' fill='none' "
        "xmlns='http://www.w3.org/2000/svg'><circle cx='12' cy='12' r='8' stroke='#cfe0ff' stroke-width='2'/></svg>"
    )


if page == "Landing":
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
    left, right = st.columns([1.2, 1])
    with left:
        st.markdown("<div class='section-title'>Why GreenDC?</div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="glass">
                A practical platform to measure, explain, and validate energy and carbon reductions.
                Built for industrial data centers with realistic constraints.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("")
        st.markdown(
            """
            <div class="glass">
                <b>Core pillars:</b>
                <ul>
                    <li>Measurable KPIs (PUE, DCiE, CO2)</li>
                    <li>Actionable recommendations</li>
                    <li>Scenario validation to reach -25%</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown("<div class='section-title'>Platform Snapshot</div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="glass">
                <b>Inputs:</b> Energy, cooling, utilization, carbon factor<br><br>
                <b>Outputs:</b> KPIs, AI recommendations, savings simulation<br><br>
                <span class="badge badge-solid">Audit-ready</span>
                <span class="badge badge-solid">Explainable</span>
                <span class="badge badge-solid">Lightweight</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

if page == "Dashboard":
    st.markdown(
        """
        <div class="topbar">
            <div><b>GreenDC</b> <span class="subtle">| Audit Console</span></div>
            <div class="nav">
                <a href="#metrics">Metrics</a>
                <a href="#recommendations">Recommendations</a>
                <a href="#simulation">Simulation</a>
                <a href="#about">About</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    metrics_col, recs_col = st.columns([1, 1])

    with metrics_col:
        st.markdown("<div id='metrics' class='section-title'>Key Metrics</div>", unsafe_allow_html=True)
        pue = calculate_pue(it_energy_mwh, total_energy_mwh)
        dcie = calculate_dcie(it_energy_mwh, total_energy_mwh)
        co2_tonnes = calculate_co2_tonnes(total_energy_mwh, carbon_factor)

        metric_cols = st.columns(3)
        with metric_cols[0]:
            st.markdown(
                f"<div class='metric-card'><h3>"
                f"<svg class='svg-icon' width='14' height='14' viewBox='0 0 24 24' fill='none' "
                f"xmlns='http://www.w3.org/2000/svg'><path d='M13 2L3 14h7l-1 8 10-12h-7l1-8z' "
                f"fill='#cfe0ff'/></svg>PUE</h3><div class='value'>{pue:.2f}</div></div>",
                unsafe_allow_html=True,
            )
        with metric_cols[1]:
            st.markdown(
                f"<div class='metric-card'><h3>"
                f"<svg class='svg-icon' width='14' height='14' viewBox='0 0 24 24' fill='none' "
                f"xmlns='http://www.w3.org/2000/svg'><path d='M4 19h16v2H4z' fill='#cfe0ff'/>"
                f"<path d='M6 17V9h3v8H6zm5 0V5h3v12h-3zm5 0v-6h3v6h-3z' fill='#cfe0ff'/></svg>"
                f"DCiE</h3><div class='value'>{dcie:.1f}%</div></div>",
                unsafe_allow_html=True,
            )
        with metric_cols[2]:
            st.markdown(
                f"<div class='metric-card'><h3>"
                f"<svg class='svg-icon' width='14' height='14' viewBox='0 0 24 24' fill='none' "
                f"xmlns='http://www.w3.org/2000/svg'><path d='M12 2C7 2 3 6 3 11c0 4 2.6 7.5 6.4 8.7'"
                f" stroke='#cfe0ff' stroke-width='2' fill='none'/>"
                f"<path d='M12 2c5 0 9 4 9 9 0 4-2.6 7.5-6.4 8.7' stroke='#cfe0ff' stroke-width='2' fill='none'/>"
                f"</svg>CO2</h3><div class='value'>{co2_tonnes:.1f} t/y</div></div>",
                unsafe_allow_html=True,
            )

        st.markdown(
            f"<div class='glass'>Servers: <b>{servers}</b> | CPU Utilization: <b>{cpu_utilization:.1f}%</b>"
            f" | Cooling Setpoint: <b>{cooling_setpoint:.1f} °C</b></div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='subtle'>Tip: Improve DCiE by reducing non-IT energy overheads.</div>",
            unsafe_allow_html=True,
        )

    with recs_col:
        st.markdown("<div id='recommendations' class='section-title'>AI Recommendations</div>", unsafe_allow_html=True)
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
        for rec in recs_data:
            st.markdown(
                f"<div class='rec-card'>"
                f"<div class='rec-title'>{action_icon_svg(rec['Action'])}{rec['Action']}</div>"
                f"<div class='subtle'>{rec['Why it helps']}</div>"
                f"<div class='rec-meta'>Estimated Saving: {rec['Estimated Saving (%)']}%</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown("<div id='simulation' class='section-title'>Before / After Simulation</div>", unsafe_allow_html=True)
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
    st.markdown(
        "<div class='footer'>GreenDC Audit Platform • Responsible by design • © GreenAI Systems</div>",
        unsafe_allow_html=True,
    )

if page == "About":
    st.markdown("<div id='about' class='section-title'>About the Platform</div>", unsafe_allow_html=True)
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
    st.markdown("")
    st.markdown(
        """
        <div class="glass">
            <b>Modules:</b> frontend, energy_metrics, ai_recommendation, simulation, case_study.
            <br><br>
            <span class="badge badge-solid">Green IT</span>
            <span class="badge badge-solid">Green Coding</span>
            <span class="badge badge-solid">Proportional Computing</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
