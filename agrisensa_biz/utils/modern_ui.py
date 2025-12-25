"""
Modern UI Components for AgriSensa Biz
Reusable components for consistent, professional design
"""

import streamlit as st
import os

def load_custom_css():
    """Load custom CSS theme"""
    css_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'custom.css')
    try:
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Custom CSS not found. Using default theme.")


def modern_card(title, value, delta=None, icon="📊", color="green"):
    """
    Modern metric card with gradient background and icon
    
    Args:
        title: Card title
        value: Main value to display
        delta: Optional change indicator (e.g., "+12%")
        icon: Emoji icon
        color: Color theme (green, blue, purple, orange)
    """
    colors = {
        "green": "linear-gradient(135deg, #10B981 0%, #059669 100%)",
        "blue": "linear-gradient(135deg, #3B82F6 0%, #2563EB 100%)",
        "purple": "linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%)",
        "orange": "linear-gradient(135deg, #F59E0B 0%, #D97706 100%)",
        "red": "linear-gradient(135deg, #EF4444 0%, #DC2626 100%)"
    }
    
    delta_html = ''
    if delta:
        delta_color = "#10B981" if "+" in str(delta) else "#EF4444"
        delta_arrow = "↑" if "+" in str(delta) else "↓"
        delta_html = f'<div style="color: {delta_color}; font-size: 0.875rem; margin-top: 0.5rem;">{delta_arrow} {delta}</div>'
    
    card_html = f"""
    <div style="
        background: {colors.get(color, colors['green'])};
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    " class="modern-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div style="flex: 1;">
                <div style="color: rgba(255,255,255,0.8); font-size: 0.875rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em;">
                    {title}
                </div>
                <div style="color: white; font-size: 2rem; font-weight: 700; margin-top: 0.5rem;">
                    {value}
                </div>
                {delta_html}
            </div>
            <div style="font-size: 3rem; opacity: 0.3; margin-left: 1rem;">
                {icon}
            </div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def dashboard_header(title, subtitle, user_name=None):
    """
    Modern dashboard header with greeting
    
    Args:
        title: Page title
        subtitle: Page description
        user_name: Optional user name for personalized greeting
    """
    import datetime
    hour = datetime.datetime.now().hour
    greeting = "Selamat Pagi" if hour < 12 else "Selamat Siang" if hour < 18 else "Selamat Malam"
    
    greeting_html = ''
    if user_name:
        greeting_html = f"""
        <div style="color: #94A3B8; font-size: 0.875rem; margin-bottom: 0.5rem;">
            {greeting}, {user_name} 👋
        </div>
        """
    
    header_html = f"""
    <div style="
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid #334155;
    ">
        {greeting_html}
        <h1 style="color: #F1F5F9; margin: 0; font-size: 2rem; font-weight: 700;">
            {title}
        </h1>
        <p style="color: #94A3B8; margin-top: 0.5rem; font-size: 1rem; margin-bottom: 0;">
            {subtitle}
        </p>
    </div>
    """
    # CRITICAL: Must have unsafe_allow_html=True
    st.markdown(header_html, unsafe_allow_html=True)


def stats_grid(stats_list):
    """
    Display stats in modern grid layout
    
    Args:
        stats_list: List of dicts with keys: title, value, icon, color, delta (optional)
    
    Example:
        stats_grid([
            {"title": "Total Biaya", "value": "Rp 93.9M", "icon": "💰", "color": "green"},
            {"title": "Omzet", "value": "Rp 162.4M", "icon": "📈", "color": "blue", "delta": "+25%"}
        ])
    """
    cols = st.columns(len(stats_list))
    for col, stat in zip(cols, stats_list):
        with col:
            modern_card(
                stat['title'],
                stat['value'],
                delta=stat.get('delta'),
                icon=stat['icon'],
                color=stat.get('color', 'green')
            )


def info_card(title, content, icon="ℹ️", color="blue"):
    """
    Information card with icon
    
    Args:
        title: Card title
        content: Card content (can be HTML)
        icon: Emoji icon
        color: Border color (blue, green, orange, red)
    """
    border_colors = {
        "blue": "#3B82F6",
        "green": "#10B981",
        "orange": "#F59E0B",
        "red": "#EF4444"
    }
    
    card_html = f"""
    <div style="
        background: #1E293B;
        border-left: 4px solid {border_colors.get(color, border_colors['blue'])};
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    ">
        <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
            <span style="font-size: 1.5rem; margin-right: 0.75rem;">{icon}</span>
            <h3 style="color: #F1F5F9; margin: 0; font-size: 1.125rem; font-weight: 600;">
                {title}
            </h3>
        </div>
        <div style="color: #94A3B8; font-size: 0.9375rem; line-height: 1.6;">
            {content}
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def section_header(title, subtitle=None):
    """
    Section header with optional subtitle
    
    Args:
        title: Section title
        subtitle: Optional subtitle
    """
    subtitle_html = f'<p style="color: #94A3B8; margin-top: 0.25rem; font-size: 0.9375rem;">{subtitle}</p>' if subtitle else ''
    
    header_html = f"""
    <div style="margin: 2rem 0 1rem 0;">
        <h2 style="color: #F1F5F9; margin: 0; font-size: 1.5rem; font-weight: 700;">
            {title}
        </h2>
        {subtitle_html}
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


def loading_spinner(message="Loading..."):
    """
    Modern loading spinner
    
    Args:
        message: Loading message
    """
    spinner_html = f"""
    <div style="
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 3rem;
    ">
        <div class="spinner" style="
            border: 4px solid #1E293B;
            border-top: 4px solid #10B981;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
        "></div>
        <p style="color: #94A3B8; margin-top: 1rem;">{message}</p>
    </div>
    
    <style>
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    </style>
    """
    return st.markdown(spinner_html, unsafe_allow_html=True)


def feature_card(title, description, icon, link=None):
    """
    Feature card for showcasing modules/features
    
    Args:
        title: Feature title
        description: Feature description
        icon: Emoji icon
        link: Optional link/button
    """
    link_html = ''
    if link:
        link_html = f"""
        <a href="{link}" style="
            color: #10B981;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.875rem;
        ">
            Lihat Detail →
        </a>
        """
    
    card_html = f"""
    <div style="
        background: linear-gradient(135deg, #1E293B 0%, #2a3a4f 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #334155;
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    " class="modern-card">
        <div style="font-size: 2.5rem; margin-bottom: 1rem;">{icon}</div>
        <h3 style="color: #F1F5F9; margin: 0 0 0.5rem 0; font-size: 1.125rem; font-weight: 600;">
            {title}
        </h3>
        <p style="color: #94A3B8; margin: 0 0 1rem 0; font-size: 0.9375rem; line-height: 1.6;">
            {description}
        </p>
        {link_html}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
