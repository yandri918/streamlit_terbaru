"""
AgriSensa Design System
Centralized design tokens and reusable UI components for consistent styling across all modules.

Usage:
    from utils.design_system import *
    
    # Apply global styles
    apply_design_system()
    
    # Use components
    create_header("Title", "Subtitle", "🌾")
    create_card("Content here")
    create_metric_card("Metric", "1,234", "↑ 12%")
"""

import streamlit as st

# ============================================================================
# DESIGN TOKENS
# ============================================================================

COLORS = {
    # Primary Colors (Agriculture Theme)
    'primary': '#10b981',      # Emerald Green
    'primary_dark': '#059669',
    'primary_light': '#34d399',
    
    # Secondary Colors
    'secondary': '#3b82f6',    # Blue
    'secondary_dark': '#2563eb',
    'secondary_light': '#60a5fa',
    
    # Accent Colors
    'accent': '#f59e0b',       # Amber
    'accent_dark': '#d97706',
    'accent_light': '#fbbf24',
    
    # Semantic Colors
    'success': '#22c55e',
    'warning': '#f59e0b',
    'error': '#ef4444',
    'info': '#3b82f6',
    
    # Neutral Colors
    'dark': '#1f2937',
    'light': '#f9fafb',
    'white': '#ffffff',
    
    # Gray Scale
    'gray_50': '#f9fafb',
    'gray_100': '#f3f4f6',
    'gray_200': '#e5e7eb',
    'gray_300': '#d1d5db',
    'gray_400': '#9ca3af',
    'gray_500': '#6b7280',
    'gray_600': '#4b5563',
    'gray_700': '#374151',
    'gray_800': '#1f2937',
    'gray_900': '#111827',
}

GRADIENTS = {
    'primary': 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
    'secondary': 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
    'accent': 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
    'success': 'linear-gradient(135deg, #22c55e 0%, #16a34a 100%)',
    'purple': 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)',
    'pink': 'linear-gradient(135deg, #ec4899 0%, #db2777 100%)',
    'blue': 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
}

FONTS = {
    'heading': "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    'body': "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    'mono': "'JetBrains Mono', 'Courier New', monospace",
}

FONT_SIZES = {
    'xs': '0.75rem',      # 12px
    'sm': '0.875rem',     # 14px
    'base': '1rem',       # 16px
    'lg': '1.125rem',     # 18px
    'xl': '1.25rem',      # 20px
    '2xl': '1.5rem',      # 24px
    '3xl': '1.875rem',    # 30px
    '4xl': '2.25rem',     # 36px
    '5xl': '3rem',        # 48px
}

FONT_WEIGHTS = {
    'light': '300',
    'normal': '400',
    'medium': '500',
    'semibold': '600',
    'bold': '700',
}

SPACING = {
    'xs': '0.25rem',   # 4px
    'sm': '0.5rem',    # 8px
    'md': '1rem',      # 16px
    'lg': '1.5rem',    # 24px
    'xl': '2rem',      # 32px
    '2xl': '3rem',     # 48px
    '3xl': '4rem',     # 64px
}

BORDER_RADIUS = {
    'sm': '0.375rem',  # 6px
    'md': '0.5rem',    # 8px
    'lg': '0.75rem',   # 12px
    'xl': '1rem',      # 16px
    'full': '9999px',
}

SHADOWS = {
    'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
    'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
}

# ============================================================================
# GLOBAL CSS
# ============================================================================

def get_global_css():
    """Returns global CSS for consistent styling"""
    return f"""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* CSS Variables */
        :root {{
            --primary: {COLORS['primary']};
            --primary-dark: {COLORS['primary_dark']};
            --primary-light: {COLORS['primary_light']};
            --secondary: {COLORS['secondary']};
            --accent: {COLORS['accent']};
            --success: {COLORS['success']};
            --warning: {COLORS['warning']};
            --error: {COLORS['error']};
            --info: {COLORS['info']};
            --dark: {COLORS['dark']};
            --light: {COLORS['light']};
            --gray-100: {COLORS['gray_100']};
            --gray-200: {COLORS['gray_200']};
            --gray-300: {COLORS['gray_300']};
            --gray-500: {COLORS['gray_500']};
            --gray-700: {COLORS['gray_700']};
            --gray-900: {COLORS['gray_900']};
        }}
        
        /* Global Typography */
        body {{
            font-family: {FONTS['body']};
            color: var(--dark);
            line-height: 1.6;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            font-family: {FONTS['heading']};
            font-weight: {FONT_WEIGHTS['semibold']};
            color: var(--dark);
            line-height: 1.3;
        }}
        
        /* Streamlit Overrides */
        .stApp {{
            background-color: var(--light);
        }}
        
        /* Buttons */
        .stButton > button {{
            border-radius: {BORDER_RADIUS['md']};
            font-weight: {FONT_WEIGHTS['medium']};
            padding: 0.5rem 1.5rem;
            transition: all 0.2s ease;
            border: none;
            box-shadow: {SHADOWS['sm']};
        }}
        
        .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: {SHADOWS['md']};
        }}
        
        /* Primary Button */
        .stButton > button[kind="primary"] {{
            background: {GRADIENTS['primary']};
            color: white;
        }}
        
        /* Cards */
        .card {{
            background: white;
            border-radius: {BORDER_RADIUS['lg']};
            padding: {SPACING['lg']};
            box-shadow: {SHADOWS['md']};
            border: 1px solid var(--gray-200);
            margin-bottom: {SPACING['md']};
        }}
        
        /* Metric Cards */
        .metric-card {{
            background: {GRADIENTS['primary']};
            color: white;
            border-radius: {BORDER_RADIUS['lg']};
            padding: {SPACING['lg']};
            box-shadow: {SHADOWS['lg']};
            margin-bottom: {SPACING['md']};
        }}
        
        /* Info Boxes */
        .info-box {{
            background: {GRADIENTS['blue']};
            color: white;
            border-radius: {BORDER_RADIUS['md']};
            padding: {SPACING['md']};
            margin: {SPACING['md']} 0;
        }}
        
        .success-box {{
            background: {GRADIENTS['success']};
            color: white;
            border-radius: {BORDER_RADIUS['md']};
            padding: {SPACING['md']};
            margin: {SPACING['md']} 0;
        }}
        
        .warning-box {{
            background: {GRADIENTS['accent']};
            color: white;
            border-radius: {BORDER_RADIUS['md']};
            padding: {SPACING['md']};
            margin: {SPACING['md']} 0;
        }}
        
        /* Headers */
        .page-header {{
            background: {GRADIENTS['primary']};
            padding: {SPACING['2xl']};
            border-radius: {BORDER_RADIUS['xl']};
            color: white;
            text-align: center;
            margin-bottom: {SPACING['xl']};
            box-shadow: {SHADOWS['lg']};
        }}
        
        .page-header h1 {{
            color: white;
            margin: 0;
            font-size: {FONT_SIZES['4xl']};
            font-weight: {FONT_WEIGHTS['bold']};
        }}
        
        .page-header p {{
            color: rgba(255, 255, 255, 0.9);
            margin: {SPACING['sm']} 0 0 0;
            font-size: {FONT_SIZES['lg']};
        }}
        
        /* Section Headers */
        .section-header {{
            border-left: 4px solid var(--primary);
            padding-left: {SPACING['md']};
            margin: {SPACING['xl']} 0 {SPACING['md']} 0;
        }}
        
        /* Tables */
        .dataframe {{
            border-radius: {BORDER_RADIUS['md']};
            overflow: hidden;
            box-shadow: {SHADOWS['sm']};
        }}
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: {SPACING['sm']};
        }}
        
        .stTabs [data-baseweb="tab"] {{
            border-radius: {BORDER_RADIUS['md']};
            padding: {SPACING['sm']} {SPACING['md']};
            font-weight: {FONT_WEIGHTS['medium']};
        }}
        
        /* Metrics */
        [data-testid="stMetricValue"] {{
            font-size: {FONT_SIZES['3xl']};
            font-weight: {FONT_WEIGHTS['bold']};
            color: var(--primary);
        }}
        
        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: white;
            border-right: 1px solid var(--gray-200);
        }}
        
        /* Expanders */
        .streamlit-expanderHeader {{
            background-color: var(--gray-100);
            border-radius: {BORDER_RADIUS['md']};
            font-weight: {FONT_WEIGHTS['medium']};
        }}
        
        /* Footer */
        .footer {{
            text-align: center;
            padding: {SPACING['xl']};
            color: var(--gray-500);
            border-top: 1px solid var(--gray-200);
            margin-top: {SPACING['2xl']};
        }}
        
        /* Breadcrumb */
        .breadcrumb {{
            display: flex;
            gap: {SPACING['sm']};
            align-items: center;
            color: var(--gray-500);
            font-size: {FONT_SIZES['sm']};
            margin-bottom: {SPACING['md']};
        }}
        
        .breadcrumb a {{
            color: var(--primary);
            text-decoration: none;
        }}
        
        .breadcrumb a:hover {{
            text-decoration: underline;
        }}
    </style>
    """

def apply_design_system():
    """Apply global design system CSS to the page"""
    st.markdown(get_global_css(), unsafe_allow_html=True)

# ============================================================================
# COMPONENT FUNCTIONS
# ============================================================================

def create_header(title, subtitle="", icon="🌾"):
    """Create a standardized page header
    
    Args:
        title: Main title text
        subtitle: Optional subtitle text
        icon: Optional emoji icon
    """
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    
    st.markdown(f"""
    <div class="page-header">
        <h1>{icon} {title}</h1>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)

def create_section_header(title, icon=""):
    """Create a section header with accent border
    
    Args:
        title: Section title
        icon: Optional emoji icon
    """
    icon_html = f"{icon} " if icon else ""
    st.markdown(f"""
    <div class="section-header">
        <h3>{icon_html}{title}</h3>
    </div>
    """, unsafe_allow_html=True)

def create_card(content, title=""):
    """Create a card container
    
    Args:
        content: HTML content for the card
        title: Optional card title
    """
    title_html = f"<h4>{title}</h4>" if title else ""
    
    st.markdown(f"""
    <div class="card">
        {title_html}
        {content}
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(label, value, delta="", icon="📊"):
    """Create a metric display card
    
    Args:
        label: Metric label
        value: Metric value
        delta: Optional delta/change indicator
        icon: Optional emoji icon
    """
    delta_html = f"<p style='font-size: 1rem; margin-top: 0.5rem;'>{delta}</p>" if delta else ""
    
    st.markdown(f"""
    <div class="metric-card">
        <p style='margin: 0; opacity: 0.9; font-size: 0.875rem;'>{icon} {label}</p>
        <h2 style='margin: 0.5rem 0 0 0; color: white; font-size: 2.5rem;'>{value}</h2>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def create_info_box(content, type="info"):
    """Create an information box
    
    Args:
        content: Box content
        type: Box type - 'info', 'success', 'warning'
    """
    class_name = f"{type}-box"
    
    st.markdown(f"""
    <div class="{class_name}">
        {content}
    </div>
    """, unsafe_allow_html=True)

def create_breadcrumb(items):
    """Create breadcrumb navigation
    
    Args:
        items: List of breadcrumb items (strings or tuples of (text, url))
    """
    breadcrumb_html = []
    for i, item in enumerate(items):
        if isinstance(item, tuple):
            text, url = item
            breadcrumb_html.append(f'<a href="{url}">{text}</a>')
        else:
            breadcrumb_html.append(f'<span>{item}</span>')
        
        if i < len(items) - 1:
            breadcrumb_html.append('<span>›</span>')
    
    st.markdown(f"""
    <div class="breadcrumb">
        {' '.join(breadcrumb_html)}
    </div>
    """, unsafe_allow_html=True)

def create_footer(text=""):
    """Create page footer
    
    Args:
        text: Footer text (optional)
    """
    default_text = "© 2026 AgriSensa - Platform Pertanian Cerdas Indonesia"
    footer_text = text if text else default_text
    
    st.markdown(f"""
    <div class="footer">
        <p>{footer_text}</p>
    </div>
    """, unsafe_allow_html=True)

def create_stat_row(stats):
    """Create a row of statistics
    
    Args:
        stats: List of dicts with 'label', 'value', 'icon' keys
    """
    cols = st.columns(len(stats))
    for col, stat in zip(cols, stats):
        with col:
            st.metric(
                label=f"{stat.get('icon', '📊')} {stat['label']}", 
                value=stat['value'],
                delta=stat.get('delta', None)
            )

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_color(color_name):
    """Get color value from design system
    
    Args:
        color_name: Name of the color (e.g., 'primary', 'success')
    
    Returns:
        Hex color code
    """
    return COLORS.get(color_name, COLORS['primary'])

def get_gradient(gradient_name):
    """Get gradient value from design system
    
    Args:
        gradient_name: Name of the gradient
    
    Returns:
        CSS gradient string
    """
    return GRADIENTS.get(gradient_name, GRADIENTS['primary'])

def is_mobile():
    """Check if user is on mobile device (basic detection)"""
    # This is a simple check - for production, use JavaScript
    return False  # Streamlit doesn't have built-in mobile detection

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    st.set_page_config(page_title="Design System Demo", page_icon="🎨", layout="wide")
    
    # Apply design system
    apply_design_system()
    
    # Header
    create_header("AgriSensa Design System", "Komponen UI yang konsisten dan modern", "🎨")
    
    # Breadcrumb
    create_breadcrumb([("Home", "#"), ("Utils", "#"), "Design System"])
    
    st.markdown("---")
    
    # Section: Colors
    create_section_header("Color Palette", "🎨")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div style='background: {COLORS['primary']}; padding: 2rem; border-radius: 0.5rem; color: white; text-align: center;'>
            <strong>Primary</strong><br>{COLORS['primary']}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: {COLORS['secondary']}; padding: 2rem; border-radius: 0.5rem; color: white; text-align: center;'>
            <strong>Secondary</strong><br>{COLORS['secondary']}
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='background: {COLORS['accent']}; padding: 2rem; border-radius: 0.5rem; color: white; text-align: center;'>
            <strong>Accent</strong><br>{COLORS['accent']}
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style='background: {COLORS['success']}; padding: 2rem; border-radius: 0.5rem; color: white; text-align: center;'>
            <strong>Success</strong><br>{COLORS['success']}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Section: Components
    create_section_header("Components", "🧩")
    
    # Metric Cards
    st.markdown("### Metric Cards")
    col1, col2, col3 = st.columns(3)
    with col1:
        create_metric_card("Total Panen", "1,234 kg", "↑ 12%", "🌾")
    with col2:
        create_metric_card("Pendapatan", "Rp 15.5 juta", "↑ 8%", "💰")
    with col3:
        create_metric_card("Luas Lahan", "2.5 ha", "→ 0%", "📏")
    
    st.markdown("---")
    
    # Info Boxes
    st.markdown("### Info Boxes")
    create_info_box("ℹ️ <strong>Info:</strong> Ini adalah info box untuk informasi umum.", "info")
    create_info_box("✅ <strong>Success:</strong> Operasi berhasil dilakukan!", "success")
    create_info_box("⚠️ <strong>Warning:</strong> Perhatian diperlukan untuk item ini.", "warning")
    
    st.markdown("---")
    
    # Stats Row
    st.markdown("### Statistics Row")
    create_stat_row([
        {'label': 'Petani Aktif', 'value': '1,234', 'icon': '👨‍🌾', 'delta': '+12%'},
        {'label': 'Lahan Total', 'value': '567 ha', 'icon': '🌾', 'delta': '+5%'},
        {'label': 'Produksi', 'value': '890 ton', 'icon': '📦', 'delta': '+18%'},
        {'label': 'Revenue', 'value': 'Rp 1.2M', 'icon': '💰', 'delta': '+23%'},
    ])
    
    st.markdown("---")
    
    # Footer
    create_footer()
