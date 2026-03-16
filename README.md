# 🌿 GreenDC Audit Platform

An AI-assisted platform for energy and carbon audits of industrial data centers.
Built with Green IT and Green Coding principles, the platform delivers a modern,
3D-inspired dashboard experience while staying sober, efficient, and measurable.

## 🚀 Project Summary

GreenDC Audit Platform computes core Green IT metrics (PUE, DCiE, CO2) and builds
actionable optimization plans to reach a **-25% CO2 reduction target**. It is a
lightweight, modular system that favors proportional computing and transparent logic.

## ⭐ Branch Focus (main)

- **Branch**: `main`
- **Owner**: Gemima Ondele Pourou (Maintainer)
- **Role**: Stable demo branch that presents the full platform experience and full setup guide.

## ✨ Core Features

- 🧾 Data center input form (energy, servers, utilization, cooling, carbon factor)
- 📊 Automatic calculations: PUE, DCiE, annual CO2 emissions
- 🤖 AI-assisted recommendations (rules-based, explainable)
- 🔁 Before/after scenario simulation
- 🖥️ Dashboard with tables, charts, and summary insights
- 📂 Document ingestion (PDF/CSV/DOCX) with metric extraction
- 🧠 GreenDC Audit AI for audit guidance and CO2 reduction plans
- 🧾 Document QA for workload benchmarks and audit scenarios
- ✅ Applied parameter tagging and KPI source badges

## 🧩 Architecture and Modules

- `frontend/` : Streamlit UI and user flow
- `energy_metrics/` : PUE, DCiE, CO2 formulas
- `ai_recommendation/` : rule-based recommendation engine
- `simulation/` : scenario modeling and impact aggregation
- `case_study/` : example inputs and datasets
- `knowledge_base/` : rules and standards for explainable AI

## 📚 Documentation

- `docs/gemima_ai_prompt.md` : Prompt Cursor IA + architecture + pseudo-code (Gemima)

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

## 🧠 Module: AI & Recommendation Engine (Joseph Fabrice Tsapfack)

- **Purpose**: Convert Green IT rules into explainable, prioritized actions.
- **How it works**:
  - Applies thresholds (CPU, cooling, virtualization, PUE) to trigger actions.
  - Adds reasons and estimated savings for each recommendation.
  - Optional ML ranking (lightweight) can reorder actions by impact.

## 📈 Module: Simulation & Scenario Analysis (Balasundaram Nandaa)

- **Purpose**: Validate the -25% CO2 target through before/after scenarios.
- **How it works**:
  - Computes savings per action (MWh/year, tCO2/year).
  - Combines actions into a single optimized scenario.
  - Produces comparison tables and charts for the dashboard.

## 🌱 Module: Energy Validation & Assumptions (Pierre Joel Taafo)

- **Purpose**: Ensure realistic energy assumptions and ISO 50001 coherence.
- **How it works**:
  - Defines ranges for cooling savings, setpoint impact, and electrical losses.
  - Validates that the -25% trajectory is credible and non-exaggerated.
  - Provides non-technical sustainability justification for reporting.

## 🌱 Branch Strategy

- `main` : stable demo version
- `dev` : integration branch
- Feature branches:
  - `feature/frontend-dashboard` (Gemima) — UI/UX, dashboard integration
  - `feature/energy-metrics` (Mike-Brady) — formulas, case study datasets
  - `feature/ai-recommendation` (Joseph) — rules engine, explainability, ML ranking
  - `feature/simulation-engine` (Nandaa) — before/after scenarios, charts
  - `feature/energy-validation` (Pierre Joel) — assumptions, ISO 50001 validation

## 🛠️ Tools and Stack

- Python 3.x
- Streamlit (UI)
- Pandas (data handling)
- JSON / CSV datasets
- pypdf (PDF parsing)
- python-docx (DOCX parsing)
- huggingface_hub (dataset sync)
- GitHub for collaboration

## 🧭 User Guide (Local Run)

1. Install dependencies
   - `pip install -r requirements.txt`
2. Start the app
   - `streamlit run frontend/app.py`
3. Enter data center inputs in the sidebar
4. (Optional) Upload audit documents to auto-apply parameters
5. Review metrics, recommendations, and simulation results
6. Use Document QA for workload benchmark analysis

## 🧰 Environment Setup (Windows / macOS / Linux)

### Windows (PowerShell)

1. Create and activate a virtual environment
   - `python -m venv .greenit`
   - `.\\.greenit\\Scripts\\Activate.ps1`
2. Install dependencies
   - `pip install -r requirements.txt`
3. Run the app
   - `streamlit run frontend/app.py`

### macOS / Linux (bash)

1. Create and activate a virtual environment
   - `python3 -m venv .greenit`
   - `source .greenit/bin/activate`
2. Install dependencies
   - `pip install -r requirements.txt`
3. Run the app
   - `streamlit run frontend/app.py`

### Environment Variables (optional)

Create `.greenit/.env` and add:
- `HF_TOKEN=your_huggingface_token`
- `OPENAI_API_KEY=` (not used in offline mode)

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
