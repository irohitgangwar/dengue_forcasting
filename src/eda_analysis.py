"""
eda_analysis.py - Exploratory Data Analysis & Biological Visualization Module
==============================================================================
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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'san_juan_clean.csv')
DEFAULT_FIGURES_DIR = os.path.join(BASE_DIR, 'figures')


def setup_plotting_style():
    sns.set_theme(style='whitegrid', font='sans-serif')
    plt.rcParams.update({
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.titlesize': 13,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 14,
        'figure.dpi': 300
    })


def plot_case_timeline(df: pd.DataFrame, output_path: str):
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(df['week_start_date'], df['total_cases'], color='#1f77b4', linewidth=1.2, label='Weekly Dengue Cases')
    ax.axhline(df['total_cases'].median(), color='#2ca02c', linestyle='--', linewidth=1.2, label=f'Median Baseline ({df["total_cases"].median():.0f} cases)')
    ax.axhline(df['total_cases'].mean(), color='#ff7f0e', linestyle=':', linewidth=1.2, label=f'Mean Level ({df["total_cases"].mean():.1f} cases)')
    
    peak_1994 = df.loc[df['total_cases'].idxmax()]
    ax.annotate(f"Major Epidemic Peak: {peak_1994['total_cases']} cases\n(Week {peak_1994['weekofyear']}, {peak_1994['year']})",
                xy=(peak_1994['week_start_date'], peak_1994['total_cases']),
                xytext=(peak_1994['week_start_date'] + pd.Timedelta(days=200), peak_1994['total_cases'] - 50),
                arrowprops=dict(facecolor='#d62728', shrink=0.05, width=1.5, headwidth=8),
                fontsize=9, fontweight='bold', color='#d62728',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffe6e6', edgecolor='#d62728', alpha=0.9))

    peak_1998 = df[df['year'] == 1998].sort_values('total_cases', ascending=False).iloc[0]
    ax.annotate(f"1998 Outbreak: {peak_1998['total_cases']} cases\n(Week {peak_1998['weekofyear']})",
                xy=(peak_1998['week_start_date'], peak_1998['total_cases']),
                xytext=(peak_1998['week_start_date'] - pd.Timedelta(days=600), peak_1998['total_cases'] + 20),
                arrowprops=dict(facecolor='#d62728', shrink=0.05, width=1.5, headwidth=8),
                fontsize=9, fontweight='bold', color='#d62728',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffe6e6', edgecolor='#d62728', alpha=0.9))

    ax.set_title('18-Year Weekly Dengue Caseloads in San Juan, Puerto Rico (1990–2008)', fontweight='bold', pad=12)
    ax.set_xlabel('Timeline (Epidemiological Date)')
    ax.set_ylabel('Reported Cases per Week')
    ax.set_ylim(0, 500)
    ax.legend(loc='upper right', frameon=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved: {output_path}")


def plot_seasonal_cycle(df: pd.DataFrame, output_path: str):
    seasonal_stats = df.groupby('weekofyear')['total_cases'].agg(['mean', 'std', 'median', lambda x: x.quantile(0.75), lambda x: x.quantile(0.25)]).reset_index()
    seasonal_stats.columns = ['weekofyear', 'mean', 'std', 'median', 'q75', 'q25']
    
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(seasonal_stats['weekofyear'], seasonal_stats['mean'], color='#1f77b4', linewidth=2.5, label='Weekly Mean Cases')
    ax.plot(seasonal_stats['weekofyear'], seasonal_stats['median'], color='#2ca02c', linewidth=2.0, linestyle='--', label='Weekly Median Cases')
    ax.fill_between(seasonal_stats['weekofyear'], seasonal_stats['q25'], seasonal_stats['q75'],
                    color='#1f77b4', alpha=0.2, label='Interquartile Range (25th–75th Percentile)')
    ax.axvspan(34, 46, color='#ff7f0e', alpha=0.15, label='High Epidemic Transmission Window (Weeks 34–46)')
    
    ax.set_title('Annual Dengue Transmission Seasonality in San Juan (Aggregated 1990–2008)', fontweight='bold', pad=12)
    ax.set_xlabel('Epidemiological Week of Year (1 to 53)')
    ax.set_ylabel('Dengue Cases')
    ax.set_xlim(1, 53)
    ax.set_xticks(range(1, 54, 4))
    ax.legend(loc='upper left', frameon=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved: {output_path}")


def plot_weather_correlation(df: pd.DataFrame, output_path: str):
    feature_mapping = {
        'total_cases': 'Dengue Cases',
        'reanalysis_specific_humidity_g_per_kg': 'Specific Humidity (g/kg)',
        'reanalysis_dew_point_temp_k': 'Dew Point Temp (K)',
        'station_min_temp_c': 'Station Min Temp (°C)',
        'station_avg_temp_c': 'Station Avg Temp (°C)',
        'reanalysis_air_temp_k': 'Air Temp (K)',
        'reanalysis_relative_humidity_percent': 'Relative Humidity (%)',
        'station_precip_mm': 'Station Precip (mm)',
        'precipitation_amt_mm': 'Satellite Precip (mm)',
        'ndvi_se': 'Vegetation NDVI (SE)'
    }
    corr_df = df[list(feature_mapping.keys())].rename(columns=feature_mapping).corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_df, annot=True, fmt='.2f', cmap='coolwarm', cbar_kws={'label': 'Pearson Correlation (r)'},
                vmin=-0.4, vmax=1.0, linewidths=0.5, ax=ax)
    ax.set_title('Correlation Matrix: Dengue Cases vs. Concurrent Meteorological Indicators', fontweight='bold', pad=14)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved: {output_path}")


def plot_lagged_cross_correlation(df: pd.DataFrame, output_path: str):
    max_lag = 12
    lags = list(range(0, max_lag + 1))
    weather_vars = {
        'reanalysis_specific_humidity_g_per_kg': ('Specific Humidity', '#1f77b4', 'o'),
        'reanalysis_dew_point_temp_k': ('Dew Point Temp', '#ff7f0e', 's'),
        'station_min_temp_c': ('Station Min Temp', '#2ca02c', '^'),
        'precipitation_amt_mm': ('Precipitation', '#d62728', 'D')
    }
    
    fig, ax = plt.subplots(figsize=(11, 5.5))
    for col, (label, color, marker) in weather_vars.items():
        corrs = []
        for lag in lags:
            lagged_weather = df[col].shift(lag)
            r = df['total_cases'].corr(lagged_weather)
            corrs.append(r)
        ax.plot(lags, corrs, label=label, color=color, marker=marker, linewidth=2, markersize=6)
        max_idx = np.argmax(corrs)
        ax.scatter([lags[max_idx]], [corrs[max_idx]], color=color, s=120, edgecolors='black', zorder=5)

    ax.axvline(0, color='gray', linestyle=':', label='Concurrent Weather (Lag 0)')
    ax.axvspan(2, 8, color='yellow', alpha=0.15, label='Biological Delay Window (Lags 2–8 Weeks)')
    ax.set_title('Lagged Cross-Correlation: Weather Preceding Dengue Cases by 0 to 12 Weeks', fontweight='bold', pad=12)
    ax.set_xlabel('Lag Time in Weeks (Weather Conditions k Weeks Prior to Dengue Count)')
    ax.set_ylabel('Pearson Correlation Coefficient (r)')
    ax.set_xticks(lags)
    ax.legend(loc='lower left', frameon=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved: {output_path}")


def run_eda(processed_data_path: str = DEFAULT_DATA_PATH,
            figures_dir: str = DEFAULT_FIGURES_DIR):
    os.makedirs(figures_dir, exist_ok=True)
    setup_plotting_style()
    print(f"Loading cleaned data from: {processed_data_path}...")
    df = pd.read_csv(processed_data_path)
    df['week_start_date'] = pd.to_datetime(df['week_start_date'])
    
    print("Generating Figure 1: Case timeline...")
    plot_case_timeline(df, os.path.join(figures_dir, 'eda_case_timeline.png'))
    print("Generating Figure 2: Annual seasonality cycle...")
    plot_seasonal_cycle(df, os.path.join(figures_dir, 'eda_seasonal_cycle.png'))
    print("Generating Figure 3: Weather correlation heatmap...")
    plot_weather_correlation(df, os.path.join(figures_dir, 'eda_weather_correlation.png'))
    print("Generating Figure 4: Lagged cross-correlation proof...")
    plot_lagged_cross_correlation(df, os.path.join(figures_dir, 'eda_lagged_cross_correlation.png'))
    print("All 4 EDA figures generated successfully!")


if __name__ == '__main__':
    run_eda()
