"""
data_loader.py - Data Synchronization, Sorting, and Time-Series Imputation Module
===================================================================================
Project: Explainable Short-Term Dengue Case Forecasting
Domain: Public Health Informatics & Epidemiological Time-Series Forecasting
"""

import os
import pandas as pd
import numpy as np

# Dynamically determine base directory (parent of src/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
DEFAULT_PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')


def load_raw_data(features_path: str, labels_path: str, city: str = 'sj') -> pd.DataFrame:
    if not os.path.exists(features_path):
        raise FileNotFoundError(f"Features file not found at: {features_path}")
    if not os.path.exists(labels_path):
        raise FileNotFoundError(f"Labels file not found at: {labels_path}")
        
    df_features = pd.read_csv(features_path)
    df_labels = pd.read_csv(labels_path)
    
    df_features = df_features[df_features['city'] == city].copy()
    df_labels = df_labels[df_labels['city'] == city].copy()
    
    df_merged = pd.merge(df_features, df_labels, on=['city', 'year', 'weekofyear'], how='inner')
    df_merged['week_start_date'] = pd.to_datetime(df_merged['week_start_date'])
    df_merged = df_merged.sort_values('week_start_date').reset_index(drop=True)
    return df_merged


def impute_timeseries_features(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()
    feature_cols = [col for col in df_clean.columns if col not in ['city', 'year', 'weekofyear', 'week_start_date', 'total_cases']]
    df_clean[feature_cols] = df_clean[feature_cols].ffill()
    df_clean[feature_cols] = df_clean[feature_cols].bfill()
    return df_clean


def verify_dataset_integrity(df: pd.DataFrame, expected_rows: int = 936):
    assert len(df) == expected_rows, f"Expected {expected_rows} rows, found {len(df)}"
    null_count = df.isnull().sum().sum()
    assert null_count == 0, f"Integrity failure: Found {null_count} missing values!"
    assert df['week_start_date'].is_monotonic_increasing, "Integrity failure: Dates are not strictly increasing!"
    assert (df['total_cases'] >= 0).all(), "Integrity failure: Negative dengue case counts found!"
    assert df['total_cases'].dtype == np.int64 or df['total_cases'].dtype == int, "Target is not integer!"
    print("Dataset integrity verified successfully:")
    print(f"  - Total records: {len(df)}")
    print(f"  - Total columns: {df.shape[1]}")
    print(f"  - Date range: {df['week_start_date'].min().strftime('%Y-%m-%d')} to {df['week_start_date'].max().strftime('%Y-%m-%d')}")
    print(f"  - Missing values: {null_count}")
    print(f"  - Total dengue cases recorded: {df['total_cases'].sum():,}")
    print(f"  - Weekly cases: min={df['total_cases'].min()}, median={df['total_cases'].median()}, max={df['total_cases'].max()}")


def process_and_save(raw_dir: str = DEFAULT_RAW_DIR,
                     processed_dir: str = DEFAULT_PROCESSED_DIR,
                     city: str = 'sj') -> pd.DataFrame:
    os.makedirs(processed_dir, exist_ok=True)
    feat_path = os.path.join(raw_dir, 'dengue_features_train.csv')
    labels_path = os.path.join(raw_dir, 'dengue_labels_train.csv')
    
    print(f"Loading and synchronizing raw data for city: '{city}'...")
    df_merged = load_raw_data(feat_path, labels_path, city=city)
    print(f"Raw merged shape: {df_merged.shape}")
    
    print("Applying causal time-series imputation (ffill + bfill)...")
    df_clean = impute_timeseries_features(df_merged)
    
    verify_dataset_integrity(df_clean, expected_rows=936 if city == 'sj' else 520)
    
    output_filename = f"{'san_juan' if city == 'sj' else 'iquitos'}_clean.csv"
    output_path = os.path.join(processed_dir, output_filename)
    df_clean.to_csv(output_path, index=False)
    print(f"Cleaned dataset saved successfully to: {output_path}")
    return df_clean


if __name__ == '__main__':
    process_and_save()
