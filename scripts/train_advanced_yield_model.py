# train_advanced_yield_model.py
# -*- coding: utf-8 -*-
# ============================================================
# Model: Advanced Yield Prediction (LightGBM + SHAP XAI)
# Algoritma: LightGBM Regressor (Gradient Boosting)
# Output: advanced_yield_model.pkl + shap_explainer.pkl
#
# DATASET PRIMER : yield_df.csv (FAO - 28.242 baris, 101 negara)
# DATASET FALLBACK: EDA_500.csv
#
# LightGBM lebih efisien untuk dataset besar dan menangani
# interaksi fitur non-linear secara lebih baik dari RandomForest.
# ============================================================

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import lightgbm as lgb
import shap
import joblib
import os

# ===== LANGKAH 1: PERSIAPAN =====
DATASET_PRIMARY   = 'yield_df.csv'
DATASET_FALLBACK  = 'EDA_500.csv'
MODEL_SAVE_PATH   = 'advanced_yield_model.pkl'
EXPLAINER_SAVE_PATH = 'shap_explainer.pkl'

def load_dataset():
    """Load FAO dataset jika ada, fallback ke EDA_500.csv"""
    if os.path.exists(DATASET_PRIMARY):
        df = pd.read_csv(DATASET_PRIMARY)
        if 'Unnamed: 0' in df.columns:
            df.drop('Unnamed: 0', axis=1, inplace=True)
        df['yield_kg_ha'] = df['hg/ha_yield'] / 100
        le = LabelEncoder()
        df['Item_encoded'] = le.fit_transform(df['Item'])
        FEATURES = ['average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp', 'Item_encoded', 'Year']
        TARGET = 'yield_kg_ha'
        df.dropna(subset=FEATURES + [TARGET], inplace=True)
        # Per-crop outlier removal
        cleaned = []
        for item in df['Item'].unique():
            sub = df[df['Item'] == item].copy()
            Q1, Q3 = sub[TARGET].quantile(0.05), sub[TARGET].quantile(0.95)
            cleaned.append(sub[(sub[TARGET] >= Q1) & (sub[TARGET] <= Q3)])
        df = pd.concat(cleaned)
        print(f"Dataset FAO: {len(df)} baris setelah cleaning")
        return df[FEATURES], df[TARGET], FEATURES, DATASET_PRIMARY
    else:
        df = pd.read_csv(DATASET_FALLBACK)
        FEATURES = ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Rainfall', 'pH']
        TARGET = 'Yield'
        df[TARGET] = pd.to_numeric(df[TARGET], errors='coerce')
        df.dropna(subset=[TARGET] + FEATURES, inplace=True)
        Q1, Q3 = df[TARGET].quantile(0.25), df[TARGET].quantile(0.75)
        IQR = Q3 - Q1
        df = df[(df[TARGET] >= Q1-1.5*IQR) & (df[TARGET] <= Q3+1.5*IQR)]
        print(f"Dataset Fallback EDA: {len(df)} baris")
        return df[FEATURES], df[TARGET], FEATURES, DATASET_FALLBACK

def train_advanced_model():
    """
    Melatih model LightGBM + SHAP explainer untuk yield prediction.
    Menggunakan yield_df.csv (FAO 28k baris) sebagai dataset utama.
    """

    if not os.path.exists(DATASET_PRIMARY) and not os.path.exists(DATASET_FALLBACK):
        print("[ERROR] Tidak ada dataset yang ditemukan.")
        return

    # ===== LANGKAH 2: MUAT & BERSIHKAN DATA =====
    X, y, FEATURES, dataset_used = load_dataset()
    print(f"Dataset: {dataset_used} | {len(X)} baris | Fitur: {FEATURES}")

    # ===== LANGKAH 3: BAGI DATA =====
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    # Untuk early stopping: buat validasi set dari training
    X_tr, X_val, y_tr, y_val = train_test_split(
        X_train, y_train, test_size=0.15, random_state=42
    )
    print(f"Training: {len(X_tr)} | Validasi: {len(X_val)} | Test: {len(X_test)}\n")

    # ===== LANGKAH 4: MODEL LGBM (Hyperparameter Dipilih dengan Tepat) =====
    # Parameter ini dipilih berdasarkan best practice untuk dataset pertanian kecil-menengah
    lgbm_model = lgb.LGBMRegressor(
        n_estimators=500,          # Banyak tree, dikontrol early stopping
        learning_rate=0.05,        # Lebih lambat = lebih akurat
        num_leaves=31,             # Default optimal untuk dataset sedang
        max_depth=-1,              # Auto depth
        min_child_samples=20,      # Cegah overfit pada data kecil
        subsample=0.8,             # 80% data per tree (regularisasi)
        colsample_bytree=0.8,      # 80% fitur per tree
        reg_alpha=0.1,             # L1 regularization
        reg_lambda=0.1,            # L2 regularization
        random_state=42,
        n_jobs=-1,
        verbose=-1                 # Suppress training logs
    )

    # ===== LANGKAH 5: CROSS-VALIDATION =====
    print("Menjalankan 5-Fold Cross-Validation...")
    # Gunakan model tanpa scaler untuk CV (LightGBM tidak butuh scaling)
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_r2 = cross_val_score(lgbm_model, X_train, y_train, cv=cv, scoring='r2')
    cv_mae = cross_val_score(lgbm_model, X_train, y_train, cv=cv,
                              scoring='neg_mean_absolute_error')

    print(f"CV R² per fold  : {np.round(cv_r2, 4)}")
    print(f"CV R² rata-rata : {cv_r2.mean():.4f} (+/- {cv_r2.std():.4f})")
    print(f"CV MAE rata-rata: {-cv_mae.mean():.2f} kg/ha\n")

    # ===== LANGKAH 6: LATIH MODEL FINAL DENGAN EARLY STOPPING =====
    print("Melatih model final dengan early stopping...")
    lgbm_model.fit(
        X_tr, y_tr,
        eval_set=[(X_val, y_val)],
        callbacks=[
            lgb.early_stopping(stopping_rounds=50, verbose=False),
            lgb.log_evaluation(period=100)
        ]
    )
    best_iter = lgbm_model.best_iteration_
    print(f"Iterasi terbaik (early stopping): {best_iter}\n")

    # ===== LANGKAH 7: EVALUASI =====
    predictions = lgbm_model.predict(X_test)
    r2   = r2_score(y_test, predictions)
    mae  = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))

    print(f"Evaluasi pada data test:")
    print(f"  R² Score : {r2:.4f}  (CV: {cv_r2.mean():.4f}) — Gap: {abs(r2 - cv_r2.mean()):.4f}")
    print(f"  MAE      : {mae:.2f} kg/ha")
    print(f"  RMSE     : {rmse:.2f} kg/ha\n")

    # Feature Importance LightGBM
    importances = lgbm_model.feature_importances_
    print("Feature Importance (LightGBM gain):")
    for fname, imp in sorted(zip(FEATURES, importances), key=lambda x: x[1], reverse=True):
        print(f"  {fname:12s}: {imp}")
    print()

    # ===== LANGKAH 8: SIMPAN MODEL =====
    joblib.dump(lgbm_model, MODEL_SAVE_PATH)
    print(f"[OK] LightGBM model disimpan sebagai '{MODEL_SAVE_PATH}'")

    # ===== LANGKAH 9: BUAT & SIMPAN SHAP EXPLAINER =====
    print("Membuat SHAP TreeExplainer...")
    explainer = shap.TreeExplainer(lgbm_model)

    # Verifikasi SHAP berjalan dengan benar pada sample
    shap_sample = X_test.head(10)
    shap_values = explainer.shap_values(shap_sample)
    print(f"SHAP values shape: {np.array(shap_values).shape} [OK]")

    joblib.dump(explainer, EXPLAINER_SAVE_PATH)
    print(f"[OK] SHAP explainer disimpan sebagai '{EXPLAINER_SAVE_PATH}'")

if __name__ == '__main__':
    train_advanced_model()
