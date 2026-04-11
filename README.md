# 🛰️ AgriSensa Intelligence Ecosystem v4.0

![Platform Status](https://img.shields.io/badge/Status-Production--Ready-10b981?style=for-the-badge)
![AI Engine](https://img.shields.io/badge/AI-LightGBM%20%7C%20RandomForest-3b82f6?style=for-the-badge)
![UI Theme](https://img.shields.io/badge/Theme-Emerald--Dark-064e3b?style=for-the-badge)

**AgriSensa** is an advanced agricultural super-app ecosystem designed for data-driven precision farming. It integrates real-world agronomic datasets (FAO), real-time food price monitoring (BAPANAS), and high-fidelity weather intelligence into a unified command center.

---

## 🌟 Key Features

### 🧠 Advanced ML Pipeline
*   **Yield Prediction Ultra**: Powered by LightGBM, trained on 28,000+ real-world FAO observations for high-accuracy tonnage estimation.
*   **Smart Crop Advisor**: 99.55% accuracy in crop recommendation based on specific soil (NPK, pH) and climate parameters.
*   **Interpretable AI (SHAP)**: Decisions are no longer "Black Box"—the AI explains *why* it recommends specific actions.

### 📊 Real-Time Market Intelligence
*   **Bapanas Auto-Seek**: Smart integration with the National Food Agency (BAPANAS) with 7-day lookback logic, ensuring price data is always available even during API lag.
*   **Market Trend Analysis**: Predictive price modeling using Linear Regression and Random Forest to anticipate market fluctuations.

### 🌦️ Weather Intelligence Ultra
*   **Agricultural Alerts**: Beyond forecast—AgriSensa provides specific warnings for frost, pests, and irrigation needs.
*   **Ultra-Cache System**: Responsive UI with 30-minute intelligent caching for instant global access.

---

## 🚀 The Satellite Network

AgriSensa is structured as a unified multi-satellite ecosystem:

| Satellite | Focus Area | Live Links |
| :--- | :--- | :--- |
| **AgriSensa Tech** | IoT, Drone, GIS, & Genetics | [Live App](https://teknology.streamlit.app/) |
| **AgriSensa Biz** | RAB, Profit Analysis, & supply Chain | [Live App](https://busines.streamlit.app/) |
| **AgriSensa Eco** | Conservation, Waste, & Environment | [Live App](https://ekosistem.streamlit.app/) |
| **AgriSensa Commodities** | Specific Crop SOPs (Rice, Corn, Fruit) | [Live App](https://budidaya.streamlit.app/) |
| **AgriSensa Livestock** | Animal Husbandry & Aquaculture | [Live App](https://livestoc.streamlit.app/) |

---

## 🛠️ Tech Stack & Architecture

- **Core**: Python 3.10+
- **Frontend**: Streamlit (Emerald Dark Theme)
- **Machine Learning**: Scikit-Learn, LightGBM, Joblib, SHAP
- **Data Engineering**: Pandas, NumPy, JSON-API Integration
- **Visualization**: Plotly, Altair, Folium (GIS)

---

## 📦 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yandri918/streamlit_terbaru.git
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_key
   DATABASE_URL=your_db_url
   BAPANAS_API_KEY=your_bapanas_key (Optional)
   ```

4. **Run the Dashboard**:
   ```bash
   streamlit run agrisensa_streamlit/Home.py
   ```

---

## 💎 Premium UI Configuration

The ecosystem is pre-configured with a professional dark theme. Configuration can be found in `agrisensa_streamlit/.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#10b981"
backgroundColor = "#0f172a"
secondaryBackgroundColor = "#1e293b"
textColor = "#f8fafc"
```

---

## ⚖️ Accountability & Data Source
*   **Agronomic Data**: UN FAO (Food and Agriculture Organization) statistics.
*   **Market Data**: BAPANAS (Badan Pangan Nasional) API.
*   **Weather Data**: Open-Meteo Professional API.

© 2025 AgriSensa Intelligence Systems | *Advancing Food Security through Data Precision.*
