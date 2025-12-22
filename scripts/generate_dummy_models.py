import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import joblib

# 1. BWD Model Dummy (1 fitur: avg_hue, target score 0 atau 1)
X_bwd = np.array([[30], [40], [50], [60], [70], [80], [90]])  # 1 fitur avg_hue
y_bwd = np.array([0, 0, 1, 1, 1, 0, 0])
bwd_model = DecisionTreeClassifier()
bwd_model.fit(X_bwd, y_bwd)
joblib.dump(bwd_model, 'bwd_model.pkl')

# 2. Recommendation Model Dummy (4 fitur: ph_tanah, skor_bwd, kelembaban_tanah, umur_tanaman_hari)
X_rec = np.random.uniform(5.5, 7.5, size=(100, 4))
y_rec = np.random.uniform(20, 180, size=(100, 3))  # N, P, K dummy output
recommendation_model = RandomForestRegressor()
recommendation_model.fit(X_rec, y_rec)
joblib.dump(recommendation_model, 'recommendation_model.pkl')

# 3. Crop Recommendation Model (7 fitur environmental)
X_crop = np.random.uniform(0, 100, size=(50, 7))
y_crop = np.random.choice(['padi', 'jagung', 'cabai'], size=(50,))
crop_model = RandomForestClassifier()
crop_model.fit(X_crop, y_crop)
joblib.dump(crop_model, 'crop_recommendation_model.pkl')

print('Dummy models bwd_model.pkl, recommendation_model.pkl, crop_recommendation_model.pkl have been generated!')



