"""
split_data.py - Strict Chronological Train-Test Partitioning Module
===================================================================
Project: Explainable Short-Term Dengue Case Forecasting
"""

import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_INPUT_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'san_juan_engineered.csv')
DEFAULT_PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')


def perform_chronological_split(input_path: str = DEFAULT_INPUT_PATH,
                                processed_dir: str = DEFAULT_PROCESSED_DIR,
                                train_ratio: float = 0.80):
    print(f"Loading engineered dataset from: {input_path}...")
    df = pd.read_csv(input_path)
    df['week_start_date'] = pd.to_datetime(df['week_start_date'])
    df = df.sort_values('week_start_date').reset_index(drop=True)
    
    n_total = len(df)
    n_train = int(n_total * train_ratio)
    
    train_df = df.iloc[:n_train].copy().reset_index(drop=True)
    test_df = df.iloc[n_train:].copy().reset_index(drop=True)
    
    assert len(train_df) + len(test_df) == n_total, "Partition row sum mismatch!"
    assert train_df['week_start_date'].max() < test_df['week_start_date'].min(), "Chronological breach: Train dates overlap test dates!"
    
    train_path = os.path.join(processed_dir, 'train_split.csv')
    test_path = os.path.join(processed_dir, 'test_split.csv')
    
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    
    print("Chronological train-test split completed successfully:")
    print(f"  - Training records: {len(train_df)} ({len(train_df)/n_total:.1%}) | Dates: {train_df['week_start_date'].min().strftime('%Y-%m-%d')} to {train_df['week_start_date'].max().strftime('%Y-%m-%d')}")
    print(f"  - Testing records:  {len(test_df)} ({len(test_df)/n_total:.1%}) | Dates: {test_df['week_start_date'].min().strftime('%Y-%m-%d')} to {test_df['week_start_date'].max().strftime('%Y-%m-%d')}")
    print(f"  - Saved to: {train_path} and {test_path}")
    return train_df, test_df


if __name__ == '__main__':
    perform_chronological_split()
