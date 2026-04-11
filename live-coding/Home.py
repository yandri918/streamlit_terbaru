import streamlit as st

st.set_page_config(
    page_title="Big Tech Live Coding",
    page_icon="💻",
    layout="wide"
)

# Custom CSS for Glassmorphism and specialized styling
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #1e1e2f 0%, #2a2a40 100%);
        color: #e0e0e0;
    }
    
    /* Glassmorphism Cards */
    .css-1r6slb0, .css-12oz5g7 {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    h1, h2, h3 {
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Code blocks */
    .stCodeBlock {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161625;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 Senior Data Science Live Coding Survival Guide")
st.markdown("### Master the Art of the Technical Interview at FAANG+")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    Welcome to your personal training ground. This application simulates the **live coding** environment used by top-tier tech companies.
    
    #### 🎯 The Rubric
    Interviewers grade you on 4 key pillars:
    1.  **Communication**: Clarifying requirements, thinking out loud.
    2.  **Problem Solving**: Algorithmic efficiency (Time/Space Complexity).
    3.  **Coding Fluency**: Clean, idiomatic, bug-free code.
    4.  **Verification**: Testing edge cases and valid inputs.
    
    #### 📚 Modules
    Select a module from the sidebar to begin:
    -   **Python Algorithms**: Patterns for algorithmic challenges (LeetCode style).
    -   **Pandas Mastery**: Complex data manipulation and cleaning.
    -   **SQL Integration**: Advanced querying with Window Functions.
    -   **Machine Learning**: Modeling from scratch (Transformers, Evaluation).
    -   **A/B Testing**: Statistical rigor and experiment design.
    -   **System Design**: ML Systems architecture and scaling.
    """)
    
    st.info("💡 **Pro Tip**: In a real interview, *always* run your code often. Don't write 50 lines without checking if it works.")

with col2:
    st.image("https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", caption="Live Coding Environment")
    st.markdown("### 🛠️ Interactive Workspace")
    st.markdown("""
    - Embedded Code Runners
    - Hidden Solutions
    - Real-time Output
    """)

st.markdown("---")
st.markdown("##### Created by Yandri for Live Coding Prep")
