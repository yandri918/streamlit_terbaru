from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas as pdf_canvas
from datetime import datetime
import io
import os

def generate_tax_report_pdf(calc_type, user_name, company_name, input_data, output_data, session_id=None):
    """
    Generate professional PDF report for tax calculation
    
    Args:
        calc_type (str): Type of tax calculation
        user_name (str): User name
        company_name (str): Company name
        input_data (dict): Input parameters
        output_data (dict): Calculation results
        session_id (str): Session ID for tracking
    
    Returns:
        bytes: PDF file as bytes
    """
    # Create PDF buffer
    buffer = io.BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2.5*cm,
        leftMargin=2.5*cm,
        topMargin=2.5*cm,
        bottomMargin=2.5*cm
    )
    
    # Container for PDF elements
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#764ba2'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        fontName='Helvetica'
    )
    
    # Header
    elements.append(Paragraph("LAPORAN PERHITUNGAN PAJAK", title_style))
    elements.append(Paragraph(f"<b>{calc_type}</b>", ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#667eea'),
        alignment=TA_CENTER,
        spaceAfter=20
    )))
    
    # Info Box
    info_data = [
        ['Tanggal', datetime.now().strftime('%d %B %Y, %H:%M:%S')],
        ['User', user_name or 'Anonymous'],
        ['Perusahaan', company_name or 'N/A'],
        ['Session ID', session_id or 'N/A']
    ]
    
    info_table = Table(info_data, colWidths=[4*cm, 10*cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(info_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # Ringkasan Eksekutif
    elements.append(Paragraph("RINGKASAN EKSEKUTIF", heading_style))
    
    # Get main tax value based on calc_type
    tax_amount = get_main_tax_value(calc_type, output_data)
    
    summary_data = [
        ['Jenis Pajak', calc_type],
        ['PAJAK TERUTANG', f"Rp {tax_amount:,.0f}"],
    ]
    
    summary_table = Table(summary_data, colWidths=[6*cm, 8*cm])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8eaf6')),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTSIZE', (0, 1), (-1, 1), 16),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#667eea')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    
    elements.append(summary_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # Detail Input
    elements.append(Paragraph("DETAIL INPUT PARAMETERS", heading_style))
    
    input_table_data = [['Parameter', 'Nilai']]
    for key, value in input_data.items():
        formatted_key = key.replace('_', ' ').title()
        if isinstance(value, (int, float)):
            formatted_value = f"Rp {value:,.0f}" if value > 1000 else str(value)
        else:
            formatted_value = str(value)
        input_table_data.append([formatted_key, formatted_value])
    
    input_table = Table(input_table_data, colWidths=[7*cm, 7*cm])
    input_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
    ]))
    
    elements.append(input_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # Detail Output
    elements.append(Paragraph("HASIL PERHITUNGAN", heading_style))
    
    output_table_data = [['Komponen', 'Nilai (Rp)']]
    for key, value in output_data.items():
        formatted_key = key.replace('_', ' ').title()
        if isinstance(value, (int, float)):
            formatted_value = f"{value:,.0f}"
        else:
            formatted_value = str(value)
        output_table_data.append([formatted_key, formatted_value])
    
    output_table = Table(output_table_data, colWidths=[7*cm, 7*cm])
    output_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#764ba2')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
    ]))
    
    elements.append(output_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # Rekomendasi Tax Planning
    elements.append(Paragraph("REKOMENDASI TAX PLANNING", heading_style))
    
    recommendations = get_tax_recommendations(calc_type, output_data)
    
    for i, rec in enumerate(recommendations, 1):
        elements.append(Paragraph(f"<b>{i}. {rec['title']}</b>", normal_style))
        elements.append(Paragraph(rec['description'], normal_style))
        elements.append(Spacer(1, 0.3*cm))
    
    # Footer/Disclaimer
    elements.append(Spacer(1, 1*cm))
    elements.append(Paragraph("DISCLAIMER", ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_JUSTIFY
    )))
    
    disclaimer_text = """
    Laporan ini adalah hasil perhitungan estimasi berdasarkan data yang diinput. 
    Untuk perhitungan resmi dan konsultasi perpajakan lebih lanjut, silakan hubungi 
    konsultan pajak profesional atau kantor pajak setempat. TaxPro Indonesia tidak 
    bertanggung jawab atas keputusan yang diambil berdasarkan laporan ini.
    """
    
    elements.append(Paragraph(disclaimer_text, ParagraphStyle(
        'DisclaimerText',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_JUSTIFY
    )))
    
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph(
        "Generated by <b>TaxPro Indonesia</b> | konsultasi@taxpro.id",
        ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#667eea'),
            alignment=TA_CENTER
        )
    ))
    
    # Build PDF
    doc.build(elements)
    
    # Get PDF bytes
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes

def get_main_tax_value(calc_type, output_data):
    """Get the main tax value based on calculation type"""
    tax_keys = {
        'PPh 21': 'pajak_bulanan',
        'PPh 23': 'pph23',
        'PPN': 'ppn',
        'PPh Badan': 'pph_badan',
        'PBB': 'pbb',
        'PKB': 'total',
        'BPHTB': 'bphtb'
    }
    
    key = tax_keys.get(calc_type, list(output_data.keys())[0])
    return output_data.get(key, 0)

def get_tax_recommendations(calc_type, output_data):
    """Get tax planning recommendations based on calculation type"""
    
    recommendations = {
        'PPh 21': [
            {
                'title': 'Optimasi PTKP',
                'description': 'Pastikan status PTKP sudah sesuai dengan kondisi aktual (menikah/tanggungan) untuk maksimalkan pengurangan pajak.'
            },
            {
                'title': 'Manfaatkan Tunjangan Non-Taxable',
                'description': 'Gunakan tunjangan yang tidak dikenakan pajak seperti tunjangan transport, makan, dan kesehatan sesuai ketentuan.'
            },
            {
                'title': 'Perencanaan Bonus',
                'description': 'Atur timing pembayaran bonus/THR untuk optimasi beban pajak tahunan.'
            }
        ],
        'PPh 23': [
            {
                'title': 'Kelengkapan NPWP',
                'description': 'Pastikan penerima penghasilan memiliki NPWP untuk menghindari tarif 100% lebih tinggi.'
            },
            {
                'title': 'Dokumentasi Lengkap',
                'description': 'Simpan bukti potong PPh 23 sebagai kredit pajak di SPT Tahunan.'
            },
            {
                'title': 'Verifikasi Jenis Jasa',
                'description': 'Pastikan klasifikasi jenis jasa sudah benar untuk penerapan tarif yang tepat.'
            }
        ],
        'PPN': [
            {
                'title': 'Kelola Faktur Pajak',
                'description': 'Pastikan faktur pajak masukan dan keluaran tercatat dengan baik untuk kompensasi PPN.'
            },
            {
                'title': 'Timing Transaksi',
                'description': 'Atur timing transaksi besar untuk optimasi cash flow terkait PPN.'
            },
            {
                'title': 'Restitusi PPN',
                'description': 'Jika PPN masukan lebih besar dari keluaran, ajukan restitusi sesuai prosedur.'
            }
        ],
        'PPh Badan': [
            {
                'title': 'Manfaatkan Fasilitas UMKM',
                'description': 'Jika omzet < 4.8M, manfaatkan tarif PPh final 0.5% untuk efisiensi pajak.'
            },
            {
                'title': 'Optimasi Koreksi Fiskal',
                'description': 'Review biaya-biaya yang dapat dikurangkan (deductible) untuk meminimalkan PKP.'
            },
            {
                'title': 'Tax Planning Strategis',
                'description': 'Pertimbangkan timing pengakuan pendapatan dan biaya untuk optimasi beban pajak.'
            },
            {
                'title': 'Kredit Pajak',
                'description': 'Manfaatkan PPh Pasal 22, 23, dan 25 sebagai kredit pajak untuk mengurangi PPh kurang bayar.'
            }
        ],
        'PBB': [
            {
                'title': 'Verifikasi NJOP',
                'description': 'Cek kesesuaian NJOP dengan harga pasar. Jika terlalu tinggi, ajukan keberatan ke kantor pajak.'
            },
            {
                'title': 'Bayar Tepat Waktu',
                'description': 'Bayar PBB sebelum jatuh tempo untuk hindari denda 2% per bulan.'
            },
            {
                'title': 'Manfaatkan NJOPTKP',
                'description': 'Pastikan NJOPTKP sudah diperhitungkan dengan benar sesuai ketentuan daerah.'
            }
        ],
        'PKB': [
            {
                'title': 'Perpanjangan Tepat Waktu',
                'description': 'Perpanjang STNK sebelum jatuh tempo untuk hindari denda dan biaya tambahan.'
            },
            {
                'title': 'Cek Tarif Progresif',
                'description': 'Untuk kendaraan kedua dan seterusnya, pertimbangkan tarif progresif yang lebih tinggi.'
            },
            {
                'title': 'Program Pemutihan',
                'description': 'Manfaatkan program pemutihan pajak kendaraan jika ada untuk hemat biaya denda.'
            }
        ],
        'BPHTB': [
            {
                'title': 'Verifikasi NPOPTKP',
                'description': 'Pastikan NPOPTKP sesuai ketentuan daerah untuk maksimalkan pengurangan pajak.'
            },
            {
                'title': 'Konsultasi Notaris',
                'description': 'Gunakan jasa notaris berpengalaman untuk memastikan perhitungan dan proses yang benar.'
            },
            {
                'title': 'Cek Harga Transaksi vs NJOP',
                'description': 'Dasar pengenaan menggunakan nilai tertinggi. Pastikan harga transaksi wajar.'
            }
        ]
    }
    
    return recommendations.get(calc_type, [
        {
            'title': 'Konsultasi Profesional',
            'description': 'Untuk optimasi pajak lebih lanjut, konsultasikan dengan konsultan pajak profesional.'
        }
    ])
