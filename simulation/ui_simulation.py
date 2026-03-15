import pandas as pd
import streamlit as st
from .scenario import get_simulation_results


def render_simulation_section():
    st.markdown(
        "<div id='simulation' class='section-title'>Before / After Simulation</div>",
        unsafe_allow_html=True,
    )

    simulation = get_simulation_results()
    baseline = simulation["baseline"]
    single_actions = simulation["single_actions"]
    combined = simulation["combined"]

    comparison_df = pd.DataFrame([
        {
            "Metric": "Total Energy (MWh/year)",
            "Baseline": baseline["total_energy_mwh"],
            "Optimized": combined["optimized_energy_mwh"],
        },
        {
            "Metric": "CO2 Emissions (t/year)",
            "Baseline": baseline["co2_tonnes_per_year"],
            "Optimized": combined["optimized_co2_tonnes"],
        },
        {
            "Metric": "Energy Saved (MWh/year)",
            "Baseline": 0,
            "Optimized": combined["energy_saved_mwh"],
        },
        {
            "Metric": "CO2 Saved (t/year)",
            "Baseline": 0,
            "Optimized": combined["co2_saved_tonnes"],
        },
        {
            "Metric": "Reduction (%)",
            "Baseline": 0,
            "Optimized": combined["reduction_percent"],
        },
    ])

    st.subheader("Baseline vs Optimized Comparison")
    st.dataframe(comparison_df, use_container_width=True)

    actions_df = pd.DataFrame([
        {
            "Action": a["action_name"],
            "Energy Saved (MWh/year)": a["energy_saved_mwh"],
            "CO2 Saved (t/year)": a["co2_saved_tonnes"],
        }
        for a in single_actions
    ])

    st.subheader("Savings by Action")
    st.dataframe(actions_df, use_container_width=True)

    energy_chart_df = pd.DataFrame([
        {"Scenario": "Baseline", "Energy (MWh/year)": baseline["total_energy_mwh"]},
        {"Scenario": "Optimized", "Energy (MWh/year)": combined["optimized_energy_mwh"]},
    ])

    st.subheader("Baseline vs Optimized Energy")
    st.bar_chart(energy_chart_df.set_index("Scenario"))

    action_chart_df = pd.DataFrame([
        {"Action": a["action_name"], "Energy Saved (MWh/year)": a["energy_saved_mwh"]}
        for a in single_actions
    ])

    st.subheader("Energy Saved per Action")
    st.bar_chart(action_chart_df.set_index("Action"))

    st.subheader("Target Validation")
    st.markdown(
        f"""
        CO2 Reduction Achieved: **{combined['reduction_percent']:.2f}%**  
        Target: **25%**  
        Status: **{'Achieved' if combined['target_achieved'] else 'Not achieved'}**
        """
    )

    if combined["target_achieved"]:
        st.success("Target -25% CO2 is achieved.")
    else:
        st.warning("Target -25% CO2 is not achieved.")