"""
Report Service — PDF/HTML Laporan Resmi Budidaya Krisan Pro
Generates official cultivation reports with letterhead.
"""
from datetime import datetime
from typing import Dict


def generate_report_html(batch: Dict, growth_records: list, harvest: Dict = None) -> str:
    """Generate HTML report with official letterhead for printing/PDF."""
    now = datetime.now()
    doc_number = f"KRISAN-{now.strftime('%Y%m%d%H%M%S')[:12]}"
    print_date = now.strftime("%d %B %Y, %H:%M WIB")
    batch_code = batch.get("batch_code", "-")
    variety = batch.get("variety_name", "-")
    planting_date = batch.get("planting_date", "-")
    target_harvest = batch.get("target_harvest_date", "-")
    land_area = batch.get("land_area_m2", 0)
    plant_count = batch.get("plant_count", 0)

    # Build growth table rows
    growth_rows = ""
    for r in growth_records:
        anomaly_icon = "⚠️" if r.get("anomaly_detected") else "✓"
        growth_rows += f"""
        <tr>
            <td>Minggu {r.get('week_number','')}</td>
            <td>{r.get('recording_date','')}</td>
            <td>{r.get('plant_height_cm','-')} cm</td>
            <td>{r.get('leaf_count','-')}</td>
            <td>{r.get('stem_diameter_mm','-')} mm</td>
            <td>{r.get('health_score','-')}</td>
            <td><strong>{r.get('ai_grade','C')}</strong></td>
            <td>{r.get('growth_deviation_pct','0')}%</td>
            <td>{anomaly_icon}</td>
        </tr>"""

    # Harvest section
    harvest_section = ""
    if harvest:
        gross = harvest.get("gross_revenue", 0)
        cost = harvest.get("production_cost", 0)
        profit = harvest.get("net_profit", 0)
        roi = harvest.get("roi_pct", 0)
        harvest_section = f"""
        <div class="section">
            <h3>📦 Data Hasil Panen</h3>
            <div class="kpi-row">
                <div class="kpi-box"><div class="kpi-label">Total Tangkai</div><div class="kpi-val">{harvest.get('total_stems',0):,}</div></div>
                <div class="kpi-box"><div class="kpi-label">Grade A</div><div class="kpi-val green">{harvest.get('grade_a_stems',0):,}</div></div>
                <div class="kpi-box"><div class="kpi-label">Omset Kotor</div><div class="kpi-val">Rp {gross:,}</div></div>
                <div class="kpi-box"><div class="kpi-label">Laba Bersih</div><div class="kpi-val blue">Rp {profit:,}</div></div>
                <div class="kpi-box"><div class="kpi-label">ROI</div><div class="kpi-val">{roi:.1f}%</div></div>
            </div>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Laporan Budidaya Krisan — {batch_code}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 12px; color: #1e293b; background: #fff; padding: 32px; }}
  .header {{ border-bottom: 3px double #10b981; padding-bottom: 16px; margin-bottom: 20px; text-align: center; }}
  .brand-icon {{ font-size: 36px; margin-bottom: 6px; }}
  .brand-name {{ font-size: 22px; font-weight: 800; color: #059669; letter-spacing: -0.02em; }}
  .brand-sub {{ font-size: 11px; color: #64748b; margin-top: 3px; }}
  .doc-info {{ display: flex; justify-content: space-between; font-size: 10px; color: #94a3b8; margin-top: 10px; border-top: 1px solid #e2e8f0; padding-top: 8px; }}
  .section {{ margin-bottom: 20px; }}
  .section h3 {{ font-size: 13px; font-weight: 700; color: #059669; margin-bottom: 10px; border-left: 3px solid #10b981; padding-left: 8px; }}
  .info-grid {{ display: grid; grid-template-columns: repeat(3,1fr); gap: 8px; margin-bottom: 12px; }}
  .info-item {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px; }}
  .info-label {{ font-size: 9px; color: #94a3b8; font-weight: 600; text-transform: uppercase; }}
  .info-val {{ font-size: 13px; font-weight: 700; color: #1e293b; margin-top: 2px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 11px; }}
  th {{ background: #f1faf5; color: #059669; font-weight: 700; padding: 8px; border: 1px solid #d1fae5; text-align: center; }}
  td {{ padding: 7px 8px; border: 1px solid #e2e8f0; text-align: center; }}
  tr:nth-child(even) td {{ background: #fafafa; }}
  .kpi-row {{ display: flex; gap: 10px; flex-wrap: wrap; }}
  .kpi-box {{ flex: 1; min-width: 120px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px 14px; }}
  .kpi-label {{ font-size: 9px; color: #94a3b8; text-transform: uppercase; font-weight: 600; }}
  .kpi-val {{ font-size: 16px; font-weight: 800; color: #1e293b; margin-top: 3px; }}
  .green {{ color: #059669 !important; }}
  .blue {{ color: #0284c7 !important; }}
  .footer {{ margin-top: 32px; border-top: 1px solid #e2e8f0; padding-top: 12px; text-align: center; font-size: 10px; color: #94a3b8; }}
  @media print {{
    body {{ padding: 16px; }}
    @page {{ margin: 1cm; }}
  }}
</style>
</head>
<body>

<div class="header">
  <div class="brand-icon">🌸</div>
  <div class="brand-name">BUDIDAYA KRISAN PRO</div>
  <div class="brand-sub">Sistem Cerdas Monitoring & Analitik Budidaya Krisan Spray Jepang | AI-Powered</div>
  <div class="brand-sub" style="margin-top:4px;">Standar Acuan: Balai Penelitian Tanaman Hias (Balithi) — Kementerian Pertanian RI</div>
  <div class="doc-info">
    <span>No. Dokumen: <strong>{doc_number}</strong></span>
    <span>Tanggal Cetak: {print_date}</span>
    <span>Status: Laporan Resmi</span>
  </div>
</div>

<div class="section">
  <h3>📋 Informasi Batch Tanam</h3>
  <div class="info-grid">
    <div class="info-item"><div class="info-label">Kode Batch</div><div class="info-val">{batch_code}</div></div>
    <div class="info-item"><div class="info-label">Varietas</div><div class="info-val">{variety}</div></div>
    <div class="info-item"><div class="info-label">Status</div><div class="info-val">{batch.get('status','active').upper()}</div></div>
    <div class="info-item"><div class="info-label">Tanggal Tanam</div><div class="info-val">{planting_date}</div></div>
    <div class="info-item"><div class="info-label">Target Panen</div><div class="info-val">{target_harvest}</div></div>
    <div class="info-item"><div class="info-label">Luas Lahan</div><div class="info-val">{land_area} m²</div></div>
    <div class="info-item"><div class="info-label">Jumlah Tanaman</div><div class="info-val">{plant_count:,}</div></div>
    <div class="info-item"><div class="info-label">Total Data Pertumbuhan</div><div class="info-val">{len(growth_records)} minggu</div></div>
    <div class="info-item"><div class="info-label">Catatan</div><div class="info-val">{batch.get('notes','-') or '-'}</div></div>
  </div>
</div>

<div class="section">
  <h3>📈 Riwayat Data Pertumbuhan Mingguan</h3>
  <table>
    <thead>
      <tr>
        <th>Minggu</th><th>Tanggal</th><th>Tinggi</th><th>Daun</th>
        <th>Diameter</th><th>Health Score</th><th>Grade AI</th>
        <th>Deviasi</th><th>Anomali</th>
      </tr>
    </thead>
    <tbody>
      {growth_rows if growth_rows else '<tr><td colspan="9">Belum ada data pertumbuhan</td></tr>'}
    </tbody>
  </table>
</div>

{harvest_section}

<div class="footer">
  <p>🌸 <strong>Budidaya Krisan Pro</strong> — AI-Powered Cultivation Platform | Laporan ini dibuat secara otomatis oleh sistem.</p>
  <p style="margin-top:4px;">Dikembangkan untuk mendukung digitalisasi pertanian bunga Indonesia 🇮🇩</p>
</div>

</body>
</html>"""
