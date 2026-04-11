# 🚀 Senior Data Science Live Coding Survival Guide

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📖 Overview

**Senior Data Science Live Coding Survival Guide** is a comprehensive training ground designed to simulate the high-pressure live coding environments of top-tier tech companies (FAANG+). 

This Streamlit application provides an interactive workspace where you can practice and master the four key pillars of technical interviews:
1.  **Communication**: Articulating thought processes.
2.  **Problem Solving**: optimizing for time/space complexity.
3.  **Coding Fluency**: Writing clean, idiomatic code.
4.  **Verification**: Handling edge cases and testing.

## ✨ Features

The application is divided into specialized modules targeting critical skill sets:

-   **🐍 Python Algorithms**: LeetCode-style algorithmic challenges focusing on patterns and efficiency.
-   **🐼 Pandas Mastery**: Advanced data manipulation, cleaning, and transformation tasks.
-   **💾 SQL Integration**: Complex querying scenarios using DuckDB and Window Functions.
-   **🤖 Machine Learning**: End-to-end modeling, from implementation to evaluation (Transformers, etc.).
-   **📊 A/B Testing**: Statistical rigor, hypothesis testing, and experiment design.
-   **🏗️ System Design**: Architecture and scaling strategies for Machine Learning systems.

## 🛠️ Tech Stack

-   **Frontend**: [Streamlit](https://streamlit.io/)
-   **Data Processing**: Pandas, NumPy
-   **Database**: DuckDB (In-memory SQL)
-   **Machine Learning**: Scikit-learn
-   **Visualization**: Plotly
-   **Statistics**: SciPy

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.8 or higher installed on your system.

### Installation

1.  **Clone the repository** (if applicable) or navigate to the project directory:
    ```bash
    cd live-coding
    ```

2.  **Install dependencies**:
    It is recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

Launch the application using Streamlit:

```bash
streamlit run Home.py
```

The application will open in your default web browser at `http://localhost:8501`.

## 📂 Project Structure

```text
live-coding/
├── Home.py                 # Main entry point and dashboard
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
└── pages/                  # Individual learning modules
    ├── 1_Python_Algorithms.py
    ├── 2_Pandas_Mastery.py
    ├── 3_SQL_Integration.py
    ├── 4_Machine_Learning.py
    ├── 5_AB_Testing_Stats.py
    └── 6_System_Design.py
```

## 🤝 Contributing

Contributions are welcome! If you have additional interview questions, optimizations, or new modules, please feel free to:
1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---
**Created by Yandri for Live Coding Prep**
