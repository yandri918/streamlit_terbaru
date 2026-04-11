# train_model.py
# -*- coding: utf-8 -*-
# ============================================================
# Model: BWD (Brown/Black Wing Disease) Classifier
# Algoritma: SVM (Support Vector Classifier)
# Output: bwd_model.pkl
#
# DATASET YANG DIPERLUKAN: bwd_dataset.csv
# - Kolom: avg_hue_value (float), bwd_score (int: 0 atau 1)
# - Sumber: Spektrofotometer sensor daun padi, atau
#           https://www.kaggle.com/datasets/shayanriyaz/riceleafs
#           (perlu konversi label gambar ke nilai hue numerik)
# ============================================================

import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os
import numpy as np

# ===== LANGKAH 1: PERSIAPAN =====
DATASET_PATH = 'bwd_dataset.csv'
MODEL_SAVE_PATH = 'bwd_model.pkl'

def train_bwd_model():
    """
    Fungsi untuk melatih model SVM deteksi BWD pada daun padi.
    PERBAIKAN:
    - Tambah StandardScaler (WAJIB untuk SVM — tanpa scaler, SVM bisa bias)
    - Gunakan Pipeline (scaler otomatis ikut tersimpan di .pkl)
    - Tambah cross-validation 5-fold untuk validasi yang lebih robust
    - Tambah classification_report & confusion_matrix
    """

    # Cek dataset tersedia
    if not os.path.exists(DATASET_PATH):
        print(f"[ERROR] File dataset '{DATASET_PATH}' tidak ditemukan.")
        print("Silakan download dataset dari:")
        print("  https://www.kaggle.com/datasets/shayanriyaz/riceleafs")
        print("  atau buat bwd_dataset.csv dengan kolom: avg_hue_value, bwd_score")
        return

    # ===== LANGKAH 2: MUAT DATASET =====
    print("Memuat dataset...")
    dataset = pd.read_csv(DATASET_PATH)
    print(f"Dataset berhasil dimuat: {len(dataset)} baris, {dataset.shape[1]} kolom")
    print(f"Distribusi kelas:\n{dataset['bwd_score'].value_counts()}\n")

    # Pisahkan fitur dan target
    X = dataset[['avg_hue_value']]
    y = dataset['bwd_score']

    # ===== LANGKAH 3: BAGI DATA TRAINING & TESTING =====
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y  # Pastikan proporsi kelas terjaga
    )
    print(f"Data training: {len(X_train)} baris | Data testing: {len(X_test)} baris\n")

    # ===== LANGKAH 4: BUAT PIPELINE (Scaler + SVM) =====
    # PENTING: StandardScaler WAJIB untuk SVM!
    # Tanpa scaling, fitur dengan nilai besar mendominasi dan model jadi bias.
    # Pipeline memastikan scaler disimpan bersama model di file .pkl
    pipeline = Pipeline([
        ('scaler', StandardScaler()),          # Normalisasi fitur
        ('svm', SVC(kernel='linear', probability=True, random_state=42))
    ])

    # ===== LANGKAH 5: CROSS-VALIDATION (5-FOLD) =====
    # Lebih akurat dari single train-test split
    print("Menjalankan 5-Fold Stratified Cross-Validation...")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring='accuracy')

    print(f"CV Accuracy per fold : {np.round(cv_scores * 100, 2)}")
    print(f"CV Accuracy rata-rata: {cv_scores.mean() * 100:.2f}% (+/- {cv_scores.std() * 100:.2f}%)\n")

    # ===== LANGKAH 6: LATIH MODEL FINAL =====
    print("Melatih model final pada seluruh data training...")
    pipeline.fit(X_train, y_train)
    print("Model berhasil dilatih.\n")

    # ===== LANGKAH 7: EVALUASI PADA DATA TEST =====
    predictions = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print(f"Akurasi pada data test    : {accuracy * 100:.2f}%")
    print(f"Selisih dengan CV score   : {abs(accuracy - cv_scores.mean()) * 100:.2f}% (idealnya < 5%)\n")

    print("Classification Report:")
    print(classification_report(y_test, predictions, target_names=['Sehat (0)', 'BWD (1)']))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, predictions))
    print()

    # ===== LANGKAH 8: SIMPAN MODEL =====
    joblib.dump(pipeline, MODEL_SAVE_PATH)
    print(f"[OK] Model Pipeline (Scaler + SVM) disimpan sebagai '{MODEL_SAVE_PATH}'")
    print("     Model sudah termasuk StandardScaler - siap langsung dipakai tanpa pre-processing manual.")


if __name__ == '__main__':
    train_bwd_model()