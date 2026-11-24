"""
run_pipeline.py - Master Reproduction Pipeline Script
======================================================
Project: Explainable Short-Term Dengue Case Forecasting
Domain: Public Health Informatics & Machine Learning

This script runs the complete end-to-end Machine Learning pipeline.
It auto-resolves directory paths so it works whether executed from the
project root, from inside teacher_submission/, or directly in an IDE.
"""

import os
import sys
import time
import tempfile
os.environ['MPLCONFIGDIR'] = tempfile.gettempdir()
import matplotlib
matplotlib.use('Agg')

# -------------------------------------------------------------
# 1. Directory Path Setup
# -------------------------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))

# Determine project root and package directory dynamically
if os.path.exists(os.path.join(current_dir, 'src')):
    project_root = os.path.dirname(current_dir)
    package_dir = current_dir
else:
    project_root = current_dir
    candidates = ['dengue_forecasting_project', 'dengue forecasting project', 'teacher_submission']
    package_dir = current_dir
    for c in candidates:
        cand_path = os.path.join(current_dir, c)
        if os.path.exists(cand_path):
            package_dir = cand_path
            break

# Ensure working directory is project root
os.chdir(project_root)

# Add package directory and src to sys.path so 'from src....' resolves anywhere
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)
src_dir = os.path.join(package_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# -------------------------------------------------------------
# 2. Clean Package Imports from src/
# -------------------------------------------------------------
from src.data_loader import process_and_save
from src.eda_analysis import run_eda
from src.feature_engineering import run_feature_engineering
from src.split_data import perform_chronological_split
from src.train_evaluate import run_multi_horizon_training
from src.ablation_study import run_ablation_study
from src.explainability import run_shap_analysis
from src.predict_future import generate_future_forecasts


def main():
    start_time = time.time()
    print("=" * 70)
    print("  EXPLAINABLE SHORT-TERM DENGUE CASE FORECASTING PIPELINE")
    print(f"  Project Root: {project_root}")
    print("=" * 70)
    
    print("\n>>> STAGE 1: Data Synchronization & Chronological Imputation")
    process_and_save()
    
    print("\n>>> STAGE 2: Exploratory Data Analysis & Biological Visualization")
    run_eda()
    
    print("\n>>> STAGE 3: Systematic Feature Engineering & Target Alignment")
    run_feature_engineering()
    
    print("\n>>> STAGE 4: Chronological Train-Test Partitioning")
    perform_chronological_split()
    
    print("\n>>> STAGE 5: Multi-Horizon Model Training & Evaluation")
    run_multi_horizon_training()
    
    print("\n>>> STAGE 6: Feature Ablation Study (Experiments E1 to E5)")
    run_ablation_study()
    
    print("\n>>> STAGE 7: Explainable AI (XAI) via TreeSHAP")
    run_shap_analysis()
    
    print("\n>>> STAGE 8: Out-of-Sample Forward Prediction (2008–2013)")
    generate_future_forecasts()
    
    elapsed = time.time() - start_time
    print("\n" + "=" * 70)
    print(f"  COMPLETE PIPELINE EXECUTED SUCCESSFULLY IN {elapsed:.1f} SECONDS!")
    print("=" * 70)


if __name__ == '__main__':
    main()
