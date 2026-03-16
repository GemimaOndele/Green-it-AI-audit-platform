
# 🤖 GreenDC Audit Platform — AI Recommendations

This branch focuses on **AI-assisted recommendation logic** with transparent,
rule-based decisions aligned with Green IT principles.

## 🧪 Branch Focus

- **Branch**: `feature/ai-recommendation`
- **Owner**: Joseph Fabrice Tsapfack (AI & Recommendation Engine)
- **Scope**: rule design, prioritization logic, explainability.

## ✅ Key Deliverables

- Rule-based recommendations (consolidation, cooling, virtualization)
- Clear explanations for each action
- Prioritization toward the -25% CO2 target
- Phase 2 ML ranking (optional, lightweight linear model)

## 🖥️ Interface Behavior & Features (How it works)

- **Inputs**: Reads audit KPIs and infrastructure inputs from the dashboard.
- **Rules engine**: Applies Green IT thresholds to trigger actions.
- **Explainability**: Each action includes a reason and estimated saving.
- **Prioritization**: Actions are ordered for maximum CO2 impact.
- **Optional ML ranking**: Reorders actions using a tiny linear model (no heavy AI).

## 🧩 Module

- `ai_recommendation/` : recommendation rules and scoring

## 🤖 Phase 2 ML Ranking (Optional)

The module includes a lightweight ML-based ranking layer to prioritize actions.
It uses a tiny linear regression model trained on synthetic samples (no external
dependencies) and can be enabled when needed.

How to enable:

- Set `use_ml_ranking=True` in the `AuditContext`, or
- Pass `use_ml_ranking=True` in the UI inputs before building the context.

## ▶️ Run Command

- `streamlit run frontend/app.py`

## 🔗 Project Overview

See the full project description on `main`.
