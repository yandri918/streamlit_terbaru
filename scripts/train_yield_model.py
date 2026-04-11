# train_yield_model.py
# -*- coding: utf-8 -*-
# ============================================================
# Model: Yield Prediction (Prediksi Hasil Panen)
# Algoritma: Random Forest Regressor
# Output: yield_prediction_model.pkl
#
# DATASET: yield_df.csv (FAO Data - 28.242 baris)
# - 101 negara, 10 jenis tanaman, tahun 1990-2013
# - Fitur: average_rain_fall_mm_per_year, pesticides_tonnes, avg_temp
# - Target: hg/ha_yield (konversi ke kg/ha = bagi 100)
#
# Fallback: EDA_500.csv jika yield_df.csv tidak ada
# ============================================================

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib
import os

# ===== KONFIGURASI =====
DATASET_PRIMARY   = 'yield_df.csv'       # Dataset utama (FAO 28k baris)
DATASET_FALLBACK  = 'EDA_500.csv'        # Fallback jika primary tidak ada
MODEL_SAVE_PATH   = 'yield_prediction_model.pkl'

def load_and_prepare_fao_dataset(path):
    """Muat dan siapkan dataset FAO yield_df.csv"""
    print(f"Memuat dataset FAO: '{path}'...")
    df = pd.read_csv(path)

    # Drop kolom index redundan
    if 'Unnamed: 0' in df.columns:
        df.drop('Unnamed: 0', axis=1, inplace=True)

    print(f"Dataset awal: {df.shape[0]} baris, {df.shape[1]} kolom")
    print(f"Tanaman: {sorted(df['Item'].unique())}")
    print(f"Missing values: {df.isnull().sum().sum()} total")

    # Konversi yield dari hg/ha ke kg/ha (bagi 100)
    df['yield_kg_ha'] = df['hg/ha_yield'] / 100

    # Encode Item (jenis tanaman) sebagai fitur kategori → angka
    le = LabelEncoder()
    df['Item_encoded'] = le.fit_transform(df['Item'])

    # Simpan mapping untuk referensi
    print("\nMapping tanaman:")
    for code, name in enumerate(le.classes_):
        print(f"  {code}: {name}")

    # Fitur yang digunakan
    FEATURES = ['average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp', 'Item_encoded', 'Year']
    TARGET   = 'yield_kg_ha'

    df.dropna(subset=FEATURES + [TARGET], inplace=True)

    # Hapus outlier ekstrem (IQR per tanaman)
    before = len(df)
    cleaned_dfs = []
    for item in df['Item'].unique():
        sub = df[df['Item'] == item].copy()
        Q1 = sub[TARGET].quantile(0.05)
        Q3 = sub[TARGET].quantile(0.95)
        sub = sub[(sub[TARGET] >= Q1) & (sub[TARGET] <= Q3)]
        cleaned_dfs.append(sub)
    df = pd.concat(cleaned_dfs)
    print(f"\nSetelah hapus outlier: {len(df)} baris (dihapus: {before - len(df)})")

    X = df[FEATURES]
    y = df[TARGET]
    return X, y, FEATURES, le


def load_and_prepare_eda_dataset(path):
    """Muat dan siapkan dataset EDA_500.csv sebagai fallback"""
    print(f"Memuat dataset fallback: '{path}'...")
    df = pd.read_csv(path)
    FEATURES = ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Rainfall', 'pH']
    TARGET = 'Yield'

    df[TARGET] = pd.to_numeric(df[TARGET], errors='coerce')
    df.dropna(subset=[TARGET] + FEATURES, inplace=True)

    Q1, Q3 = df[TARGET].quantile(0.25), df[TARGET].quantile(0.75)
    IQR = Q3 - Q1
    df = df[(df[TARGET] >= Q1 - 1.5*IQR) & (df[TARGET] <= Q3 + 1.5*IQR)]
    print(f"Dataset bersih: {len(df)} baris")

    X = df[FEATURES]
    y = df[TARGET]
    return X, y, FEATURES, None


def train_yield_prediction_model():
    """
    Melatih model prediksi hasil panen.
    Prioritas: yield_df.csv (FAO 28k baris) -> EDA_500.csv (fallback)
    """

    # Pilih dataset
    if os.path.exists(DATASET_PRIMARY):
        X, y, features, label_encoder = load_and_prepare_fao_dataset(DATASET_PRIMARY)
        dataset_used = DATASET_PRIMARY
    elif os.path.exists(DATASET_FALLBACK):
        X, y, features, label_encoder = load_and_prepare_eda_dataset(DATASET_FALLBACK)
        dataset_used = DATASET_FALLBACK
    else:
        print(f"[ERROR] Tidak ada dataset yang ditemukan.")
        print("Download: https://www.kaggle.com/datasets/patelris/crop-yield-prediction-dataset")
        return

    print(f"\nDataset digunakan: {dataset_used}")
    print(f"Total sampel     : {len(X)}")
    print(f"Fitur            : {features}")
    print(f"\nStatistik Yield (kg/ha):")
    print(y.describe())
    print()

    # ===== SPLIT DATA =====
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"Training: {len(X_train)} | Testing: {len(X_test)}\n")

    # ===== PIPELINE =====
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('rf', RandomForestRegressor(
            n_estimators=200,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        ))
    ])

    # ===== CROSS-VALIDATION (5-FOLD) =====
    print("Menjalankan 5-Fold Cross-Validation...")
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_r2  = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring='r2')
    cv_mae = cross_val_score(pipeline, X_train, y_train, cv=cv,
                              scoring='neg_mean_absolute_error')

    print(f"CV R2  per fold  : {np.round(cv_r2, 4)}")
    print(f"CV R2  rata-rata : {cv_r2.mean():.4f} (+/- {cv_r2.std():.4f})")
    print(f"CV MAE rata-rata : {-cv_mae.mean():.2f} kg/ha\n")

    # ===== LATIH MODEL FINAL =====
    print("Melatih model final...")
    pipeline.fit(X_train, y_train)
    print("Selesai.\n")

    # ===== EVALUASI =====
    predictions = pipeline.predict(X_test)
    r2   = r2_score(y_test, predictions)
    mae  = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))

    print("Evaluasi pada data test:")
    print(f"  R2 Score : {r2:.4f}  (CV: {cv_r2.mean():.4f})  Gap: {abs(r2-cv_r2.mean()):.4f}")
    print(f"  MAE      : {mae:.2f} kg/ha")
    print(f"  RMSE     : {rmse:.2f} kg/ha\n")

    # Feature Importance
    rf = pipeline.named_steps['rf']
    importances = rf.feature_importances_
    print("Feature Importance:")
    for fname, imp in sorted(zip(features, importances), key=lambda x: x[1], reverse=True):
        bar = '|' * int(imp * 50)
        print(f"  {fname:35s}: {imp:.4f} {bar}")
    print()

    # ===== SIMPAN =====
    # Simpan pipeline + metadata
    model_data = {
        'pipeline': pipeline,
        'features': features,
        'dataset': dataset_used,
        'label_encoder': label_encoder,  # None jika pakai EDA_500
        'metrics': {
            'cv_r2_mean': cv_r2.mean(),
            'cv_r2_std': cv_r2.std(),
            'test_r2': r2,
            'test_mae': mae,
            'test_rmse': rmse
        }
    }
    joblib.dump(model_data, MODEL_SAVE_PATH)
    print(f"[OK] Model + metadata disimpan sebagai '{MODEL_SAVE_PATH}'")
    print(f"     Dataset: {dataset_used} | R2: {r2:.4f} | MAE: {mae:.2f} kg/ha")


if __name__ == '__main__':
    train_yield_prediction_model()
