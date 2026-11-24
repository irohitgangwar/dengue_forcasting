"""
explainability.py - Explainable AI (XAI) via TreeSHAP
======================================================
Project: Explainable Short-Term Dengue Case Forecasting
"""

import os
import tempfile
os.environ['MPLCONFIGDIR'] = tempfile.gettempdir()

import pandas as pd
import numpy as np
import joblib
import shap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_MODEL_PATH = os.path.join(BASE_DIR, 'models', 'xgboost_h1.joblib')
DEFAULT_TEST_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'test_split.csv')
DEFAULT_FIGURES_DIR = os.path.join(BASE_DIR, 'figures')


def run_shap_analysis(model_path: str = DEFAULT_MODEL_PATH,
                      test_path: str = DEFAULT_TEST_PATH,
                      figures_dir: str = DEFAULT_FIGURES_DIR):
    os.makedirs(figures_dir, exist_ok=True)
    print(f"Loading trained model: {model_path}...")
    model = joblib.load(model_path)
    
    print(f"Loading test dataset: {test_path}...")
    test_df = pd.read_csv(test_path)
    
    ignore_cols = ['city', 'year', 'weekofyear', 'week_start_date', 'total_cases',
                   'target_h1', 'target_h2', 'target_h3', 'target_h4']
    feature_cols = [c for c in test_df.columns if c not in ignore_cols]
    X_test = test_df[feature_cols]
    
    print("Computing TreeSHAP values across all test weeks...")
    explainer = shap.TreeExplainer(model)
    shap_explanation = explainer(X_test)
    
    # 1. Global Beeswarm Summary Plot
    print("Generating Figure: Global SHAP Beeswarm Summary Plot...")
    fig = plt.figure(figsize=(12, 7))
    shap.plots.beeswarm(shap_explanation, max_display=15, show=False)
    plt.title("SHAP Beeswarm Summary: Global Drivers of Dengue Case Predictions", fontsize=14, fontweight='bold', pad=14)
    plt.tight_layout()
    beeswarm_path = os.path.join(figures_dir, 'shap_summary_beeswarm.png')
    plt.savefig(beeswarm_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {beeswarm_path}")
    
    # 2. Local Outbreak Waterfall Plot
    peak_idx = test_df['target_h1'].idxmax()
    peak_row = test_df.iloc[peak_idx]
    print(f"Peak Epidemic Test Week: {peak_row['week_start_date']} with {peak_row['target_h1']} cases (Row index {peak_idx})")
    
    fig = plt.figure(figsize=(10, 6))
    shap.plots.waterfall(shap_explanation[peak_idx], max_display=10, show=False)
    plt.title(f"SHAP Local Waterfall Explanation: Peak Epidemic Week ({peak_row['week_start_date']})", fontsize=12, fontweight='bold', pad=12)
    plt.tight_layout()
    waterfall_peak_path = os.path.join(figures_dir, 'shap_outbreak_waterfall.png')
    plt.savefig(waterfall_peak_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {waterfall_peak_path}")
    
    # 3. Local Endemic Trough Waterfall Plot
    trough_idx = test_df['target_h1'].idxmin()
    trough_row = test_df.iloc[trough_idx]
    print(f"Trough Endemic Test Week: {trough_row['week_start_date']} with {trough_row['target_h1']} cases (Row index {trough_idx})")
    
    fig = plt.figure(figsize=(10, 6))
    shap.plots.waterfall(shap_explanation[trough_idx], max_display=10, show=False)
    plt.title(f"SHAP Local Waterfall Explanation: Low Transmission Week ({trough_row['week_start_date']})", fontsize=12, fontweight='bold', pad=12)
    plt.tight_layout()
    waterfall_trough_path = os.path.join(figures_dir, 'shap_trough_waterfall.png')
    plt.savefig(waterfall_trough_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {waterfall_trough_path}")
    print("All SHAP explainability figures generated successfully!")


if __name__ == '__main__':
    run_shap_analysis()
