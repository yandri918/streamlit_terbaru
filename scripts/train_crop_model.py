# train_crop_model.py
# ============================================================
# Model: Crop Recommendation Classifier
# Algoritma: Random Forest Classifier
# Output: crop_recommendation_model.pkl
# -*- coding: utf-8 -*-
#
# DATASET YANG DIPERLUKAN: Crop_recommendation.csv
# - 2200 baris, 7 fitur, 22 kelas tanaman
# - Sumber: https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset
# - Kolom: N, P, K, temperature, humidity, ph, rainfall, label
#
# CATATAN: File ini MENGGANTIKAN train_recommendation_model.py yang identik.
# ============================================================

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# ===== LANGKAH 1: PERSIAPAN =====
DATASET_PATH = 'Crop_recommendation.csv'
MODEL_SAVE_PATH = 'crop_recommendation_model.pkl'

def train_crop_recommendation_model():
    """
    Fungsi untuk melatih model klasifikasi rekomendasi tanaman.
    PERBAIKAN:
    - Gunakan Pipeline dengan StandardScaler untuk konsistensi
    - Tambah 5-Fold Stratified Cross-Validation
    - Tambah classification_report + top feature importance
    - Tambah info distribusi kelas
    """

    # Cek dataset tersedia
    if not os.path.exists(DATASET_PATH):
        print(f"[ERROR] File dataset '{DATASET_PATH}' tidak ditemukan.")
        print("Download dari:")
        print("  https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset")
        print("  -> Simpan sebagai 'Crop_recommendation.csv' di folder yang sama")
        return

    # ===== LANGKAH 2: MUAT DATASET =====
    print(f"Memuat dataset dari '{DATASET_PATH}'...")
    dataset = pd.read_csv(DATASET_PATH)
    print(f"Dataset: {dataset.shape[0]} baris, {dataset.shape[1]} kolom")
    print(f"Jumlah kelas tanaman: {dataset['label'].nunique()}")
    print(f"Kelas: {sorted(dataset['label'].unique())}\n")

    # Pisahkan fitur dan target
    X = dataset.drop('label', axis=1)
    y = dataset['label']

    # Cek missing values
    if X.isnull().sum().any():
        print("[WARNING] Ditemukan missing values - melakukan drop baris NaN...")
        dataset.dropna(inplace=True)
        X = dataset.drop('label', axis=1)
        y = dataset['label']

    # ===== LANGKAH 3: BAGI DATA =====
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y  # Jaga proporsi setiap kelas tanaman
    )
    print(f"Data training: {len(X_train)} | Data testing: {len(X_test)}\n")

    # ===== LANGKAH 4: BUAT PIPELINE =====
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('rf', RandomForestClassifier(
            n_estimators=200,        # Lebih banyak tree = lebih stabil
            max_depth=None,          # Biarkan pohon tumbuh optimal
            min_samples_split=2,
            random_state=42,
            n_jobs=-1                # Pakai semua core CPU
        ))
    ])

    # ===== LANGKAH 5: CROSS-VALIDATION =====
    print("Menjalankan 5-Fold Stratified Cross-Validation...")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring='accuracy')

    print(f"CV Accuracy per fold : {np.round(cv_scores * 100, 2)}")
    print(f"CV Accuracy rata-rata: {cv_scores.mean() * 100:.2f}% (+/- {cv_scores.std() * 100:.2f}%)\n")

    # ===== LANGKAH 6: LATIH MODEL FINAL =====
    print("Melatih model final...")
    pipeline.fit(X_train, y_train)
    print("Selesai.\n")

    # ===== LANGKAH 7: EVALUASI =====
    predictions = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print(f"Akurasi pada data test: {accuracy * 100:.2f}%")
    print(f"Gap dengan CV score   : {abs(accuracy - cv_scores.mean()) * 100:.2f}% (idealnya < 5%)\n")

    print("Classification Report:")
    print(classification_report(y_test, predictions))

    # Feature importance dari RandomForest (tanpa scaler step)
    rf_model = pipeline.named_steps['rf']
    feature_names = X.columns.tolist()
    importances = rf_model.feature_importances_
    sorted_idx = np.argsort(importances)[::-1]

    print("Top Feature Importance:")
    for i in sorted_idx:
        print(f"  {feature_names[i]:12s}: {importances[i]:.4f}")
    print()

    # ===== LANGKAH 8: SIMPAN MODEL =====
    joblib.dump(pipeline, MODEL_SAVE_PATH)
    print(f"[OK] Model Pipeline disimpan sebagai '{MODEL_SAVE_PATH}'")

if __name__ == '__main__':
    train_crop_recommendation_model()
