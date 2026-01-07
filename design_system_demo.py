import streamlit as st
import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils.design_system import *

st.set_page_config(
    page_title="Design System - AgriSensa", 
    page_icon="🎨", 
    layout="wide"
)

# Apply design system
apply_design_system()

# Header
create_header(
    "🎨 AgriSensa Design System", 
    "Komponen UI yang konsisten, modern, dan profesional untuk semua modul AgriSensa",
    "🎨"
)

# Breadcrumb
create_breadcrumb(["Home", "Utils", "Design System Demo"])

st.markdown("---")

# Introduction
st.markdown("""
### 📖 Tentang Design System

Design system ini menyediakan **komponen UI yang konsisten** untuk semua modul AgriSensa. 
Dengan menggunakan design system, kita memastikan:

- ✅ **Konsistensi visual** di seluruh platform
- ✅ **Development lebih cepat** dengan komponen reusable
- ✅ **Maintenance lebih mudah** dengan centralized styling
- ✅ **User experience lebih baik** dengan interface yang familiar
""")

st.markdown("---")

# ============================================================================
# COLOR PALETTE
# ============================================================================

create_section_header("Color Palette", "🎨")

st.markdown("#### Primary Colors")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div style='background: {COLORS['primary']}; padding: 2rem; border-radius: {BORDER_RADIUS['lg']}; color: white; text-align: center; box-shadow: {SHADOWS['md']};'>
        <strong style='font-size: 1.2rem;'>Primary</strong><br>
        <code style='background: rgba(255,255,255,0.2); padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-size: 0.875rem;'>{COLORS['primary']}</code>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style='background: {COLORS['secondary']}; padding: 2rem; border-radius: {BORDER_RADIUS['lg']}; color: white; text-align: center; box-shadow: {SHADOWS['md']};'>
        <strong style='font-size: 1.2rem;'>Secondary</strong><br>
        <code style='background: rgba(255,255,255,0.2); padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-size: 0.875rem;'>{COLORS['secondary']}</code>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style='background: {COLORS['accent']}; padding: 2rem; border-radius: {BORDER_RADIUS['lg']}; color: white; text-align: center; box-shadow: {SHADOWS['md']};'>
        <strong style='font-size: 1.2rem;'>Accent</strong><br>
        <code style='background: rgba(255,255,255,0.2); padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-size: 0.875rem;'>{COLORS['accent']}</code>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style='background: {COLORS['success']}; padding: 2rem; border-radius: {BORDER_RADIUS['lg']}; color: white; text-align: center; box-shadow: {SHADOWS['md']};'>
        <strong style='font-size: 1.2rem;'>Success</strong><br>
        <code style='background: rgba(255,255,255,0.2); padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-size: 0.875rem;'>{COLORS['success']}</code>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("#### Semantic Colors")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div style='background: {COLORS['info']}; padding: 1.5rem; border-radius: {BORDER_RADIUS['md']}; color: white; text-align: center;'>
        <strong>Info</strong><br><small>{COLORS['info']}</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style='background: {COLORS['warning']}; padding: 1.5rem; border-radius: {BORDER_RADIUS['md']}; color: white; text-align: center;'>
        <strong>Warning</strong><br><small>{COLORS['warning']}</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style='background: {COLORS['error']}; padding: 1.5rem; border-radius: {BORDER_RADIUS['md']}; color: white; text-align: center;'>
        <strong>Error</strong><br><small>{COLORS['error']}</small>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style='background: {COLORS['dark']}; padding: 1.5rem; border-radius: {BORDER_RADIUS['md']}; color: white; text-align: center;'>
        <strong>Dark</strong><br><small>{COLORS['dark']}</small>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# TYPOGRAPHY
# ============================================================================

create_section_header("Typography", "📝")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Font Sizes")
    st.markdown(f"""
    <div style='background: white; padding: 1.5rem; border-radius: {BORDER_RADIUS['md']}; box-shadow: {SHADOWS['sm']};'>
        <p style='font-size: {FONT_SIZES['xs']}; margin: 0.5rem 0;'>Extra Small (xs) - {FONT_SIZES['xs']}</p>
        <p style='font-size: {FONT_SIZES['sm']}; margin: 0.5rem 0;'>Small (sm) - {FONT_SIZES['sm']}</p>
        <p style='font-size: {FONT_SIZES['base']}; margin: 0.5rem 0;'>Base - {FONT_SIZES['base']}</p>
        <p style='font-size: {FONT_SIZES['lg']}; margin: 0.5rem 0;'>Large (lg) - {FONT_SIZES['lg']}</p>
        <p style='font-size: {FONT_SIZES['xl']}; margin: 0.5rem 0;'>Extra Large (xl) - {FONT_SIZES['xl']}</p>
        <p style='font-size: {FONT_SIZES['2xl']}; margin: 0.5rem 0;'>2XL - {FONT_SIZES['2xl']}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("#### Font Weights")
    st.markdown(f"""
    <div style='background: white; padding: 1.5rem; border-radius: {BORDER_RADIUS['md']}; box-shadow: {SHADOWS['sm']};'>
        <p style='font-weight: {FONT_WEIGHTS['light']}; margin: 0.5rem 0;'>Light (300)</p>
        <p style='font-weight: {FONT_WEIGHTS['normal']}; margin: 0.5rem 0;'>Normal (400)</p>
        <p style='font-weight: {FONT_WEIGHTS['medium']}; margin: 0.5rem 0;'>Medium (500)</p>
        <p style='font-weight: {FONT_WEIGHTS['semibold']}; margin: 0.5rem 0;'>Semibold (600)</p>
        <p style='font-weight: {FONT_WEIGHTS['bold']}; margin: 0.5rem 0;'>Bold (700)</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# COMPONENTS
# ============================================================================

create_section_header("UI Components", "🧩")

# Metric Cards
st.markdown("### Metric Cards")
st.markdown("Digunakan untuk menampilkan statistik dan KPI penting")

col1, col2, col3, col4 = st.columns(4)

with col1:
    create_metric_card("Total Panen", "1,234 kg", "↑ 12% vs bulan lalu", "🌾")

with col2:
    create_metric_card("Pendapatan", "Rp 15.5 juta", "↑ 8% vs bulan lalu", "💰")

with col3:
    create_metric_card("Luas Lahan", "2.5 ha", "→ Tidak berubah", "📏")

with col4:
    create_metric_card("Petani Aktif", "156 orang", "↑ 23 petani baru", "👨‍🌾")

st.markdown("```python")
st.code("""
create_metric_card("Total Panen", "1,234 kg", "↑ 12% vs bulan lalu", "🌾")
""", language='python')

st.markdown("---")

# Info Boxes
st.markdown("### Info Boxes")
st.markdown("Digunakan untuk menampilkan informasi, peringatan, atau notifikasi")

create_info_box("ℹ️ <strong>Info:</strong> Ini adalah info box untuk menampilkan informasi umum kepada pengguna.", "info")
create_info_box("✅ <strong>Success:</strong> Operasi berhasil dilakukan! Data telah tersimpan dengan baik.", "success")
create_info_box("⚠️ <strong>Warning:</strong> Perhatian diperlukan! Pastikan data sudah benar sebelum melanjutkan.", "warning")

st.markdown("```python")
st.code("""
create_info_box("ℹ️ <strong>Info:</strong> Pesan info", "info")
create_info_box("✅ <strong>Success:</strong> Pesan sukses", "success")
create_info_box("⚠️ <strong>Warning:</strong> Pesan peringatan", "warning")
""", language='python')

st.markdown("---")

# Statistics Row
st.markdown("### Statistics Row")
st.markdown("Digunakan untuk menampilkan beberapa metrik dalam satu baris")

create_stat_row([
    {'label': 'Petani Aktif', 'value': '1,234', 'icon': '👨‍🌾', 'delta': '+12%'},
    {'label': 'Lahan Total', 'value': '567 ha', 'icon': '🌾', 'delta': '+5%'},
    {'label': 'Produksi', 'value': '890 ton', 'icon': '📦', 'delta': '+18%'},
    {'label': 'Revenue', 'value': 'Rp 1.2M', 'icon': '💰', 'delta': '+23%'},
])

st.markdown("```python")
st.code("""
create_stat_row([
    {'label': 'Petani Aktif', 'value': '1,234', 'icon': '👨‍🌾', 'delta': '+12%'},
    {'label': 'Lahan Total', 'value': '567 ha', 'icon': '🌾', 'delta': '+5%'},
    {'label': 'Produksi', 'value': '890 ton', 'icon': '📦', 'delta': '+18%'},
])
""", language='python')

st.markdown("---")

# ============================================================================
# USAGE GUIDE
# ============================================================================

create_section_header("Usage Guide", "📚")

st.markdown("""
### Cara Menggunakan Design System

#### 1. Import Design System

```python
import streamlit as st
from utils.design_system import *

# Apply global styles
apply_design_system()
```

#### 2. Gunakan Components

```python
# Header
create_header("Judul Halaman", "Subtitle opsional", "🌾")

# Breadcrumb
create_breadcrumb(["Home", "Category", "Page"])

# Section Header
create_section_header("Section Title", "📊")

# Metric Card
create_metric_card("Label", "1,234", "↑ 12%", "📊")

# Info Box
create_info_box("Pesan informasi", "info")

# Footer
create_footer()
```

#### 3. Akses Design Tokens

```python
# Colors
primary_color = get_color('primary')
success_color = get_color('success')

# Gradients
primary_gradient = get_gradient('primary')
```

### Best Practices

✅ **DO:**
- Gunakan design system components untuk konsistensi
- Ikuti color palette yang sudah ditentukan
- Gunakan spacing scale untuk margin/padding
- Gunakan typography scale untuk font sizes

❌ **DON'T:**
- Jangan buat inline CSS untuk styling yang sudah ada di design system
- Jangan gunakan warna random di luar palette
- Jangan gunakan font sizes arbitrary
- Jangan duplikasi component code
""")

st.markdown("---")

# Footer
create_footer("🎨 AgriSensa Design System v1.0 - Dibuat untuk konsistensi UI/UX yang lebih baik")
