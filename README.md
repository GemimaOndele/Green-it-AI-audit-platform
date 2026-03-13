# 📊 GreenDC Audit Platform — Energy Metrics

This branch focuses on the **energy metrics engine**, validation against course TDs,
and the real company case-study datasets (Google).

## 🧪 Branch Focus (feature/energy-metrics)

- **Branch**: `feature/energy-metrics`
- **Owner**: Mike‑Brady Mbolim Mbock (Energy Metrics Engineer)
- **Scope**: PUE/DCiE/CO2 formulas, validation, and case‑study datasets.
- **Note**: Full setup and OS-specific environment guides live on `main`.

## 🧾 How this part works

- Deterministic formulas compute **PUE**, **DCiE**, **annual energy**, and **CO2**.
- Validation is performed against course exercises in `case_study/td_validation.json`.
- A real company case study (Google) is packaged as CSV/JSON + a short report.

## ✅ Features delivered in this branch

- `energy_metrics/metrics.py` with core formulas and ratings.
- `case_study/google_case_study.csv` (table‑based dataset).
- `case_study/google_case_study.json` (structured dataset).
- `case_study/td_validation.json` (course TD verification table).
- `docs/google_case_study_report.docx` (short report).

## ▶️ How to run / test this part

1. Install dependencies  
   - `pip install -r requirements.txt`
2. Run the app  
   - `streamlit run frontend/app.py`
3. In the sidebar, select **Real case study (Google)**  
4. Check the **TD Validation** table to confirm formula matches

## 🔗 Project Overview

See the full project description on `main`.
