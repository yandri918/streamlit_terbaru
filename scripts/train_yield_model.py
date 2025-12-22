import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import joblib
import os

# --- LANGKAH 1: PERSIAPAN ---
DATASET_PATH = 'EDA_500.csv'
MODEL_SAVE_PATH = 'yield_prediction_model.pkl'

def train_yield_prediction_model():
    """
    Fungsi untuk melatih model regresi prediksi hasil panen.
    """
    if not os.path.exists(DATASET_PATH):
        print(f"Error: File dataset '{DATASET_PATH}' tidak ditemukan.")
        return

    # --- LANGKAH 2: MEMUAT & MEMBERSIHKAN DATA ---
    print(f"Memuat dataset dari '{DATASET_PATH}'...")
    dataset = pd.read_csv(DATASET_PATH)
    
    # Membersihkan data: Paksa kolom 'Yield' menjadi numerik dan hapus baris yang tidak valid
    dataset['Yield'] = pd.to_numeric(dataset['Yield'], errors='coerce')
    dataset.dropna(subset=['Yield'], inplace=True)
    
    # Memilih fitur yang relevan
    features = ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Rainfall', 'pH']
    target = 'Yield'
    X = dataset[features]
    y = dataset[target]
    print("Dataset berhasil dimuat dan dibersihkan.")

    # --- LANGKAH 3: MELATIH MODEL ---
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print("Melatih model RandomForestRegressor...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    print("Model berhasil dilatih.")

    # --- LANGKAH 4: EVALUASI & SIMPAN ---
    predictions = model.predict(X_test)
    r2 = r2_score(y_test, predictions)
    print(f"R-squared (R²) score model prediksi panen: {r2:.4f}")
    joblib.dump(model, MODEL_SAVE_PATH)
    print(f"Model berhasil disimpan sebagai '{MODEL_SAVE_PATH}'.")

if __name__ == '__main__':
    train_yield_prediction_model()

