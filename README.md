# 🎛️ GreenDC Audit Platform — Frontend Dashboard

This branch focuses on the **modern, 3D-inspired Streamlit interface** and full
integration of all modules into a clean, demo-ready flow.

## 🧪 Branch Focus

- **Branch**: `feature/frontend-dashboard`
- **Owner**: Gemima Ondele Pourou (Platform Architect & Frontend/Integration)
- **Scope**: UI/UX, layout, styling, and end-to-end integration.

## ✨ Key UI Goals

- Sleek dashboard with 3D-inspired cards and shadows
- Clear input workflow and instant results
- Visual storytelling for the -25% CO2 objective
- GreenDC Audit AI panel with audit guidance
- Document QA block for uploaded datasets
- Applied parameter badges and KPI source labels

## 🖥️ Interface Behavior & Features (How it works)

- **Navigation**: Top bar + sidebar sections (Metrics, Recommendations, Simulation, About).
- **Case study selector**: Choose *Course exercises (test)* or *Real case study (Google)*.
- **Inputs**: Sidebar fields are auto‑filled from documents or case study datasets.
- **KPI cards**: PUE, DCiE, CO2 show **Applied** badges + **Source** labels.
- **Recommendations**: Explainable, rule‑based actions with estimated savings.
- **Simulation**: Before/After energy scenario to validate the -25% CO2 target.
- **Documents**: Upload PDF/CSV/DOCX; extraction applies metrics automatically.
- **Document QA**: Analyze workload benchmarks separately from audit KPIs.
- **Insights & graphs**: Clear charts with labeled axes (CO2 current vs target, energy mix, PUE comparison).

## 🧩 Modules Integrated

- `frontend/` : Streamlit UI and user flow
- `energy_metrics/` : PUE, DCiE, CO2 formulas
- `ai_recommendation/` : rule-based recommendations
- `simulation/` : before/after scenario modeling
- Document ingestion (PDF/CSV/DOCX) and KPI extraction

## 🧭 Run the App (Local)

```
pip install -r requirements.txt
streamlit run frontend/app.py
```

## 🔗 Project Overview

See the full project description on `main`.
