import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib
import os

# =============================================================================
# 🛠️ AGRI-SENSA DUMMY MODEL GENERATOR (V2)
# Produces more realistic dummy models for development/demo when real 
# datasets are unavailable. 
# Matches the Pipeline structure used in production.
# =============================================================================

def generate_bwd_dummy():
    """1. BWD Model Dummy (1 feature: avg_hue)"""
    print("Generating BWD Dummy Model...")
    np.random.seed(42)
    X = np.random.uniform(30, 90, size=(500, 1))
    # Synthetic logic: hue between 45-75 is likely diseased (BWD=1)
    y = ((X[:, 0] > 45) & (X[:, 0] < 75)).astype(int)
    
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('dt', DecisionTreeClassifier(max_depth=5, random_state=42))
    ])
    pipeline.fit(X, y)
    joblib.dump(pipeline, 'bwd_model.pkl')
    print("  - Saved: bwd_model.pkl")

def generate_recommendation_dummy():
    """2. Generic NPK Recommendation Model Dummy (4 features)"""
    print("Generating Recommendation Dummy Model...")
    np.random.seed(42)
    # Features: pH, BWD_Score, Humidity, Plant_Age_Days
    X = np.random.rand(500, 4)
    X[:, 0] = X[:, 0] * 3 + 5.0     # pH: 5-8
    X[:, 1] = np.random.choice([0, 1], 500) # BWD
    X[:, 2] = X[:, 2] * 60 + 40    # Humidity: 40-100
    X[:, 3] = X[:, 3] * 120        # Age: 0-120 days
    
    # Target: N, P, K output
    y_n = (X[:, 0] * 20) + (X[:, 2] * 0.5)
    y_p = (X[:, 3] * 0.4) + 20
    y_k = (X[:, 0] * 15) + 30
    y = np.column_stack([y_n, y_p, y_k])
    
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('rf', RandomForestRegressor(n_estimators=50, random_state=42))
    ])
    pipeline.fit(X, y)
    joblib.dump(pipeline, 'recommendation_model.pkl')
    print("  - Saved: recommendation_model.pkl")

def generate_crop_dummy():
    """3. Crop Recommendation Model Dummy (7 features)"""
    print("Generating Crop Recommendation Dummy Model...")
    np.random.seed(42)
    # Features: N, P, K, Temp, Humidity, pH, Rainfall
    X = np.random.rand(500, 7)
    X[:, 0] *= 300; X[:, 1] *= 100; X[:, 2] *= 200 # NPK
    X[:, 3] = X[:, 3] * 20 + 15  # Temp: 15-35
    X[:, 4] = X[:, 4] * 50 + 50  # Hum: 50-100
    X[:, 5] = X[:, 5] * 3 + 4    # pH: 4-7
    X[:, 6] *= 3000              # Rain
    
    crops = ['Rice', 'Maize', 'Soybean', 'Potato', 'Cassava']
    y = np.random.choice(crops, 500)
    
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('rf', RandomForestClassifier(n_estimators=50, random_state=42))
    ])
    pipeline.fit(X, y)
    joblib.dump(pipeline, 'crop_recommendation_model.pkl')
    print("  - Saved: crop_recommendation_model.pkl")

def run_all():
    print("Starting Dummy Model Generation...")
    generate_bwd_dummy()
    generate_recommendation_dummy()
    generate_crop_dummy()
    print("\n[OK] All dummy models generated successfully.")

if __name__ == '__main__':
    run_all()
