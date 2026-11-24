"""
feature_engineering.py - Systematic Feature Engineering & Multi-Horizon Targets
================================================================================
Project: Explainable Short-Term Dengue Case Forecasting
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_INPUT_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'san_juan_clean.csv')
DEFAULT_OUTPUT_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'san_juan_engineered.csv')


def build_engineered_features(df_clean: pd.DataFrame) -> pd.DataFrame:
    df = df_clean.copy()
    df['week_start_date'] = pd.to_datetime(df['week_start_date'])
    df = df.sort_values('week_start_date').reset_index(drop=True)
    
    # 1. Autoregressive Dengue Case Lags
    case_series = df['total_cases']
    df['cases_lag1'] = case_series
    df['cases_lag2'] = case_series.shift(1)
    df['cases_lag3'] = case_series.shift(2)
    df['cases_lag4'] = case_series.shift(3)
    df['cases_lag8'] = case_series.shift(7)
    
    # 2. Moving Window Statistics
    df['cases_roll_mean_4'] = case_series.rolling(window=4).mean()
    df['cases_roll_std_4'] = case_series.rolling(window=4).std().fillna(0)
    df['cases_roll_mean_8'] = case_series.rolling(window=8).mean()
    df['cases_roll_std_8'] = case_series.rolling(window=8).std().fillna(0)
    df['cases_trend_4'] = df['cases_lag1'] - df['cases_roll_mean_4']
    df['cases_ratio_4'] = (df['cases_lag1'] + 1.0) / (df['cases_roll_mean_4'] + 1.0)
    
    # 3. Cyclical Seasonal Encodings
    weeks_in_year = 52.1775
    df['sin_week'] = np.sin(2 * np.pi * df['weekofyear'] / weeks_in_year)
    df['cos_week'] = np.cos(2 * np.pi * df['weekofyear'] / weeks_in_year)
    df['month'] = df['week_start_date'].dt.month
    
    # 4. Biologically Lagged Weather Variables
    key_weather_vars = [
        'reanalysis_specific_humidity_g_per_kg',
        'reanalysis_dew_point_temp_k',
        'station_min_temp_c',
        'precipitation_amt_mm'
    ]
    lags = [1, 2, 3, 4, 6, 8]
    for var in key_weather_vars:
        for lag in lags:
            df[f"{var}_lag{lag}"] = df[var].shift(lag)
            
    # 5. Cumulative Weather Encodings
    df['precip_roll_sum_4'] = df['precipitation_amt_mm'].rolling(window=4).sum()
    df['humidity_roll_mean_4'] = df['reanalysis_specific_humidity_g_per_kg'].rolling(window=4).mean()
    df['temp_min_roll_mean_4'] = df['station_min_temp_c'].rolling(window=4).mean()
    
    # 6. Multi-Horizon Forward Targets
    df['target_h1'] = df['total_cases'].shift(-1)
    df['target_h2'] = df['total_cases'].shift(-2)
    df['target_h3'] = df['total_cases'].shift(-3)
    df['target_h4'] = df['total_cases'].shift(-4)
    
    df_engineered = df.dropna().reset_index(drop=True)
    return df_engineered


def verify_feature_matrix(df_eng: pd.DataFrame):
    assert df_eng.isnull().sum().sum() == 0, "Engineered dataset contains missing values!"
    targets = ['target_h1', 'target_h2', 'target_h3', 'target_h4']
    for t in targets:
        assert t in df_eng.columns, f"Target {t} missing!"
        assert (df_eng[t] >= 0).all(), f"Target {t} has negative values!"
    assert df_eng['week_start_date'].is_monotonic_increasing, "Dates are not monotonic!"
    print("Feature matrix successfully validated:")
    print(f"  - Total usable rows: {len(df_eng)} weeks (~17.8 continuous years)")
    print(f"  - Total columns: {df_eng.shape[1]}")
    print(f"  - Start date: {df_eng['week_start_date'].min().strftime('%Y-%m-%d')}")
    print(f"  - End date: {df_eng['week_start_date'].max().strftime('%Y-%m-%d')}")
    print(f"  - Targets created: {targets}")
    print(f"  - Target H1 mean={df_eng['target_h1'].mean():.2f}, max={df_eng['target_h1'].max():.0f}")


def run_feature_engineering(input_path: str = DEFAULT_INPUT_PATH,
                            output_path: str = DEFAULT_OUTPUT_PATH) -> pd.DataFrame:
    print(f"Loading cleaned dataset from: {input_path}...")
    df_clean = pd.read_csv(input_path)
    print("Constructing case lags, weather lags, rolling windows, and multi-horizon targets...")
    df_eng = build_engineered_features(df_clean)
    verify_feature_matrix(df_eng)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_eng.to_csv(output_path, index=False)
    print(f"Engineered dataset saved successfully to: {output_path}")
    return df_eng


if __name__ == '__main__':
    run_feature_engineering()
