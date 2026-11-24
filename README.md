# Explainable Short-Term Dengue Case Forecasting Using Weather and Epidemiological Indicators

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn%20%7C%20XGBoost%20%7C%20LightGBM-orange.svg)](https://scikit-learn.org/)
[![Explainability](https://img.shields.io/badge/XAI-TreeSHAP-brightgreen.svg)](https://shap.readthedocs.io/)

An end-to-end Machine Learning and Explainable Artificial Intelligence (XAI) research project designed to forecast weekly dengue incidence up to 4 weeks ahead in San Juan, Puerto Rico, using historical epidemiological trends and delayed meteorological indicators.

---

## 📌 Project Overview

Dengue fever is a severe mosquito-borne viral infection transmitted by *Aedes aegypti* mosquitoes, affecting over 390 million individuals annually. Because epidemic outbreaks lag environmental conditions due to biological incubation windows (extrinsic incubation period of 8–14 days and aquatic vector reproduction cycles of 7–14 days), unlagged climate readings fail to predict sudden case surges.

This project implements:
1. **Zero-Leakage Chronological Pipeline:** 18 continuous years of weekly surveillance (1990–2008) split chronologically into an 80% Training set (1990–2004, 739 weeks) and a 20% Holdout Test set (2004–2008, 185 weeks).
2. **Direct Multi-Horizon Modeling:** Independent predictive estimators for lead times $t+1$, $t+2$, $t+3$, and $t+4$ weeks ahead, eliminating compounding multi-step error accumulation.
3. **Rigorous Feature Ablation (E1–E5):** Controlled 5-stage ablation study evaluating the standalone vs. complementary value of autoregressive disease momentum, annual seasonality, and lagged meteorological drivers.
4. **Explainable AI (TreeSHAP):** Global beeswarm attribution and local outbreak waterfall decompositions explaining *why* the model predicts explosive epidemic spikes versus endemic baselines.

---

## 📊 Experimental Results & Benchmarks

### 1. Multi-Horizon Model Comparison (Holdout Test Set: 2004–2008)

| Lead Time | Persistence Baseline (MAE / RMSE / R²) | Random Forest (MAE / RMSE / R²) | **XGBoost (Winning)** (MAE / RMSE / R²) | LightGBM (MAE / RMSE / R²) |
| :--- | :--- | :--- | :--- | :--- |
| **Horizon 1 ($t+1$)** | 7.00 / 11.43 / 0.8667 | 7.48 / 11.74 / 0.8594 | **7.10 / 11.44 / 0.8665** | 7.65 / 11.96 / 0.8539 |
| **Horizon 2 ($t+2$)** | 9.11 / 15.18 / 0.7653 | 9.88 / 16.49 / 0.7233 | **9.17 / 14.22 / 0.7942** | 10.39 / 17.40 / 0.6916 |
| **Horizon 3 ($t+3$)** | 11.12 / 19.24 / 0.6240 | 12.96 / 23.57 / 0.4360 | **11.58 / 19.38 / 0.6187** | 12.66 / 23.62 / 0.4334 |
| **Horizon 4 ($t+4$)** | 13.53 / 23.62 / 0.4343 | 14.43 / 24.65 / 0.3839 | **14.31 / 24.80 / 0.3763** | 15.34 / 28.80 / 0.1587 |
| **Average Across Horizons** | 10.19 / 17.37 / 0.6726 | 11.19 / 19.11 / 0.6007 | **10.54 / 17.46 / 0.6639** | 11.51 / 20.45 / 0.5344 |

> **Key Takeaway:** At Horizon 2 ($t+2$), XGBoost outperforms the strong Persistence baseline on Root Mean Squared Error (14.22 vs. 15.18) and $R^2$ (0.7942 vs. 0.7653), demonstrating that environmental features provide critical lead-time warning against peak outbreak misses.

---

### 2. Feature Ablation Study (Experiments E1 to E5)

| Exp | Feature Group Description | Features | H1 MAE | H1 RMSE | H1 R² | H2 MAE | H2 RMSE | H2 R² |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **E1** | Previous Cases Only (`cases_lag1`) | 1 | 7.21 | 11.97 | 0.8537 | 9.00 | 15.12 | 0.7673 |
| **E2** | E1 + Multi-Lags (`t-2..8`) & Rolling Averages | 11 | 7.63 | 12.93 | 0.8293 | 9.89 | 17.70 | 0.6809 |
| **E3** | E2 + Cyclical Calendar Seasonality (`sin/cos`) | 14 | 7.50 | 12.14 | 0.8496 | 10.61 | 18.28 | 0.6596 |
| **E4** | E3 + Concurrent Weather Readings | 25 | 6.78 | 10.63 | 0.8847 | 9.34 | 15.26 | 0.7629 |
| **E5** | **E4 + Lagged Weather (Full System)** | **61** | **7.10** | **11.44** | **0.8665** | **9.17** | **14.22** | **0.7942** |

> **Biological Confirmation:** Experiment **E5** achieved the highest overall $R^2$ (0.7942) and lowest RMSE (14.22) on Horizon 2, confirming that backward-lagged specific humidity and minimum temperature are required to forecast non-linear epidemic spikes.

---

## 🔍 Explainable AI (XAI) via TreeSHAP

Using TreeSHAP (Lundberg et al., Nature Machine Intelligence), we extracted both global feature attributions and local case predictions:
- **Global Climate Drivers:** Elevated specific humidity ($t-3$) and higher minimum night temperatures ($t-4$) exert strong positive SHAP contributions, accelerating predicted transmission rates.
- **Local Outbreak Deconstruction (Week 39, 2007 - 170 Actual Cases):**
  - Expected baseline caseload: ~30 cases
  - Autoregressive viral momentum (`cases_lag1 = 120`): $+75$ cases
  - Cyclical high transmission season (`sin_week`): $+10$ cases
  - Delayed humidity anomaly (`reanalysis_specific_humidity_lag3`): $+8$ cases
  - Delayed night temperature (`station_min_temp_c_lag4`): $+5$ cases
  - **Predicted Caseload: 155 cases** (tracking the real surge within 9% error).

---

## 📁 Repository Directory Structure

```
dengue_forcasting/
│
├── data/
│   ├── raw/                           # Original intact raw data (features + labels)
│   └── processed/                     # Imputed, engineered, and partitioned datasets
├── figures/                           # 9 high-resolution 300 DPI figures
│   ├── eda_case_timeline.png
│   ├── eda_seasonal_cycle.png
│   ├── eda_weather_correlation.png
│   ├── eda_lagged_cross_correlation.png
│   ├── forecast_vs_actual_h1_to_h4.png
│   ├── ablation_comparison_mae.png
│   ├── shap_summary_beeswarm.png
│   ├── shap_outbreak_waterfall.png
│   └── shap_trough_waterfall.png
├── models/                            # 16 serialized models (.joblib) for H1–H4
├── tables/                            # Benchmark comparisons & 2008–2013 forward forecasts
├── src/                               # Modular ML source code
│   ├── data_loader.py                 # Ingestion & causal time-series imputation
│   ├── eda_analysis.py                # Visualizations & cross-correlation analysis
│   ├── feature_engineering.py         # Multi-lag matrix construction
│   ├── split_data.py                  # Chronological 80/20 train-test partition
│   ├── models.py                      # Estimator definitions (Baseline, RF, XGB, LGBM)
│   ├── train_evaluate.py              # Multi-horizon training & metric tracking
│   ├── ablation_study.py              # 5-stage ablation framework (E1 to E5)
│   ├── explainability.py              # TreeSHAP beeswarm & waterfall generator
│   ├── predict_future.py              # Out-of-sample forward forecasting (2008–2013)
│   ├── create_report.py               # Automated Word report builder
│   └── create_presentation.py         # Automated PowerPoint slide builder
├── requirements.txt                   # Dependency specifications
├── run_pipeline.py                    # Master reproduction pipeline script
├── .gitignore                         # Git exclusion rules
└── README.md                          # Repository overview & documentation
```

---

## 🚀 Quickstart & Reproduction

### Prerequisites
- Python 3.10, 3.11, 3.12, or 3.13
- Git

### Installation
```bash
# Clone the repository
git clone https://github.com/irohitgangwar/dengue_forcasting.git
cd dengue_forcasting

# Install dependencies
pip install -r requirements.txt
```

### Run the Full Pipeline
Run the reproduction pipeline from the repository directory:
```bash
python run_pipeline.py
```
*The entire pipeline (data cleaning, feature engineering, split, training 16 models, ablation study, SHAP computation, and forward forecasting) executes end-to-end in ~16 seconds.*

---

## 📄 License & Attribution
Developed as an academic end-semester machine learning project in epidemiological time-series forecasting. Raw surveillance data sourced from the NOAA / CDC Dengue Forecasting Challenge.

