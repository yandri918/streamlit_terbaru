# train_success_model.py
# -*- coding: utf-8 -*-
# ============================================================
# Model: Success Prediction (Prediksi Keberhasilan Panen)
# Algoritma: Logistic Regression (Klasifikasi Biner)
# Output: success_model.pkl
#
# DATASET PRIMER : yield_df.csv (FAO - 28.242 baris)
# DATASET FALLBACK: EDA_500.csv
#
# Target dibuat otomatis: Yield > Median -> Success = 1
# ============================================================

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, classification_report,
    confusion_matrix, roc_auc_score
)
import joblib
import os

# ===== KONFIGURASI =====
DATASET_PRIMARY  = 'yield_df.csv'
DATASET_FALLBACK = 'EDA_500.csv'
MODEL_SAVE_PATH  = 'success_model.pkl'

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
        TARGET = 'Success'
        
        # Feature Engineering: Success biner per jenis tanaman
        df['Success'] = 0
        for item in df['Item'].unique():
            mask = df['Item'] == item
            median_yield = df.loc[mask, 'yield_kg_ha'].median()
            df.loc[mask, 'Success'] = (df.loc[mask, 'yield_kg_ha'] > median_yield).astype(int)
        
        df.dropna(subset=FEATURES + [TARGET], inplace=True)
        print(f"Dataset FAO Success: {len(df)} baris")
        return df[FEATURES], df[TARGET], FEATURES, DATASET_PRIMARY
    else:
        df = pd.read_csv(DATASET_FALLBACK)
        FEATURES = ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Rainfall', 'pH']
        TARGET = 'Success'
        df['Yield'] = pd.to_numeric(df['Yield'], errors='coerce')
        df.dropna(subset=['Yield'] + FEATURES, inplace=True)
        yield_median = df['Yield'].median()
        df['Success'] = (df['Yield'] > yield_median).astype(int)
        print(f"Dataset Fallback EDA Success: {len(df)} baris")
        return df[FEATURES], df[TARGET], FEATURES, DATASET_FALLBACK

def train_success_prediction_model():
    """
    Fungsi untuk melatih model prediksi keberhasilan panen (biner: Gagal/Berhasil).
    PERBAIKAN:
    - Tambah StandardScaler via Pipeline (PENTING untuk Logistic Regression)
    - Tambah 5-Fold Stratified Cross-Validation
    - Tambah ROC-AUC score (metrik yang lebih baik untuk klasifikasi biner)
    - Tambah confusion matrix
    - Tambah threshold analysis
    """

    if not os.path.exists(DATASET_PRIMARY) and not os.path.exists(DATASET_FALLBACK):
        print("[ERROR] Tidak ada dataset yang ditemukan.")
        return

    # ===== LANGKAH 2: MUAT & REKAYASA FITUR =====
    X, y, FEATURES, dataset_used = load_dataset()
    print(f"Dataset: {dataset_used} | {len(X)} baris")

    class_dist = y.value_counts()
    print(f"Distribusi kelas:")
    print(f"  Berhasil (1): {class_dist.get(1, 0)} ({class_dist.get(1, 0)/len(y)*100:.1f}%)")
    print(f"  Gagal    (0): {class_dist.get(0, 0)} ({class_dist.get(0, 0)/len(y)*100:.1f}%)\n")

    # ===== LANGKAH 3: BAGI DATA =====
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y  # Jaga proporsi kelas dalam split
    )
    print(f"Data training: {len(X_train)} | Data testing: {len(X_test)}\n")

    # ===== LANGKAH 4: BUAT PIPELINE =====
    # StandardScaler sangat penting untuk Logistic Regression
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('lr', LogisticRegression(
            random_state=42,
            max_iter=1000,
            C=1.0,               # Regularization strength (default)
            class_weight='balanced'  # Handle imbalanced class
        ))
    ])

    # ===== LANGKAH 5: CROSS-VALIDATION =====
    print("Menjalankan 5-Fold Stratified Cross-Validation...")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    cv_acc = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring='accuracy')
    cv_auc = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring='roc_auc')

    print(f"CV Accuracy per fold : {np.round(cv_acc * 100, 2)}")
    print(f"CV Accuracy rata-rata: {cv_acc.mean() * 100:.2f}% (+/- {cv_acc.std() * 100:.2f}%)")
    print(f"CV ROC-AUC rata-rata : {cv_auc.mean():.4f} (+/- {cv_auc.std():.4f})\n")

    # ===== LANGKAH 6: LATIH MODEL FINAL =====
    print("Melatih model final...")
    pipeline.fit(X_train, y_train)
    print("Selesai.\n")

    # ===== LANGKAH 7: EVALUASI =====
    predictions = pipeline.predict(X_test)
    proba = pipeline.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, predictions)
    roc_auc = roc_auc_score(y_test, proba)

    print(f"Evaluasi pada data test:")
    print(f"  Accuracy : {accuracy * 100:.2f}%  (CV: {cv_acc.mean()*100:.2f}%)")
    print(f"  ROC-AUC  : {roc_auc:.4f}         (CV: {cv_auc.mean():.4f})")
    print(f"  Gap (Acc): {abs(accuracy - cv_acc.mean()) * 100:.2f}% (idealnya < 5%)\n")

    print("Classification Report:")
    print(classification_report(y_test, predictions, target_names=['Gagal (0)', 'Berhasil (1)']))

    print("Confusion Matrix:")
    cm = confusion_matrix(y_test, predictions)
    print(f"  TN={cm[0,0]}  FP={cm[0,1]}")
    print(f"  FN={cm[1,0]}  TP={cm[1,1]}\n")

    # Koefisien fitur (interpretasi Logistic Regression)
    lr_model = pipeline.named_steps['lr']
    print("Koefisien Fitur (pengaruh terhadap keberhasilan):")
    for fname, coef in sorted(zip(FEATURES, lr_model.coef_[0]), key=lambda x: abs(x[1]), reverse=True):
        direction = "[+]" if coef > 0 else "[-]"
        print(f"  {fname:35s}: {coef:+.4f} {direction}")
    print()

    # ===== LANGKAH 8: SIMPAN =====
    joblib.dump(pipeline, MODEL_SAVE_PATH)
    print(f"[OK] Model disimpan sebagai '{MODEL_SAVE_PATH}'")

if __name__ == '__main__':
    train_success_prediction_model()
