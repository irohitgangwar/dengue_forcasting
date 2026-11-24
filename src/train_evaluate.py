"""
train_evaluate.py - Direct Multi-Horizon Training & Evaluation Module
=====================================================================
Project: Explainable Short-Term Dengue Case Forecasting
"""

import os
import tempfile
os.environ['MPLCONFIGDIR'] = tempfile.gettempdir()

import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

try:
    from models import get_model
except ImportError:
    from src.models import get_model

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_TRAIN_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'train_split.csv')
DEFAULT_TEST_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'test_split.csv')
DEFAULT_MODELS_DIR = os.path.join(BASE_DIR, 'models')
DEFAULT_TABLES_DIR = os.path.join(BASE_DIR, 'tables')
DEFAULT_FIGURES_DIR = os.path.join(BASE_DIR, 'figures')


def get_feature_columns(df: pd.DataFrame) -> list:
    ignore_cols = ['city', 'year', 'weekofyear', 'week_start_date', 'total_cases',
                   'target_h1', 'target_h2', 'target_h3', 'target_h4']
    return [c for c in df.columns if c not in ignore_cols]


def evaluate_forecast(y_true, y_pred):
    y_pred_clipped = np.maximum(0, y_pred)
    mae = mean_absolute_error(y_true, y_pred_clipped)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred_clipped))
    r2 = r2_score(y_true, y_pred_clipped)
    return mae, rmse, r2, y_pred_clipped


def run_multi_horizon_training(train_path: str = DEFAULT_TRAIN_PATH,
                               test_path: str = DEFAULT_TEST_PATH,
                               models_dir: str = DEFAULT_MODELS_DIR,
                               tables_dir: str = DEFAULT_TABLES_DIR,
                               figures_dir: str = DEFAULT_FIGURES_DIR):
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(tables_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)
    
    print(f"Loading train ({train_path}) and test ({test_path})...")
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    
    feature_cols = get_feature_columns(train_df)
    print(f"Feature set size: {len(feature_cols)} features.")
    
    horizons = [1, 2, 3, 4]
    model_names = ['Persistence', 'Random_Forest', 'XGBoost', 'LightGBM']
    
    results = []
    predictions_dict = {m: {} for m in model_names}
    trained_models = {}
    
    for h in horizons:
        target_col = f"target_h{h}"
        print(f"\n==========================================")
        print(f" TRAINING FOR HORIZON {h} ({h} WEEK{'S' if h > 1 else ''} AHEAD: {target_col})")
        print(f"==========================================")
        
        X_train, y_train = train_df[feature_cols], train_df[target_col]
        X_test, y_test = test_df[feature_cols], test_df[target_col]
        
        for name in model_names:
            model = get_model(name)
            model.fit(X_train, y_train)
            
            y_pred = model.predict(X_test)
            mae, rmse, r2, y_pred_clipped = evaluate_forecast(y_test, y_pred)
            
            predictions_dict[name][h] = y_pred_clipped
            trained_models[f"{name}_h{h}"] = model
            
            model_filename = f"{name.lower()}_h{h}.joblib"
            joblib.dump(model, os.path.join(models_dir, model_filename))
            
            results.append({
                'Horizon': f"{h}-Week Ahead",
                'Horizon_Weeks': h,
                'Model': name,
                'MAE': round(mae, 3),
                'RMSE': round(rmse, 3),
                'R2_Score': round(r2, 4)
            })
            print(f"  [{name:14s}] MAE: {mae:6.2f} | RMSE: {rmse:6.2f} | R2: {r2:7.4f}")

    results_df = pd.DataFrame(results)
    results_csv_path = os.path.join(tables_dir, 'model_comparison_results.csv')
    results_df.to_csv(results_csv_path, index=False)
    print(f"\nMaster model comparison results saved to: {results_csv_path}")
    
    avg_mae = results_df[results_df['Model'] != 'Persistence'].groupby('Model')['MAE'].mean()
    best_model_name = avg_mae.idxmin()
    print(f"\nWinning Model Family: {best_model_name} (Lowest Avg MAE across horizons: {avg_mae[best_model_name]:.2f})")
    
    sns.set_theme(style='whitegrid', font='sans-serif')
    fig, axes = plt.subplots(4, 1, figsize=(14, 12), sharex=True)
    test_dates = pd.to_datetime(test_df['week_start_date'])
    
    for idx, h in enumerate(horizons):
        ax = axes[idx]
        y_true = test_df[f'target_h{h}'].values
        y_pred = predictions_dict[best_model_name][h]
        y_base = predictions_dict['Persistence'][h]
        
        ax.plot(test_dates, y_true, label='Actual Test Cases', color='black', linewidth=1.8)
        ax.plot(test_dates, y_pred, label=f'{best_model_name} Forecast', color='#d62728', linewidth=1.5, linestyle='-')
        ax.plot(test_dates, y_base, label='Persistence Baseline', color='#7f7f7f', linewidth=1.0, linestyle=':')
        
        h_metrics = results_df[(results_df['Horizon_Weeks'] == h) & (results_df['Model'] == best_model_name)].iloc[0]
        ax.set_title(f"Horizon {h}: {h}-Week Ahead Forecast (MAE: {h_metrics['MAE']}, RMSE: {h_metrics['RMSE']}, R²: {h_metrics['R2_Score']})", fontweight='bold')
        ax.set_ylabel('Cases / Week')
        ax.legend(loc='upper right', frameon=True)
        ax.set_ylim(0, max(y_true.max(), y_pred.max()) * 1.15)
        
    axes[-1].set_xlabel('Holdout Test Timeline (2004–2008)')
    plt.suptitle(f'Out-of-Time Multi-Horizon Dengue Forecasting: Actual vs. {best_model_name}', fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    
    plot_path = os.path.join(figures_dir, 'forecast_vs_actual_h1_to_h4.png')
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"Multi-horizon forecast plot saved to: {plot_path}")
    return results_df, best_model_name, trained_models


if __name__ == '__main__':
    run_multi_horizon_training()
