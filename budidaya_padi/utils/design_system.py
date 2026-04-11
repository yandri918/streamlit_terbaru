"""
Premium Design System for AgriSensa Padi
Centralized styling, icons, and UI components
"""

def get_font_awesome_cdn():
    """Returns Font Awesome CDN link"""
    return '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">'

def get_google_fonts():
    """Returns Google Fonts import"""
    return '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">'

# Color Palette
COLORS = {
    # Primary (Agricultural Green)
    'primary': '#2E7D32',
    'primary_dark': '#1B5E20',
    'primary_light': '#4CAF50',
    
    # Secondary
    'secondary': '#558B2F',
    'secondary_dark': '#33691E',
    'secondary_light': '#7CB342',
    
    # Accent
    'accent': '#FDD835',
    'accent_dark': '#F9A825',
    
    # Neutrals
    'white': '#FFFFFF',
    'gray_50': '#F8F9FA',
    'gray_100': '#F1F3F4',
    'gray_200': '#E8EAED',
    'gray_300': '#DADCE0',
    'gray_400': '#BDC1C6',
    'gray_500': '#9AA0A6',
    'gray_600': '#80868B',
    'gray_700': '#5F6368',
    'gray_800': '#3C4043',
    'gray_900': '#202124',
    
    # Status
    'success': '#34A853',
    'warning': '#FBBC04',
    'error': '#EA4335',
    'info': '#4285F4',
}

# Icon Mapping
ICONS = {
    'rab_calculator': 'fa-calculator',
    'cultivation_guide': 'fa-book-open',
    'pest_disease': 'fa-bug',
    'sop': 'fa-clipboard-list',
    'fertilizer': 'fa-flask',
    'calendar': 'fa-calendar-alt',
    'business': 'fa-chart-line',
    'varieties': 'fa-seedling',
    'water': 'fa-tint',
    'soil': 'fa-vial',
    'spray': 'fa-spray-can',
    'logbook': 'fa-book',
    'mechanization': 'fa-tractor',
    'weather': 'fa-cloud-sun',
    'money': 'fa-money-bill-wave',
    'chart': 'fa-chart-bar',
    'alert': 'fa-exclamation-triangle',
    'check': 'fa-check-circle',
    'info': 'fa-info-circle',
    'download': 'fa-download',
    'upload': 'fa-upload',
    'edit': 'fa-edit',
    'delete': 'fa-trash',
    'save': 'fa-save',
    'search': 'fa-search',
    'filter': 'fa-filter',
    'settings': 'fa-cog',
    'user': 'fa-user',
    'home': 'fa-home',
}

def icon(name, style='fas', color=None, size=None):
    """
    Generate Font Awesome icon HTML
    
    Args:
        name: Icon name from ICONS dict or direct FA class
        style: Icon style (fas, far, fab)
        color: Optional color override
        size: Optional size (sm, lg, 2x, 3x, etc.)
    
    Returns:
        HTML string for icon
    """
    icon_class = ICONS.get(name, name)
    classes = f"{style} {icon_class}"
    
    if size:
        classes += f" fa-{size}"
    
    style_attr = f'style="color: {color};"' if color else ''
    
    return f'<i class="{classes}" {style_attr}></i>'

def get_premium_css():
    """Returns comprehensive premium CSS styling"""
    return f"""
    <style>
        /* Import Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Roboto:wght@300;400;500;700&display=swap');
        
        /* Root Variables */
        :root {{
            --primary: {COLORS['primary']};
            --primary-dark: {COLORS['primary_dark']};
            --primary-light: {COLORS['primary_light']};
            --secondary: {COLORS['secondary']};
            --accent: {COLORS['accent']};
            --white: {COLORS['white']};
            --gray-50: {COLORS['gray_50']};
            --gray-100: {COLORS['gray_100']};
            --gray-800: {COLORS['gray_800']};
            --success: {COLORS['success']};
            --warning: {COLORS['warning']};
            --error: {COLORS['error']};
            --info: {COLORS['info']};
            
            --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-secondary: 'Roboto', sans-serif;
            
            --shadow-sm: 0 2px 4px rgba(0,0,0,0.05);
            --shadow-md: 0 4px 12px rgba(0,0,0,0.08);
            --shadow-lg: 0 8px 24px rgba(0,0,0,0.12);
            --shadow-xl: 0 12px 40px rgba(0,0,0,0.15);
            
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --radius-xl: 20px;
        }}
        
        /* Global Styles */
        * {{
            font-family: var(--font-primary);
        }}
        
        .stApp {{
            background: linear-gradient(135deg, #f5f7fa 0%, #e8f5e9 100%);
        }}
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {{
            font-family: var(--font-primary);
            font-weight: 600;
            color: var(--gray-800);
            letter-spacing: -0.02em;
        }}
        
        h1 {{
            font-size: 2.5rem;
            font-weight: 700;
        }}
        
        h2 {{
            font-size: 2rem;
        }}
        
        h3 {{
            font-size: 1.5rem;
        }}
        
        /* Dashboard Header - Glassmorphism */
        .dashboard-header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            padding: 2.5rem;
            border-radius: var(--radius-lg);
            color: white;
            margin-bottom: 2rem;
            box-shadow: var(--shadow-xl);
            position: relative;
            overflow: hidden;
        }}
        
        .dashboard-header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><defs><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
            opacity: 0.3;
        }}
        
        .dashboard-header h1 {{
            color: white !important;
            position: relative;
            z-index: 1;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        
        .dashboard-header p {{
            position: relative;
            z-index: 1;
            opacity: 0.95;
            font-size: 1.1rem;
        }}
        
        /* Weather Widget - Glassmorphism */
        .weather-widget {{
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            padding: 12px 24px;
            border-radius: var(--radius-md);
            display: inline-block;
            margin-top: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
            position: relative;
            z-index: 1;
        }}
        
        /* Premium Cards */
        .stat-card {{
            background: var(--white);
            border-radius: var(--radius-md);
            padding: 1.5rem;
            box-shadow: var(--shadow-md);
            border-left: 4px solid var(--primary);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}
        
        .stat-card::before {{
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 100px;
            height: 100px;
            background: linear-gradient(135deg, var(--primary-light) 0%, transparent 70%);
            opacity: 0.05;
            border-radius: 0 var(--radius-md) 0 100%;
        }}
        
        .stat-card:hover {{
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
            border-left-width: 6px;
        }}
        
        /* Alert Cards */
        .alert-card {{
            background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
            border-left: 5px solid var(--warning);
            padding: 1.25rem;
            border-radius: var(--radius-md);
            color: #E65100;
            margin-bottom: 1rem;
            box-shadow: var(--shadow-sm);
            font-weight: 500;
        }}
        
        .alert-card strong {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
        }}
        
        /* Price Ticker */
        .price-ticker {{
            background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
            color: var(--primary-dark);
            padding: 1.25rem;
            border-radius: var(--radius-md);
            font-weight: 600;
            text-align: center;
            margin-bottom: 1rem;
            border: 2px solid #A5D6A7;
            box-shadow: var(--shadow-sm);
            transition: all 0.3s ease;
        }}
        
        .price-ticker:hover {{
            transform: scale(1.02);
            box-shadow: var(--shadow-md);
        }}
        
        /* Feature Buttons */
        .feature-btn {{
            text-align: center;
            padding: 1.5rem;
            background: var(--white);
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-sm);
            cursor: pointer;
            border: 2px solid var(--gray-100);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}
        
        .feature-btn::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(46, 125, 50, 0.1), transparent);
            transition: left 0.5s ease;
        }}
        
        .feature-btn:hover::before {{
            left: 100%;
        }}
        
        .feature-btn:hover {{
            border-color: var(--primary);
            background: linear-gradient(135deg, #F1F8E9 0%, #DCEDC8 100%);
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
        }}
        
        .feature-btn h3 {{
            font-size: 1.1rem;
            margin-top: 1rem;
            color: var(--gray-800);
            font-weight: 600;
        }}
        
        .feature-btn i {{
            font-size: 2.5rem;
            color: var(--primary);
            margin-bottom: 0.5rem;
        }}
        
        /* Streamlit Component Overrides */
        .stButton > button {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            border: none;
            border-radius: var(--radius-md);
            padding: 0.75rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: var(--shadow-md);
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }}
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background-color: var(--gray-50);
            padding: 8px;
            border-radius: var(--radius-md);
        }}
        
        .stTabs [data-baseweb="tab"] {{
            border-radius: var(--radius-sm);
            padding: 12px 24px;
            font-weight: 600;
            background-color: transparent;
            border: none;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white !important;
        }}
        
        /* Metrics */
        [data-testid="stMetricValue"] {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary-dark);
        }}
        
        /* Sidebar */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, var(--white) 0%, var(--gray-50) 100%);
        }}
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {{
            color: var(--primary-dark);
        }}
        
        /* Input Fields */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div {{
            border-radius: var(--radius-sm);
            border: 2px solid var(--gray-200);
            transition: all 0.3s ease;
        }}
        
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {{
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.1);
        }}
        
        /* Data Tables */
        .dataframe {{
            border-radius: var(--radius-md);
            overflow: hidden;
            box-shadow: var(--shadow-sm);
        }}
        
        /* Success/Info/Warning/Error Messages */
        .stSuccess {{
            background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
            border-left: 4px solid var(--success);
            border-radius: var(--radius-md);
        }}
        
        .stInfo {{
            background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
            border-left: 4px solid var(--info);
            border-radius: var(--radius-md);
        }}
        
        .stWarning {{
            background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
            border-left: 4px solid var(--warning);
            border-radius: var(--radius-md);
        }}
        
        .stError {{
            background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%);
            border-left: 4px solid var(--error);
            border-radius: var(--radius-md);
        }}
        
        /* Animations */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .animate-fade-in {{
            animation: fadeInUp 0.6s ease-out;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .dashboard-header {{
                padding: 1.5rem;
            }}
            
            .dashboard-header h1 {{
                font-size: 1.75rem;
            }}
            
            .feature-btn {{
                padding: 1rem;
            }}
        }}
    </style>
    """

def apply_design_system():
    """Apply complete design system (CSS + Font Awesome)"""
    import streamlit as st
    
    # Inject Font Awesome and Google Fonts
    st.markdown(get_font_awesome_cdn(), unsafe_allow_html=True)
    st.markdown(get_google_fonts(), unsafe_allow_html=True)
    
    # Inject Premium CSS
    st.markdown(get_premium_css(), unsafe_allow_html=True)

def page_header(title, subtitle=None, icon_name=None):
    """
    Create a premium page header
    
    Args:
        title: Page title
        subtitle: Optional subtitle
        icon_name: Icon name from ICONS dict
    """
    import streamlit as st
    
    icon_html = icon(icon_name, size='2x', color=COLORS['primary']) if icon_name else ''
    subtitle_html = f'<p style="color: {COLORS["gray_600"]}; font-size: 1.1rem; margin-top: 0.5rem;">{subtitle}</p>' if subtitle else ''
    
    st.markdown(f"""
    <div style="margin-bottom: 2rem;">
        <h1 style="display: flex; align-items: center; gap: 1rem; color: {COLORS['gray_800']};">
            {icon_html} {title}
        </h1>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)
