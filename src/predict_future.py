"""
predict_future.py - Forward Out-of-Sample Prediction Module
============================================================
Project: Explainable Short-Term Dengue Case Forecasting
"""

import os
import pandas as pd
import numpy as np
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_RAW_TEST = os.path.join(BASE_DIR, 'data', 'raw', 'dengue_features_test.csv')
DEFAULT_CLEAN_TRAIN = os.path.join(BASE_DIR, 'data', 'processed', 'san_juan_clean.csv')
DEFAULT_MODELS_DIR = os.path.join(BASE_DIR, 'models')
DEFAULT_OUTPUT_PATH = os.path.join(BASE_DIR, 'tables', 'future_dengue_forecasts_2008_2013.csv')


def generate_future_forecasts(raw_test_path: str = DEFAULT_RAW_TEST,
                              clean_train_path: str = DEFAULT_CLEAN_TRAIN,
                              models_dir: str = DEFAULT_MODELS_DIR,
                              output_path: str = DEFAULT_OUTPUT_PATH):
    print(f"Loading raw future test features from: {raw_test_path}...")
    df_raw_test = pd.read_csv(raw_test_path)
    sj_test = df_raw_test[df_raw_test['city'] == 'sj'].copy().reset_index(drop=True)
    sj_test['week_start_date'] = pd.to_datetime(sj_test['week_start_date'])
    sj_test = sj_test.sort_values('week_start_date').reset_index(drop=True)
    
    df_train = pd.read_csv(clean_train_path)
    df_train['week_start_date'] = pd.to_datetime(df_train['week_start_date'])
    df_train = df_train.sort_values('week_start_date').reset_index(drop=True)
    
    feature_cols = [c for c in sj_test.columns if c not in ['city', 'year', 'weekofyear', 'week_start_date']]
    sj_test[feature_cols] = sj_test[feature_cols].ffill().bfill()
    
    last_train_tail = df_train.tail(8).copy()
    recent_case_level = last_train_tail['total_cases'].mean()
    
    sj_test['cases_lag1'] = recent_case_level
    for lag in [2, 3, 4, 8]:
        sj_test[f'cases_lag{lag}'] = recent_case_level
    
    sj_test['cases_roll_mean_4'] = recent_case_level
    sj_test['cases_roll_std_4'] = 5.0
    sj_test['cases_roll_mean_8'] = recent_case_level
    sj_test['cases_roll_std_8'] = 6.0
    sj_test['cases_trend_4'] = 0.0
    sj_test['cases_ratio_4'] = 1.0
    
    weeks_in_year = 52.1775
    sj_test['sin_week'] = np.sin(2 * np.pi * sj_test['weekofyear'] / weeks_in_year)
    sj_test['cos_week'] = np.cos(2 * np.pi * sj_test['weekofyear'] / weeks_in_year)
    sj_test['month'] = sj_test['week_start_date'].dt.month
    
    key_vars = ['reanalysis_specific_humidity_g_per_kg', 'reanalysis_dew_point_temp_k', 'station_min_temp_c', 'precipitation_amt_mm']
    for var in key_vars:
        for lag in [1, 2, 3, 4, 6, 8]:
            sj_test[f"{var}_lag{lag}"] = sj_test[var].shift(lag).ffill().bfill()
            
    sj_test['precip_roll_sum_4'] = sj_test['precipitation_amt_mm'].rolling(window=4).sum().ffill().bfill()
    sj_test['humidity_roll_mean_4'] = sj_test['reanalysis_specific_humidity_g_per_kg'].rolling(window=4).mean().ffill().bfill()
    sj_test['temp_min_roll_mean_4'] = sj_test['station_min_temp_c'].rolling(window=4).mean().ffill().bfill()
    
    forecast_df = sj_test[['city', 'year', 'weekofyear', 'week_start_date']].copy()
    
    train_split_path = os.path.join(BASE_DIR, 'data', 'processed', 'train_split.csv')
    train_cols = pd.read_csv(train_split_path, nrows=2).columns.tolist()
    ignore = ['city', 'year', 'weekofyear', 'week_start_date', 'total_cases', 'target_h1', 'target_h2', 'target_h3', 'target_h4']
    model_features = [c for c in train_cols if c not in ignore]
    
    for h in [1, 2, 3, 4]:
        model_file = os.path.join(models_dir, f"xgboost_h{h}.joblib")
        if os.path.exists(model_file):
            model = joblib.load(model_file)
            X_future = sj_test[model_features].copy()
            preds = np.maximum(0, model.predict(X_future))
            forecast_df[f'predicted_cases_h{h}'] = np.round(preds).astype(int)
            print(f"Generated Horizon {h} predictions for {len(forecast_df)} weeks (Mean: {preds.mean():.1f}, Max: {preds.max():.0f})")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    forecast_df.to_csv(output_path, index=False)
    print(f"Future out-of-sample forecasts saved to: {output_path}")
    return forecast_df


if __name__ == '__main__':
    generate_future_forecasts()
