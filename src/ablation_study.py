"""
ablation_study.py - Feature Ablation Pipeline (Experiments E1 to E5)
=====================================================================
Project: Explainable Short-Term Dengue Case Forecasting
"""

import os
import tempfile
os.environ['MPLCONFIGDIR'] = tempfile.gettempdir()

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_TRAIN_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'train_split.csv')
DEFAULT_TEST_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'test_split.csv')
DEFAULT_TABLES_DIR = os.path.join(BASE_DIR, 'tables')
DEFAULT_FIGURES_DIR = os.path.join(BASE_DIR, 'figures')


def get_ablation_feature_subsets(all_columns: list) -> dict:
    e1_cols = ['cases_lag1']
    case_lags = ['cases_lag2', 'cases_lag3', 'cases_lag4', 'cases_lag8']
    rolling_cols = ['cases_roll_mean_4', 'cases_roll_std_4', 'cases_roll_mean_8',
                    'cases_roll_std_8', 'cases_trend_4', 'cases_ratio_4']
    e2_cols = e1_cols + case_lags + rolling_cols
    seasonal_cols = ['sin_week', 'cos_week', 'month']
    e3_cols = e2_cols + seasonal_cols
    
    curr_weather = [
        'reanalysis_specific_humidity_g_per_kg',
        'reanalysis_dew_point_temp_k',
        'station_min_temp_c',
        'station_avg_temp_c',
        'station_max_temp_c',
        'reanalysis_air_temp_k',
        'reanalysis_relative_humidity_percent',
        'precipitation_amt_mm',
        'station_precip_mm',
        'ndvi_se', 'ndvi_sw'
    ]
    curr_weather = [c for c in curr_weather if c in all_columns]
    e4_cols = e3_cols + curr_weather
    
    ignore = ['city', 'year', 'weekofyear', 'week_start_date', 'total_cases',
              'target_h1', 'target_h2', 'target_h3', 'target_h4']
    e5_cols = [c for c in all_columns if c not in ignore]
    
    return {
        'E1': ('Previous Cases Only', e1_cols),
        'E2': ('E1 + Case Lags & Rolling Stats', e2_cols),
        'E3': ('E2 + Cyclical Seasonal Features', e3_cols),
        'E4': ('E3 + Current Weather', e4_cols),
        'E5': ('E4 + Lagged Weather (Full System)', e5_cols)
    }


def run_ablation_study(train_path: str = DEFAULT_TRAIN_PATH,
                       test_path: str = DEFAULT_TEST_PATH,
                       tables_dir: str = DEFAULT_TABLES_DIR,
                       figures_dir: str = DEFAULT_FIGURES_DIR):
    os.makedirs(tables_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)
    
    print(f"Loading data for ablation study...")
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    
    feature_subsets = get_ablation_feature_subsets(train_df.columns.tolist())
    ablation_results = []
    horizons = [1, 2]
    
    for exp_id, (exp_desc, cols) in feature_subsets.items():
        print(f"\nEvaluating Experiment {exp_id}: {exp_desc} ({len(cols)} features)...")
        h_maes, h_rmses, h_r2s = [], [], []
        
        for h in horizons:
            target_col = f"target_h{h}"
            X_train, y_train = train_df[cols], train_df[target_col]
            X_test, y_test = test_df[cols], test_df[target_col]
            
            model = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.05,
                subsample=0.8,
                colsample_bytree=0.8 if len(cols) > 4 else 1.0,
                random_state=42,
                verbosity=0
            )
            model.fit(X_train, y_train)
            y_pred = np.maximum(0, model.predict(X_test))
            
            mae = mean_absolute_error(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            r2 = r2_score(y_test, y_pred)
            
            h_maes.append(mae)
            h_rmses.append(rmse)
            h_r2s.append(r2)
            print(f"  H{h} -> MAE: {mae:.2f} | RMSE: {rmse:.2f} | R²: {r2:.4f}")

        ablation_results.append({
            'Experiment': exp_id,
            'Description': exp_desc,
            'Feature_Count': len(cols),
            'H1_MAE': round(h_maes[0], 2),
            'H1_RMSE': round(h_rmses[0], 2),
            'H1_R2': round(h_r2s[0], 4),
            'H2_MAE': round(h_maes[1], 2),
            'H2_RMSE': round(h_rmses[1], 2),
            'H2_R2': round(h_r2s[1], 4),
            'Avg_MAE': round(np.mean(h_maes), 2),
            'Avg_RMSE': round(np.mean(h_rmses), 2),
            'Avg_R2': round(np.mean(h_r2s), 4)
        })

    ablation_df = pd.DataFrame(ablation_results)
    csv_path = os.path.join(tables_dir, 'ablation_study_results.csv')
    ablation_df.to_csv(csv_path, index=False)
    print(f"\nAblation study results saved to: {csv_path}")
    
    sns.set_theme(style='whitegrid', font='sans-serif')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
    palette = ['#aec7e8', '#7bccc4', '#43a2ca', '#0868ac', '#2ca02c']
    
    bars1 = ax1.bar(ablation_df['Experiment'], ablation_df['Avg_MAE'], color=palette, edgecolor='black', width=0.55)
    ax1.set_title('Average MAE Across Experiments (Lower is Better)', fontweight='bold', pad=12)
    ax1.set_ylabel('Mean Absolute Error (Cases/Week)')
    ax1.set_ylim(0, max(ablation_df['Avg_MAE']) * 1.25)
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 0.15, f'{yval:.2f}', ha='center', va='bottom', fontweight='bold')

    bars2 = ax2.bar(ablation_df['Experiment'], ablation_df['Avg_R2'], color=palette, edgecolor='black', width=0.55)
    ax2.set_title('Average R² Score Across Experiments (Higher is Better)', fontweight='bold', pad=12)
    ax2.set_ylabel('R² Score (Explained Variance)')
    ax2.set_ylim(0, 1.0)
    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f'{yval:.4f}', ha='center', va='bottom', fontweight='bold')

    plt.suptitle('Teacher-Mandated Feature Ablation Study: Impact of Adding Lagged Weather Features', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    chart_path = os.path.join(figures_dir, 'ablation_comparison_mae.png')
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Ablation comparison chart saved to: {chart_path}")
    return ablation_df


if __name__ == '__main__':
    run_ablation_study()
