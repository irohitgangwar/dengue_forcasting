"""
models.py - Model Architectures & Baseline Definitions
======================================================
Project: Explainable Short-Term Dengue Case Forecasting
Domain: Public Health Informatics & Machine Learning

Defines:
1. PersistenceBaseline: Simple naive benchmark (y_{t+h} = y_t).
2. RandomForestRegressor: Bootstrap ensemble of decision trees.
3. XGBRegressor: Extreme Gradient Boosting.
4. LGBMRegressor: Light Gradient Boosting Machine.
"""

import numpy as np
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
import lightgbm as lgb


class PersistenceBaseline:
    """
    Persistence / Naïve forecasting baseline:
    Predicts that future dengue cases will equal the most recently observed week's cases (cases_lag1).
    """
    def __init__(self):
        self.fitted_ = True
        
    def fit(self, X, y):
        # Persistence has no parameters to learn
        return self
        
    def predict(self, X):
        # X must contain 'cases_lag1'
        if 'cases_lag1' in X.columns:
            return np.maximum(0, X['cases_lag1'].values)
        else:
            raise KeyError("Feature 'cases_lag1' required for persistence baseline!")


def get_model(model_name: str, random_state: int = 42):
    """
    Factory function returning a configured regressor model.
    """
    name = model_name.lower()
    if name == 'persistence':
        return PersistenceBaseline()
    elif name == 'random_forest':
        return RandomForestRegressor(
            n_estimators=100,
            max_depth=8,
            min_samples_split=4,
            min_samples_leaf=2,
            random_state=random_state,
            n_jobs=-1
        )
    elif name == 'xgboost':
        return xgb.XGBRegressor(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=random_state,
            verbosity=0
        )
    elif name == 'lightgbm':
        return lgb.LGBMRegressor(
            n_estimators=100,
            max_depth=5,
            num_leaves=20,
            learning_rate=0.05,
            subsample=0.8,
            random_state=random_state,
            verbose=-1,
            n_jobs=-1
        )
    else:
        raise ValueError(f"Unknown model name: {model_name}")

