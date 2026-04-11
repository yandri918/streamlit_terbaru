
import streamlit as st

def main():
    st.set_page_config(page_title="UTel Curriculum Hub", page_icon="🎓", layout="wide")

    st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        font-weight: bold;
        padding: 1rem;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("## 🎓 Computer Engineering Curriculum")
    st.info("The interactive curriculum for Semesters 1-8 is now hosted on the dedicated instance.")

    st.markdown("### Access Full Curriculum")
    st.markdown("Click the button below to open the official application with all interactive simulations and resources.")

    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <a href="https://computerenginer-2.streamlit.app/" target="_blank" style="
            background-color: #2563eb;
            color: white;
            padding: 1rem 2rem;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 1.2rem;
            display: inline-block;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.2s;
        ">
            🚀 Open App (computerenginer-2.streamlit.app)
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("Powered by UTel University • AgriSensa API")

if __name__ == "__main__":
    main()
