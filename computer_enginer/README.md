# 🎓 UTel Computer Engineering Hub

A next-generation **Learning Management System (LMS)** and curriculum visualization platform for the Computer Engineering department at UTel University. 

Built with **Streamlit**, this application transforms static course lists into an interactive, data-driven academic portal featuring real-time simulations, automated exams, and digital certification.

![LMS Dashboard](https://img.shields.io/badge/Status-Active-success) ![Python](https://img.shields.io/badge/Python-3.9%2B-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-ff4b4b)

## ✨ Key Features

### 1. 🖥️ Modern Student Dashboard
*   **Semantic Navigation**: Browse courses by Semester (1-8) using a clean dropdown interface.
*   **Visual Course Grid**: Courses displayed as interactive cards with status indicators (In Progress / Completed).
*   **Student Profile**: Sidebar tracking GPA, Credits, and smart notifications.

### 2. 🧪 Interactive Simulations (`simulations.py`)
*   **Integrated Labs**: Hands-on learning modules embedded directly within course pages.
*   **Real-time Visualization**:
    *   **Calculus**: Interactive derivative and integral plotter.
    *   **Logic Gates**: Boolean algebra visualizers.
    *   **Production Lines**: Process automation simulators.
    *   **Network Graphs**: Dijkstra pathfinding visualizers.

### 3. 📝 Exam & Certification Engine (`quizzes.py`)
*   **Auto-Graded Quizzes**: Built-in final exams with timer logic.
*   **Realistic Question Bank**: Curriculum-aligned questions for courses like Blockchain, AI, and Cybersecurity.
*   **Instant Certification**: Students scoring >80% receive a **Digital Certificate of Completion**.

### 4. 📄 PDF Export System (`pdf_utils.py`)
*   **Syllabus Downloader**: Generate one-page PDF summaries for any course.
*   **Certified Diplomas**: Download offical-looking PDF certificates with anti-fraud verification codes (mockup).

---

## 🛠️ Technology Stack

*   **Frontend/Backend**: [Streamlit](https://streamlit.io/) (Python)
*   **Data Engine**: JSON-based Curriculum (`data/curriculum.json`)
*   **Visualization**: Altair, Plotly
*   **PDF Generation**: `fpdf`
*   **Code Structure**: Modularized (`Home_Dynamic.py`, `simulations.py`, `quizzes.py`, `pdf_utils.py`)

---

## 🚀 Installation & Usage

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yandri918/computer_enginer.git
    cd computer_enginer
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application**
    ```bash
    streamlit run Home_Dynamic.py
    ```

4.  **Access the Portal**
    Open your browser at `http://localhost:8501`

---

## 📂 Project Structure

```
computer_enginer/
├── Home_Dynamic.py       # 🏠 Main Application Engine (Dashboard & Navigation)
├── Home.py               # ↩️ Legacy Redirect Page
├── simulations.py        # 🧪 Interactive Simulation Logic
├── quizzes.py            # 📝 Exam & Certification Module
├── pdf_utils.py          # 📄 PDF Generation Utilities
├── requirements.txt      # 📦 Project Dependencies
└── data/
    └── curriculum.json   # 💾 The "Brain" (Course Data, Syllabus, Topics)
```

---

## 🌟 Live Demo

Access the deployed application here:
👉 **[computerenginer-2.streamlit.app](https://computerenginer-2.streamlit.app/)**

---

*Developed for UTel University • Powered by AgriSensa API*
