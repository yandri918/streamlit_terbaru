import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

# --- LANGKAH 1: PERSIAPAN ---
DATASET_PATH = 'Crop_recommendation.csv'
MODEL_SAVE_PATH = 'crop_recommendation_model.pkl'

def train_crop_recommendation_model():
    """
    Fungsi untuk melatih model klasifikasi rekomendasi tanaman.
    """
    if not os.path.exists(DATASET_PATH):
        print(f"Error: File dataset '{DATASET_PATH}' tidak ditemukan.")
        return

    # --- LANGKAH 2: MEMUAT DATA ---
    print(f"Memuat dataset dari '{DATASET_PATH}'...")
    dataset = pd.read_csv(DATASET_PATH)
    X = dataset.drop('label', axis=1)
    y = dataset['label']
    print("Dataset berhasil dimuat.")

    # --- LANGKAH 3: MELATIH MODEL ---
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print("Melatih model RandomForestClassifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    print("Model berhasil dilatih.")

    # --- LANGKAH 4: EVALUASI & SIMPAN ---
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Akurasi model rekomendasi tanaman: {accuracy * 100:.2f}%")
    joblib.dump(model, MODEL_SAVE_PATH)
    print(f"Model berhasil disimpan sebagai '{MODEL_SAVE_PATH}'.")

if __name__ == '__main__':
    train_crop_recommendation_model()

