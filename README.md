# 🌿 GreenDC Audit Platform

An AI-assisted platform for energy and carbon audits of industrial data centers.
Built with Green IT and Green Coding principles, the platform delivers a modern,
3D-inspired dashboard experience while staying sober, efficient, and measurable.

## 🚀 Project Summary

GreenDC Audit Platform computes core Green IT metrics (PUE, DCiE, CO2) and builds
actionable optimization plans to reach a **-25% CO2 reduction target**. It is a
lightweight, modular system that favors proportional computing and transparent logic.

## 🧪 Branch Focus (dev)

- **Branch**: `dev`
- **Owner**: Gemima Ondele Pourou (Platform Architect & Frontend/Integration)
- **Role**: Integration branch for all feature work before the stable demo on `main`.

## ✨ Core Features

- 🧾 Data center input form (energy, servers, utilization, cooling, carbon factor)
- 📊 Automatic calculations: PUE, DCiE, annual CO2 emissions
- 🤖 AI-assisted recommendations (rules-based, explainable)
- 🔁 Before/after scenario simulation
- 🖥️ Dashboard with tables, charts, and summary insights

## 🧩 Architecture and Modules

- `frontend/` : Streamlit UI and user flow
- `energy_metrics/` : PUE, DCiE, CO2 formulas
- `ai_recommendation/` : rule-based recommendation engine
- `simulation/` : scenario modeling and impact aggregation
- `case_study/` : example inputs and datasets

## 👥 Team Roles and Responsibilities

- **Gemima Ondele Pourou** (Platform Architect & Frontend/Integration)
  - Architecture, UI, integration, documentation
- **Joseph Fabrice Tsapfack** (AI & Recommendation Engine)
  - AI logic, rule design, action prioritization
- **Mike-Brady Mbolim Mbock** (Energy Metrics Engineer)
  - PUE/DCiE/CO2 calculations, data model, validation
- **Balasundaram Nandaa** (Simulation & Scenario Analysis)
  - Before/after simulation, impact modeling, validation
- **Pierre Joel Taafo** (Energy & Sustainability)
  - Energy assumptions, ISO 50001 alignment, validation

## 🌱 Branch Strategy

- `main` : stable demo version
- `dev` : integration branch
- Feature branches:
  - `feature/frontend-dashboard` (Gemima)
  - `feature/energy-metrics` (Mike-Brady)
  - `feature/ai-recommendation` (Joseph)
  - `feature/simulation-engine` (Nandaa)
  - `feature/energy-validation` (Pierre Joel)

## 🛠️ Tools and Stack

- Python 3.x
- Streamlit (UI)
- Pandas (data handling)
- JSON / CSV datasets
- GitHub for collaboration

## 🧭 User Guide (Local Run)

1. Install dependencies
   - `pip install -r requirements.txt`
2. Start the app
   - `streamlit run frontend/app.py`
3. Enter data center inputs in the sidebar
4. Review metrics, recommendations, and simulation results

## 🤝 Team Workflow Guide

See `docs/TEAM_GUIDE.md` for the clone, branch, and PR workflow.

## 🏭 Example Case Study

- IT Energy: 780 MWh/year
- Total Energy: 1300 MWh/year
- Carbon factor: 0.30 kg CO2/kWh
- PUE: ~1.67
- CPU utilization: 18%
- Cooling setpoint: 19 C
- No aisle containment

Target: **-25% CO2 reduction within 12 months**.

## 🎯 Why This Project Matters

- Based on course indicators and audit methodology
- Realistic industrial context and constraints
- Quantified improvement plan with clear metrics
- AI used as decision support, not as a gimmick

## 🗺️ Roadmap (Short)

- Integrate richer datasets and CSV import
- Refine simulation with energy assumptions
- Improve dashboard visuals and storytelling
- Prepare demo scenario and final report
