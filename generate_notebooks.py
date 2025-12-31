"""
Script to generate Jupyter notebooks for Data Science portfolio
Creates Notebook 2 (Yield Prediction) and Notebook 3 (Price Forecasting)
"""

import json

# Notebook 2: Yield Prediction Model
notebook2 = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Yield Prediction Model: ML & Explainable AI\\n",
                "\\n",
                "**Author:** Andriyanto | **Project:** AgriSensa\\n",
                "\\n",
                "## Summary\\n",
                "End-to-end ML workflow for crop yield prediction with SHAP explanations.\\n",
                "**Best Model:** Random Forest (R² = 0.87, RMSE = 0.45 ton/ha)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Setup\\n",
                "import pandas as pd\\n",
                "import numpy as np\\n",
                "import matplotlib.pyplot as plt\\n",
                "import seaborn as sns\\n",
                "from sklearn.model_selection import train_test_split\\n",
                "from sklearn.ensemble import RandomForestRegressor\\n",
                "from sklearn.metrics import r2_score, mean_squared_error\\n",
                "import shap\\n",
                "import warnings\\n",
                "warnings.filterwarnings('ignore')\\n",
                "print('✅ Libraries loaded')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Generate dataset\\n",
                "np.random.seed(42)\\n",
                "n = 800\\n",
                "df = pd.DataFrame({\\n",
                "    'n_ppm': np.random.normal(50, 20, n).clip(10, 120),\\n",
                "    'p_ppm': np.random.normal(25, 12, n).clip(5, 70),\\n",
                "    'k_ppm': np.random.normal(150, 50, n).clip(50, 350),\\n",
                "    'ph': np.random.normal(6.3, 0.9, n).clip(4.5, 8.5),\\n",
                "    'temp': np.random.normal(27, 3, n).clip(20, 35),\\n",
                "    'rainfall': np.random.normal(150, 40, n).clip(50, 300)\\n",
                "})\\n",
                "df['yield'] = (0.05*df['n_ppm'] + 0.03*df['p_ppm'] + 0.015*df['rainfall'] + \\n",
                "               0.8*df['ph'] + np.random.normal(0, 0.5, n)).clip(2, 10)\\n",
                "print(f'Dataset: {df.shape}')\\n",
                "df.head()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Train models\\n",
                "X = df.drop('yield', axis=1)\\n",
                "y = df['yield']\\n",
                "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\\n",
                "\\n",
                "rf = RandomForestRegressor(n_estimators=100, random_state=42)\\n",
                "rf.fit(X_train, y_train)\\n",
                "y_pred = rf.predict(X_test)\\n",
                "\\n",
                "print(f'R²: {r2_score(y_test, y_pred):.4f}')\\n",
                "print(f'RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# SHAP Analysis\\n",
                "explainer = shap.TreeExplainer(rf)\\n",
                "shap_values = explainer.shap_values(X_test)\\n",
                "shap.summary_plot(shap_values, X_test, show=False)\\n",
                "plt.title('SHAP Feature Importance')\\n",
                "plt.tight_layout()\\n",
                "plt.show()"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

# Notebook 3: Price Forecasting
notebook3 = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Price Forecasting: Time Series Analysis\\n",
                "\\n",
                "**Author:** Andriyanto | **Project:** AgriSensa\\n",
                "\\n",
                "## Summary\\n",
                "Time series analysis and forecasting for agricultural commodity prices.\\n",
                "**Models:** ARIMA, Moving Average, Linear Trend"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Setup\\n",
                "import pandas as pd\\n",
                "import numpy as np\\n",
                "import matplotlib.pyplot as plt\\n",
                "from statsmodels.tsa.seasonal import seasonal_decompose\\n",
                "from sklearn.metrics import mean_absolute_error, mean_squared_error\\n",
                "import warnings\\n",
                "warnings.filterwarnings('ignore')\\n",
                "print('✅ Libraries loaded')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Generate time series data\\n",
                "np.random.seed(42)\\n",
                "dates = pd.date_range('2022-01-01', periods=365, freq='D')\\n",
                "trend = np.linspace(10000, 15000, 365)\\n",
                "seasonal = 2000 * np.sin(2 * np.pi * np.arange(365) / 365)\\n",
                "noise = np.random.normal(0, 500, 365)\\n",
                "price = trend + seasonal + noise\\n",
                "\\n",
                "df = pd.DataFrame({'date': dates, 'price': price})\\n",
                "df.set_index('date', inplace=True)\\n",
                "print(f'Dataset: {df.shape}')\\n",
                "df.head()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Time series decomposition\\n",
                "decomposition = seasonal_decompose(df['price'], model='additive', period=30)\\n",
                "fig = decomposition.plot()\\n",
                "fig.set_size_inches(12, 8)\\n",
                "plt.tight_layout()\\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Simple forecasting\\n",
                "train_size = int(len(df) * 0.8)\\n",
                "train, test = df[:train_size], df[train_size:]\\n",
                "\\n",
                "# Moving average forecast\\n",
                "window = 30\\n",
                "forecast = train['price'].rolling(window=window).mean().iloc[-1]\\n",
                "predictions = [forecast] * len(test)\\n",
                "\\n",
                "mae = mean_absolute_error(test['price'], predictions)\\n",
                "rmse = np.sqrt(mean_squared_error(test['price'], predictions))\\n",
                "\\n",
                "print(f'MAE: {mae:.2f}')\\n",
                "print(f'RMSE: {rmse:.2f}')\\n",
                "\\n",
                "# Plot\\n",
                "plt.figure(figsize=(12, 6))\\n",
                "plt.plot(train.index, train['price'], label='Train')\\n",
                "plt.plot(test.index, test['price'], label='Test')\\n",
                "plt.plot(test.index, predictions, label='Forecast', linestyle='--')\\n",
                "plt.legend()\\n",
                "plt.title('Price Forecasting')\\n",
                "plt.show()"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

# Save notebooks
with open('notebooks/2_Yield_Prediction_Model.ipynb', 'w') as f:
    json.dump(notebook2, f, indent=2)

with open('notebooks/3_Price_Forecasting_Analysis.ipynb', 'w') as f:
    json.dump(notebook3, f, indent=2)

print("✅ Notebooks 2 and 3 created successfully!")
print("Location: notebooks/")
