import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# --- LANGKAH 1: PERSIAPAN ---
DATASET_PATH = 'EDA_500.csv'
MODEL_SAVE_PATH = 'success_model.pkl'

def train_success_prediction_model():
    """
    Fungsi untuk melatih model Logistic Regression yang memprediksi keberhasilan panen.
    """
    if not os.path.exists(DATASET_PATH):
        print(f"Error: File dataset '{DATASET_PATH}' tidak ditemukan.")
        print("Pastikan 'EDA_500.csv' berada di folder yang sama.")
        return

    # --- LANGKAH 2: MEMUAT & MEREKAYASA FITUR DATA ---
    print(f"Memuat dataset dari '{DATASET_PATH}'...")
    dataset = pd.read_csv(DATASET_PATH)
    
    # Membersihkan data
    dataset['Yield'] = pd.to_numeric(dataset['Yield'], errors='coerce')
    dataset.dropna(subset=['Yield'], inplace=True)
    
    # REKAYASA FITUR: Membuat target biner "Success"
    yield_median = dataset['Yield'].median()
    print(f"Ambang batas keberhasilan (Median Yield): {yield_median:.2f} kg/ha")
    dataset['Success'] = (dataset['Yield'] > yield_median).astype(int) # 1 jika Berhasil, 0 jika Gagal

    # Memilih fitur yang relevan untuk model
    features = ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Rainfall', 'pH']
    target = 'Success'

    X = dataset[features]
    y = dataset[target]
    print("Dataset berhasil dimuat dan target 'Success' telah dibuat.")

    # --- LANGKAH 3: MELATIH MODEL LOGISTIC REGRESSION ---
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print("Melatih model Logistic Regression...")
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train, y_train)
    print("Model berhasil dilatih.")

    # --- LANGKAH 4: EVALUASI & SIMPAN MODEL ---
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"\nAkurasi model prediksi keberhasilan: {accuracy * 100:.2f}%\n")
    print("Laporan Klasifikasi:")
    print(classification_report(y_test, predictions, target_names=['Gagal (0)', 'Berhasil (1)']))

    joblib.dump(model, MODEL_SAVE_PATH)
    print(f"\nModel berhasil disimpan sebagai '{MODEL_SAVE_PATH}'.")

if __name__ == '__main__':
    train_success_prediction_model()

