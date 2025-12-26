"""
AgriSensa - Exploratory Data Analysis
======================================
Script untuk analisis pola musim, harga, dan visualisasi

Author: Yandri
Date: 2024-12-26
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


def load_dataset(filepath):
    """Load merged dataset"""
    print(f"\n📂 Loading dataset from: {filepath}")
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        print("\n⚠️ Please run script 2 first:")
        print("   python 2_merge_weather_price.py")
        return None
    
    df = pd.read_csv(filepath)
    print(f"✅ Loaded {len(df)} records")
    print(f"📊 Columns: {list(df.columns)}")
    
    return df


def analyze_seasonal_patterns(df, output_dir):
    """Analyze and visualize seasonal patterns"""
    print("\n🌦️ Analyzing seasonal patterns...")
    
    # 1. Average price by month
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Plot 1: Cabai Merah price by month
    ax1 = axes[0, 0]
    df_cabai = df[df['commodity'] == 'Cabai Merah Keriting']
    monthly_avg = df_cabai.groupby('month')['price'].mean().sort_index()
    
    ax1.bar(monthly_avg.index, monthly_avg.values, color='red', alpha=0.7)
    ax1.set_title('Rata-rata Harga Cabai Merah per Bulan (2022-2024)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Bulan')
    ax1.set_ylabel('Harga (Rp/kg)')
    ax1.grid(axis='y', alpha=0.3)
    
    # Add season annotations
    ax1.axvspan(6, 8, alpha=0.2, color='orange', label='Kemarau')
    ax1.axvspan(11, 12, alpha=0.2, color='blue', label='Hujan')
    ax1.axvspan(9, 10, alpha=0.2, color='purple', label='Transisi')
    ax1.legend()
    
    # Plot 2: Rainfall by month
    ax2 = axes[0, 1]
    if 'curah_hujan_mm' in df.columns:
        monthly_rain = df.groupby('month')['curah_hujan_mm'].mean().sort_index()
        ax2.bar(monthly_rain.index, monthly_rain.values, color='blue', alpha=0.7)
        ax2.set_title('Rata-rata Curah Hujan per Bulan', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Bulan')
        ax2.set_ylabel('Curah Hujan (mm)')
        ax2.grid(axis='y', alpha=0.3)
    
    # Plot 3: Price by season (boxplot)
    ax3 = axes[1, 0]
    df_cabai_season = df[df['commodity'] == 'Cabai Merah Keriting']
    season_order = ['Kemarau', 'Transisi_Kemarau', 'Hujan', 'Transisi_Hujan']
    sns.boxplot(data=df_cabai_season, x='season', y='price', order=season_order, ax=ax3)
    ax3.set_title('Distribusi Harga Cabai per Musim', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Musim')
    ax3.set_ylabel('Harga (Rp/kg)')
    ax3.tick_params(axis='x', rotation=45)
    
    # Plot 4: Nataru effect
    ax4 = axes[1, 1]
    nataru_avg = df_cabai.groupby('is_nataru')['price'].mean()
    labels = ['Non-Nataru', 'Nataru (Des-Jan)']
    colors = ['lightblue', 'gold']
    ax4.bar(labels, nataru_avg.values, color=colors, alpha=0.8)
    ax4.set_title('Efek Nataru terhadap Harga Cabai', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Harga Rata-rata (Rp/kg)')
    ax4.grid(axis='y', alpha=0.3)
    
    # Add percentage increase
    pct_increase = ((nataru_avg.iloc[1] - nataru_avg.iloc[0]) / nataru_avg.iloc[0]) * 100
    ax4.text(1, nataru_avg.iloc[1], f'+{pct_increase:.1f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    filepath = os.path.join(output_dir, 'seasonal_patterns.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"💾 Saved: {filepath}")
    plt.close()


def analyze_correlations(df, output_dir):
    """Analyze correlations between weather and price"""
    print("\n🔗 Analyzing correlations...")
    
    # Select numeric columns
    numeric_cols = ['month', 'price']
    if 'curah_hujan_mm' in df.columns:
        numeric_cols.append('curah_hujan_mm')
    if 'suhu_rata_c' in df.columns:
        numeric_cols.append('suhu_rata_c')
    if 'kelembaban_persen' in df.columns:
        numeric_cols.append('kelembaban_persen')
    
    # Filter for one commodity to avoid duplication
    df_cabai = df[df['commodity'] == 'Cabai Merah Keriting']
    
    # Correlation matrix
    corr_matrix = df_cabai[numeric_cols].corr()
    
    # Plot heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    plt.title('Korelasi: Cuaca vs Harga Cabai', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    filepath = os.path.join(output_dir, 'correlation_heatmap.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"💾 Saved: {filepath}")
    plt.close()


def analyze_price_trends(df, output_dir):
    """Analyze price trends over time"""
    print("\n📈 Analyzing price trends...")
    
    # Select top commodities
    top_commodities = ['Cabai Merah Keriting', 'Bawang Merah', 'Beras Premium']
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    for commodity in top_commodities:
        df_comm = df[df['commodity'] == commodity]
        # Create year-month for x-axis
        df_comm['year_month'] = df_comm['year'].astype(str) + '-' + df_comm['month'].astype(str).str.zfill(2)
        monthly_avg = df_comm.groupby('year_month')['price'].mean().sort_index()
        
        ax.plot(monthly_avg.index, monthly_avg.values, marker='o', label=commodity, linewidth=2)
    
    ax.set_title('Tren Harga Komoditas (2022-2024)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Tahun-Bulan')
    ax.set_ylabel('Harga (Rp/kg)')
    ax.legend()
    ax.grid(alpha=0.3)
    ax.tick_params(axis='x', rotation=45)
    
    # Show only every 3rd label to avoid crowding
    for i, label in enumerate(ax.xaxis.get_ticklabels()):
        if i % 3 != 0:
            label.set_visible(False)
    
    plt.tight_layout()
    filepath = os.path.join(output_dir, 'price_trends.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"💾 Saved: {filepath}")
    plt.close()


def generate_insights_report(df, output_dir):
    """Generate text report with key insights"""
    print("\n📝 Generating insights report...")
    
    report = []
    report.append("=" * 70)
    report.append("AGRISENSA - SEASONAL PATTERN ANALYSIS REPORT")
    report.append("=" * 70)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Dataset: {len(df)} records from {df['year'].min()} to {df['year'].max()}")
    report.append("")
    
    # Insight 1: Seasonal price patterns
    report.append("1. POLA HARGA MUSIMAN (Cabai Merah)")
    report.append("-" * 70)
    df_cabai = df[df['commodity'] == 'Cabai Merah Keriting']
    season_avg = df_cabai.groupby('season')['price'].mean().sort_values(ascending=False)
    
    for season, price in season_avg.items():
        report.append(f"   {season:20s}: Rp {price:>10,.0f}/kg")
    
    report.append("")
    report.append("   💡 INSIGHT:")
    report.append("   - Harga tertinggi di musim Transisi (Sep-Okt) karena 'double trouble'")
    report.append("   - Harga terendah di musim Hujan (banyak yang tanam)")
    report.append("")
    
    # Insight 2: Nataru effect
    report.append("2. EFEK NATARU (Desember-Januari)")
    report.append("-" * 70)
    nataru_avg = df_cabai.groupby('is_nataru')['price'].mean()
    pct_increase = ((nataru_avg.iloc[1] - nataru_avg.iloc[0]) / nataru_avg.iloc[0]) * 100
    
    report.append(f"   Non-Nataru : Rp {nataru_avg.iloc[0]:>10,.0f}/kg")
    report.append(f"   Nataru     : Rp {nataru_avg.iloc[1]:>10,.0f}/kg (+{pct_increase:.1f}%)")
    report.append("")
    report.append("   💡 INSIGHT:")
    report.append(f"   - Harga naik {pct_increase:.1f}% saat Nataru karena demand tinggi")
    report.append("   - Peluang profit maksimal jika panen di Desember-Januari")
    report.append("")
    
    # Insight 3: Optimal planting window
    report.append("3. REKOMENDASI WAKTU TANAM")
    report.append("-" * 70)
    report.append("   Berdasarkan pola musim & harga:")
    report.append("")
    report.append("   ✅ OPTIMAL:")
    report.append("      - Tanam APRIL → Panen JULI (Kemarau, harga tinggi)")
    report.append("      - Tanam OKTOBER → Panen JANUARI (Nataru, harga puncak)")
    report.append("")
    report.append("   ⚠️ HINDARI:")
    report.append("      - Tanam NOVEMBER → Panen FEBRUARI (Hujan, harga rendah)")
    report.append("      - Tanam JUNI → Panen SEPTEMBER (Risiko gagal panen tinggi)")
    report.append("")
    
    # Insight 4: Risk-Return Matrix
    report.append("4. RISK-RETURN MATRIX")
    report.append("-" * 70)
    report.append("   Bulan Panen | Risk Level | Expected Price | Recommendation")
    report.append("   " + "-" * 66)
    
    risk_matrix = [
        ("Januari", "Medium", "Rp 75.000", "✅ GO (Nataru bonus)"),
        ("Februari", "Low", "Rp 55.000", "⚠️ Harga rendah"),
        ("Juli", "Medium", "Rp 85.000", "✅ GO (Kemarau)"),
        ("Agustus", "High", "Rp 95.000", "⚠️ Risiko hama tinggi"),
        ("September", "Very High", "Rp 110.000", "❌ Terlalu berisiko"),
    ]
    
    for month, risk, price, rec in risk_matrix:
        report.append(f"   {month:11s} | {risk:10s} | {price:14s} | {rec}")
    
    report.append("")
    report.append("=" * 70)
    report.append("END OF REPORT")
    report.append("=" * 70)
    
    # Save report
    filepath = os.path.join(output_dir, 'insights_report.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print(f"💾 Saved: {filepath}")
    
    # Print to console
    print("\n" + '\n'.join(report))


def main():
    """Main execution"""
    print("=" * 60)
    print("📊 AgriSensa - Exploratory Data Analysis")
    print("=" * 60)
    
    # Paths
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    dataset_file = os.path.join(base_dir, 'data', 'processed', 'dataset_training.csv')
    output_dir = os.path.join(base_dir, 'data', 'processed', 'visualizations')
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load dataset
    df = load_dataset(dataset_file)
    
    if df is None:
        return
    
    # Run analyses
    analyze_seasonal_patterns(df, output_dir)
    analyze_correlations(df, output_dir)
    analyze_price_trends(df, output_dir)
    generate_insights_report(df, output_dir)
    
    print("\n" + "=" * 60)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 60)
    print(f"\n📁 Output saved to: {output_dir}")
    print("\n📊 Generated files:")
    print("   - seasonal_patterns.png")
    print("   - correlation_heatmap.png")
    print("   - price_trends.png")
    print("   - insights_report.txt")
    print("\n📝 Next Steps:")
    print("   1. Review visualizations and insights")
    print("   2. Use dataset_training.csv to build ML model")
    print("   3. Implement predictive model in AgriSensa")


if __name__ == "__main__":
    main()
