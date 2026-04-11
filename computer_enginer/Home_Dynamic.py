
import streamlit as st
import json
import os
import sys

# Add current directory to path so we can import simulations
sys.path.append(os.path.dirname(__file__))

try:
    from simulations import SIMULATION_MAP, apply_custom_css
    from quizzes import render_quiz
    from pdf_utils import generate_syllabus_pdf
except ImportError:
    # Fallback if file not found (for testing)
    SIMULATION_MAP = {}
    def apply_custom_css(): pass
    def render_quiz(d): pass
    def generate_syllabus_pdf(d): return b""

# Load Data
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "curriculum.json")

def load_data():
    if not os.path.exists(DATA_FILE):
        st.error("Data file not found. Please run migration script.")
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    st.set_page_config(page_title="UTel Academic Portal | Computer Engineering", page_icon="🎓", layout="wide")
    
    # Apply global styles
    apply_custom_css()
    
    curriculum = load_data()
    if not curriculum:
        return

    # Initialize Session State
    if 'selected_course_id' not in st.session_state:
        st.session_state.selected_course_id = None
        
    # --- MODERN CSS WITH GLASSMORPHISM ---
    st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@600;700;800&display=swap');
        
        /* Import Font Awesome */
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css');
        
        /* CSS Variables */
        :root {
            --primary-gradient: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
            --secondary-gradient: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
            --glass-bg: rgba(255, 255, 255, 0.1);
            --glass-border: rgba(255, 255, 255, 0.2);
            --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.1);
            --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.12);
            --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.15);
            --shadow-xl: 0 20px 60px rgba(0, 0, 0, 0.3);
        }
        
        /* Global Styles */
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Poppins', sans-serif;
            font-weight: 700;
            letter-spacing: -0.02em;
        }
        
        /* Hide Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Premium Hero Section */
        .hero-box {
            background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
            padding: 3rem 2rem;
            border-radius: 24px;
            color: white;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
            box-shadow: var(--shadow-xl);
            animation: fadeInUp 0.8s ease-out;
        }
        
        .hero-box::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: rotate 20s linear infinite;
        }
        
        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        .hero-box h1 {
            position: relative;
            z-index: 1;
            margin: 0;
            font-size: 2.5rem;
            background: linear-gradient(to right, #ffffff, #bfdbfe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .hero-box p {
            position: relative;
            z-index: 1;
            opacity: 0.9;
            margin-top: 0.5rem;
            font-size: 1.1rem;
        }
        
        /* Icon Styling */
        .fas, .far, .fab {
            margin-right: 0.5rem;
        }
        
        /* Course Cards */
        .stButton>button {
            width: 100%;
            border-radius: 12px;
            transition: all 0.3s ease;
            font-weight: 600;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: transparent !important;
            font-weight: 600;
            font-size: 1rem;
        }
        
        /* Course Content Card */
        .course-content-card {
            background: white;
            padding: 2rem;
            border-radius: 16px;
            border: 1px solid #e2e8f0;
            box-shadow: var(--shadow-md);
            animation: fadeInUp 0.6s ease-out;
        }
        
        /* Topic Items */
        .topic-item {
            padding: 12px 16px;
            margin-bottom: 8px;
            background: #f8fafc;
            border-radius: 8px;
            border-left: 3px solid #cbd5e1;
            display: flex;
            align-items: center;
            transition: all 0.2s ease;
        }
        
        .topic-item:hover {
            background: #e0f2fe;
            border-left-color: #3b82f6;
            transform: translateX(4px);
        }
        
        /* Resource Cards */
        .resource-card {
            padding: 1.25rem;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            background: white;
            transition: all 0.2s ease;
            text-decoration: none;
            color: inherit;
            display: block;
            height: 100%;
        }
        
        .resource-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-md);
            border-color: #3b82f6;
        }
        
        /* Sidebar Profile */
        .profile-section {
            text-align: center;
            padding: 1rem;
            background: linear-gradient(135deg, #f8fafc 0%, #e0f2fe 100%);
            border-radius: 12px;
            margin-bottom: 1rem;
        }
        
        /* Animations */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .hero-box h1 {
                font-size: 1.8rem;
            }
            
            .hero-box p {
                font-size: 1rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)
        
    # --- SIDEBAR: STUDENT PROFILE (LMS Style) ---
    with st.sidebar:
        st.markdown("""
        <div class="profile-section">
            <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" width="80" style="border-radius: 50%; margin-bottom: 0.5rem;">
            <h3 style="margin: 0.5rem 0 0 0; font-size: 1.1rem;">Welcome, <strong>Student</strong></h3>
            <p style="margin: 0.25rem 0; color: #64748b; font-size: 0.9rem;">Computer Engineering • Semester 6</p>
        </div>
        """, unsafe_allow_html=True)
        
        # MOCK PROGRESS
        st.markdown("#### <i class='fas fa-graduation-cap'></i> Academic Progress", unsafe_allow_html=True)
        st.progress(0.72)
        col_s1, col_s2 = st.columns(2)
        col_s1.metric("GPA", "3.85")
        col_s2.metric("Credits", "112/144")
        
        st.divider()
        st.markdown("#### <i class='fas fa-bell'></i> Notifications", unsafe_allow_html=True)
        st.info("Mid-term exams for **MA301** starting next week.")

    # --- HERO SECTION ---
    st.markdown("""
    <div class="hero-box">
        <h1><i class="fas fa-graduation-cap"></i> UTel Academic Portal</h1>
        <p>
            Access your courses, simulations, and learning resources in one unified hub.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- SEMESTER & COURSE NAVIGATION ---
    
    st.markdown("## <i class='fas fa-book-open'></i> My Courses", unsafe_allow_html=True)
    
    semesters = list(curriculum.keys())
    semesters.sort(key=lambda x: int(x.split(" ")[1]) if x.split(" ")[1].isdigit() else 99)
    
    # Filter Layout
    col_filter1, col_filter2 = st.columns([1, 2])
    with col_filter1:
        selected_semester = st.selectbox("Current Semester", semesters, index=0, label_visibility="collapsed")
    
    courses = curriculum[selected_semester]
    
    # Course Grid
    cols = st.columns(4) 
    for idx, course in enumerate(courses):
        with cols[idx % 4]:
            is_selected = st.session_state.selected_course_id == course['id']
            # Mock Status (Random for demo feel)
            status_color = "#10b981" if idx % 3 == 0 else "#f59e0b" # Green vs Amber
            status_text = "Completed" if idx % 3 == 0 else "In Progress"
            
            # Button Label WITHOUT emoji - professional appearance
            label = f"{course['id']}\n{course['name']}"
            
            if st.button(
                label, 
                key=f"btn_{course['id']}", 
                use_container_width=True,
                type="primary" if is_selected else "secondary"
            ):
                st.session_state.selected_course_id = course['id']
                
            # Mini Status Bar below button
            st.markdown(f"""
            <div style="height: 4px; width: 100%; background: #e2e8f0; border-radius: 2px; margin-top: -8px; margin-bottom: 12px;">
                <div style="height: 100%; width: {'100%' if idx%3==0 else '45%'}; background: {status_color}; border-radius: 2px;"></div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # --- ACTIVE COURSE CONTENT ---
    active_course = next((c for c in courses if c['id'] == st.session_state.selected_course_id), None)
    
    if not active_course and courses:
        active_course = courses[0]
        st.session_state.selected_course_id = active_course['id']
        
    if active_course:
        render_course_content(active_course)

def render_course_content(course_data):
    """Renders the detailed content for a single course."""
    st.markdown(f"""
    <div class="course-content-card">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div>
                <span style="background: #eff6ff; color: #2563eb; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">{course_data['id']}</span>
                <h1 style="margin-top: 0.5rem; margin-bottom: 0.5rem; font-size: 2.2rem;">{course_data['name']}</h1>
                <div style="display: flex; gap: 1.5rem; color: #64748b; font-size: 0.95rem;">
                    <span><i class="fas fa-signal"></i> Difficulty: <b>{course_data['difficulty']}</b></span>
                    <span><i class="fas fa-clock"></i> {course_data['hours']} Hrs/Week</span>
                    <span><i class="fas fa-trophy"></i> {course_data['credits']} Credits</span>
                </div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 2.5rem;">{course_data['icon']}</div>
            </div>
        </div>
        
        <hr style="margin: 2rem 0; border-color: #f1f5f9;">
        
        <div style="font-size: 1.05rem; line-height: 1.6; color: #334155;">
            {course_data['description']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("") 

    # Content Tabs
    tab1, tab2, tab_sim, tab_exam = st.tabs([
        "📚 Syllabus & Topics", 
        "📺 Learning Resources", 
        "🛠️ Launch Simulation", 
        "📝 Final Exam"
    ])

    with tab1:
        col_syl1, col_syl2 = st.columns([3, 1])
        with col_syl1:
             st.markdown("### <i class='fas fa-list-check'></i> Syllabus Breakdown", unsafe_allow_html=True)
        with col_syl2:
            try:
                pdf_bytes = generate_syllabus_pdf(course_data)
                st.download_button(
                    label="📄 Download PDF",
                    data=pdf_bytes,
                    file_name=f"Syllabus_{course_data['id']}.pdf",
                    mime="application/pdf",
                    key=f"dl_syl_{course_data['id']}"
                )
            except Exception as e:
                pass

        for topic in course_data.get('topics', []):
            st.markdown(f"""
            <div class="topic-item">
                <span style="margin-right: 12px; color: #64748b;"><i class="fas fa-check-circle"></i></span> {topic}
            </div>
            """, unsafe_allow_html=True)
            
    with tab2:
        st.markdown("### <i class='fas fa-video'></i> Curated Materials", unsafe_allow_html=True)
        resources = course_data.get('resources', [])
        if not resources:
            st.info("Additional resources are being curated.")
        else:
            r_cols = st.columns(2)
            for i, res in enumerate(resources):
                with r_cols[i % 2]:
                    if res['type'] == 'youtube':
                        icon = "fab fa-youtube"
                        color = "#ef4444"
                    elif res['type'] == 'pdf':
                        icon = "fas fa-file-pdf"
                        color = "#dc2626"
                    else:
                        icon = "fas fa-link"
                        color = "#3b82f6"
                    
                    st.markdown(f"""
                    <a href="{res['url']}" target="_blank" style="text-decoration: none; color: inherit;">
                        <div class="resource-card">
                             <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                                <span style="font-size: 1.5rem; margin-right: 0.75rem; color: {color};"><i class="{icon}"></i></span>
                                <h4 style="margin: 0; font-size: 1rem;">{res['title']}</h4>
                             </div>
                             <p style="margin: 0; color: #64748b; font-size: 0.9rem;">{res.get('description','Access external resource')}</p>
                        </div>
                    </a>
                    """, unsafe_allow_html=True)

    with tab_sim:
        st.info("💡 **Interactive Lab**: Modify parameters below to see real-time results.")
        # Wrapper for Simulation
        st.markdown('<div style="background: #fdfbf7; padding: 2rem; border-radius: 12px; border: 1px dashed #d97706;">', unsafe_allow_html=True)
        
        sim_func = SIMULATION_MAP.get(course_data['id'])
        if sim_func:
            try:
                sim_func()
            except Exception as e:
                st.error(f"Simulation Error: {e}")
        else:
            st.warning("⚠️ Simulation lab under construction.")
            
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_exam:
        render_quiz(course_data)

if __name__ == "__main__":
    main()
