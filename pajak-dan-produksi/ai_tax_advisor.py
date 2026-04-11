import re
from datetime import datetime
import json

# Tax Knowledge Base
TAX_KNOWLEDGE = {
    'pph_badan': {
        'title': 'PPh Badan - Pajak Penghasilan Badan',
        'tarif': {
            'umkm': '0.5% (final) untuk omzet < Rp 4.8 Miliar',
            'non_umkm': '22% dari Penghasilan Kena Pajak'
        },
        'strategies': [
            'Manfaatkan fasilitas UMKM jika omzet < Rp 4.8M per tahun',
            'Optimalkan koreksi fiskal untuk mengurangi Penghasilan Kena Pajak',
            'Maksimalkan kredit pajak (PPh 22, 23, 25)',
            'Timing pengakuan pendapatan dan biaya untuk tax planning',
            'Manfaatkan insentif pajak untuk sektor tertentu'
        ],
        'tips': [
            'Dokumentasikan semua biaya yang deductible',
            'Review koreksi fiskal setiap bulan',
            'Bayar PPh 25 tepat waktu untuk hindari sanksi',
            'Konsultasi dengan konsultan pajak untuk strategi kompleks'
        ]
    },
    'umkm': {
        'title': 'UMKM - Usaha Mikro Kecil Menengah',
        'eligibility': {
            'kriteria': 'Omzet bruto tidak lebih dari Rp 4.8 Miliar per tahun',
            'tarif': '0.5% dari omzet bruto (PPh Final)',
            'benefit': 'Lebih rendah dari tarif PPh Badan 22%'
        },
        'cara_apply': [
            'Pastikan omzet tahunan < Rp 4.8 Miliar',
            'Laporkan dalam SPT Tahunan',
            'Bayar PPh Final 0.5% setiap bulan',
            'Simpan bukti pembayaran untuk audit'
        ],
        'tips': [
            'Monitor omzet agar tidak melebihi threshold',
            'Jika mendekati Rp 4.8M, pertimbangkan strategi split bisnis',
            'Manfaatkan fasilitas ini selama masih eligible',
            'Siapkan transisi ke PPh Badan 22% jika omzet naik'
        ]
    },
    'production_cost': {
        'title': 'Optimasi Biaya Produksi',
        'margin_optimal': {
            'industri_umum': '20-30% untuk sustainability',
            'retail': '30-50% untuk cover overhead',
            'manufaktur': '15-25% competitive pricing'
        },
        'strategies': [
            'Analisis break-even point untuk menentukan volume minimum',
            'Optimasi biaya bahan baku dengan bulk purchasing',
            'Efisiensi tenaga kerja dengan automation',
            'Review overhead costs secara berkala',
            'Pricing strategy: cost-plus vs market-based'
        ],
        'calculation': {
            'break_even': 'Fixed Cost / (Harga Jual - Variable Cost per Unit)',
            'margin': '(Harga Jual - Total Cost) / Harga Jual × 100%',
            'markup': '(Harga Jual - Cost) / Cost × 100%'
        }
    },
    'tax_planning': {
        'title': 'Tax Planning Strategies',
        'timing': [
            'Bayar pajak sebelum jatuh tempo untuk hindari denda',
            'Atur timing pengakuan pendapatan (accrual vs cash basis)',
            'Maksimalkan biaya di akhir tahun untuk kurangi PKP',
            'Rencanakan investasi untuk manfaatkan depresiasi'
        ],
        'structure': [
            'Pertimbangkan struktur badan usaha (PT, CV, UD)',
            'Evaluasi benefit UMKM vs PPh Badan',
            'Pisahkan bisnis jika ada multiple revenue streams',
            'Manfaatkan holding company untuk tax efficiency'
        ],
        'deductions': [
            'Maksimalkan biaya operasional yang deductible',
            'Dokumentasikan semua pengeluaran bisnis',
            'Manfaatkan biaya R&D untuk tax credit',
            'Review entertainment & travel expenses'
        ]
    },
    'pph_21': {
        'title': 'PPh 21 - Pajak Penghasilan Karyawan',
        'info': 'Pajak yang dipotong dari gaji karyawan',
        'tips': [
            'Optimalkan PTKP sesuai status (menikah/tanggungan)',
            'Manfaatkan tunjangan non-taxable (transport, makan)',
            'Atur timing bonus untuk optimasi pajak tahunan',
            'Review slip gaji untuk pastikan perhitungan benar'
        ]
    },
    'ppn': {
        'title': 'PPN - Pajak Pertambahan Nilai',
        'tarif': '11% (sejak 2022)',
        'tips': [
            'Kelola faktur pajak masukan dan keluaran dengan baik',
            'Kompensasi PPN masukan dengan PPN keluaran',
            'Ajukan restitusi jika PPN masukan > keluaran',
            'Timing transaksi besar untuk optimasi cash flow'
        ]
    }
}

# Question Patterns
QUESTION_PATTERNS = {
    'pph_badan_reduce': [
        r'cara.*turun.*pph.*badan',
        r'menurunkan.*pph.*badan',
        r'hemat.*pph.*badan',
        r'kurangi.*pajak.*perusahaan'
    ],
    'umkm_eligible': [
        r'eligible.*umkm',
        r'syarat.*umkm',
        r'kriteria.*umkm',
        r'bisa.*umkm'
    ],
    'margin_optimal': [
        r'margin.*optimal',
        r'berapa.*margin',
        r'margin.*produksi',
        r'keuntungan.*ideal'
    ],
    'tax_planning': [
        r'tax.*planning',
        r'strategi.*pajak',
        r'perencanaan.*pajak',
        r'optimasi.*pajak'
    ],
    'pph_21': [
        r'pph.*21',
        r'pajak.*gaji',
        r'pajak.*karyawan'
    ],
    'ppn': [
        r'ppn',
        r'pajak.*pertambahan.*nilai',
        r'faktur.*pajak'
    ]
}

def get_ai_response(question, user_context=None):
    """
    Generate AI response based on question and context
    
    Args:
        question (str): User's question
        user_context (dict): User's calculation history and data
    
    Returns:
        str: AI-generated response
    """
    question_lower = question.lower()
    
    # Match question pattern
    topic = match_question_pattern(question_lower)
    
    if topic == 'pph_badan_reduce':
        return generate_pph_badan_reduction_advice(user_context)
    elif topic == 'umkm_eligible':
        return generate_umkm_eligibility_check(user_context)
    elif topic == 'margin_optimal':
        return generate_margin_optimization_advice(user_context)
    elif topic == 'tax_planning':
        return generate_tax_planning_advice(user_context)
    elif topic == 'pph_21':
        return get_tax_knowledge('pph_21')
    elif topic == 'ppn':
        return get_tax_knowledge('ppn')
    else:
        return generate_general_response(question, user_context)

def match_question_pattern(question):
    """Match question to predefined patterns"""
    for topic, patterns in QUESTION_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, question):
                return topic
    return None

def generate_pph_badan_reduction_advice(user_context=None):
    """Generate advice for reducing PPh Badan"""
    knowledge = TAX_KNOWLEDGE['pph_badan']
    
    response = f"""## 💡 Strategi Menurunkan PPh Badan 2025

Berikut beberapa strategi efektif untuk menurunkan beban PPh Badan:

### 🎯 Strategi Utama:

"""
    
    for i, strategy in enumerate(knowledge['strategies'], 1):
        response += f"{i}. **{strategy}**\n"
    
    response += f"\n### 📊 Tarif PPh Badan:\n"
    response += f"- UMKM: {knowledge['tarif']['umkm']}\n"
    response += f"- Non-UMKM: {knowledge['tarif']['non_umkm']}\n"
    
    response += f"\n### ✅ Tips Praktis:\n"
    for tip in knowledge['tips']:
        response += f"- {tip}\n"
    
    if user_context and 'omzet' in user_context:
        omzet = user_context['omzet']
        if omzet < 4800000000:
            response += f"\n### 🎉 Rekomendasi untuk Anda:\n"
            response += f"Berdasarkan omzet Anda (Rp {omzet:,.0f}), Anda **ELIGIBLE untuk fasilitas UMKM**!\n"
            response += f"Manfaatkan tarif PPh Final 0.5% untuk hemat pajak signifikan.\n"
    
    response += f"\n⚠️ **Catatan:** Konsultasikan dengan konsultan pajak untuk strategi yang sesuai dengan kondisi bisnis Anda."
    
    return response

def generate_umkm_eligibility_check(user_context=None):
    """Check UMKM eligibility"""
    knowledge = TAX_KNOWLEDGE['umkm']
    
    response = f"""## 🏢 Eligibilitas UMKM

### 📋 Kriteria UMKM:
- {knowledge['eligibility']['kriteria']}
- Tarif: {knowledge['eligibility']['tarif']}
- Benefit: {knowledge['eligibility']['benefit']}

"""
    
    if user_context and 'omzet' in user_context:
        omzet = user_context['omzet']
        threshold = 4800000000
        
        if omzet < threshold:
            sisa = threshold - omzet
            response += f"### ✅ **ANDA ELIGIBLE UNTUK UMKM!**\n\n"
            response += f"- Omzet Anda: Rp {omzet:,.0f}\n"
            response += f"- Threshold UMKM: Rp {threshold:,.0f}\n"
            response += f"- Sisa ruang: Rp {sisa:,.0f}\n\n"
            response += f"💡 **Rekomendasi:** Manfaatkan tarif PPh Final 0.5% untuk maksimalkan profit!\n"
        else:
            kelebihan = omzet - threshold
            response += f"### ❌ **TIDAK ELIGIBLE UNTUK UMKM**\n\n"
            response += f"- Omzet Anda: Rp {omzet:,.0f}\n"
            response += f"- Threshold UMKM: Rp {threshold:,.0f}\n"
            response += f"- Kelebihan: Rp {kelebihan:,.0f}\n\n"
            response += f"💡 **Rekomendasi:** Pertimbangkan strategi split bisnis atau gunakan PPh Badan 22%.\n"
    else:
        response += f"### 📝 Cara Mengecek Eligibilitas:\n"
        for i, step in enumerate(knowledge['cara_apply'], 1):
            response += f"{i}. {step}\n"
    
    response += f"\n### 💡 Tips:\n"
    for tip in knowledge['tips']:
        response += f"- {tip}\n"
    
    return response

def generate_margin_optimization_advice(user_context=None):
    """Generate margin optimization advice"""
    knowledge = TAX_KNOWLEDGE['production_cost']
    
    response = f"""## 📊 Optimasi Margin Produksi

### 🎯 Margin Optimal per Industri:

"""
    
    for industry, margin in knowledge['margin_optimal'].items():
        response += f"- **{industry.replace('_', ' ').title()}**: {margin}\n"
    
    response += f"\n### 💡 Strategi Optimasi:\n"
    for i, strategy in enumerate(knowledge['strategies'], 1):
        response += f"{i}. {strategy}\n"
    
    response += f"\n### 📐 Formula Penting:\n"
    for calc_type, formula in knowledge['calculation'].items():
        response += f"- **{calc_type.replace('_', ' ').title()}**: {formula}\n"
    
    if user_context and 'biaya_produksi' in user_context:
        total_cost = user_context['biaya_produksi']
        # Recommend margin based on industry average
        recommended_margin = 0.25  # 25%
        recommended_price = total_cost / (1 - recommended_margin)
        
        response += f"\n### 🎯 Rekomendasi untuk Anda:\n"
        response += f"- Total Biaya Produksi: Rp {total_cost:,.0f}\n"
        response += f"- Margin Rekomendasi: 25%\n"
        response += f"- Harga Jual Optimal: Rp {recommended_price:,.0f}\n"
        response += f"- Profit per Unit: Rp {(recommended_price - total_cost):,.0f}\n"
    
    return response

def generate_tax_planning_advice(user_context=None):
    """Generate tax planning advice"""
    knowledge = TAX_KNOWLEDGE['tax_planning']
    
    response = f"""## 📅 Tax Planning Strategies

### ⏰ Timing Strategies:
"""
    for tip in knowledge['timing']:
        response += f"- {tip}\n"
    
    response += f"\n### 🏗️ Structure Optimization:\n"
    for tip in knowledge['structure']:
        response += f"- {tip}\n"
    
    response += f"\n### 💰 Maximizing Deductions:\n"
    for tip in knowledge['deductions']:
        response += f"- {tip}\n"
    
    response += f"\n### 🎯 Action Plan:\n"
    response += f"1. **Q1**: Review struktur bisnis dan eligibilitas UMKM\n"
    response += f"2. **Q2**: Optimalkan biaya operasional yang deductible\n"
    response += f"3. **Q3**: Evaluasi timing pengakuan pendapatan\n"
    response += f"4. **Q4**: Maksimalkan biaya sebelum tutup buku\n"
    
    return response

def get_tax_knowledge(topic):
    """Get knowledge from database"""
    if topic not in TAX_KNOWLEDGE:
        return "Maaf, saya belum memiliki informasi tentang topik tersebut."
    
    knowledge = TAX_KNOWLEDGE[topic]
    response = f"## {knowledge['title']}\n\n"
    
    if 'info' in knowledge:
        response += f"{knowledge['info']}\n\n"
    
    if 'tarif' in knowledge:
        if isinstance(knowledge['tarif'], dict):
            response += "### Tarif:\n"
            for key, value in knowledge['tarif'].items():
                response += f"- {key}: {value}\n"
        else:
            response += f"### Tarif: {knowledge['tarif']}\n"
        response += "\n"
    
    if 'tips' in knowledge:
        response += "### Tips:\n"
        for tip in knowledge['tips']:
            response += f"- {tip}\n"
    
    return response

def generate_general_response(question, user_context=None):
    """Generate general response for unmatched questions"""
    response = f"""## 🤖 AI Tax Advisor

Terima kasih atas pertanyaan Anda: "{question}"

Saya dapat membantu Anda dengan topik-topik berikut:

### 💼 PPh Badan & UMKM
- Cara menurunkan PPh Badan
- Eligibilitas UMKM
- Strategi tax planning

### 📊 Biaya Produksi
- Margin optimal
- Break-even analysis
- Pricing strategies

### 📋 Pajak Lainnya
- PPh 21 (Pajak Karyawan)
- PPh 23 (Pajak Potong Pungut)
- PPN (Pajak Pertambahan Nilai)

💡 **Coba tanyakan:**
- "Bagaimana cara menurunkan PPh Badan 2025?"
- "Apakah saya eligible UMKM tahun depan?"
- "Berapa optimal margin untuk produksi?"

Atau klik salah satu pertanyaan yang disarankan di atas!
"""
    return response

def get_suggested_questions():
    """Get list of suggested questions"""
    return [
        {
            'category': 'PPh Badan & UMKM',
            'questions': [
                'Bagaimana cara menurunkan PPh Badan 2025?',
                'Apakah saya eligible UMKM tahun depan?',
                'Apa strategi tax planning terbaik untuk perusahaan?'
            ]
        },
        {
            'category': 'Biaya Produksi',
            'questions': [
                'Berapa optimal margin untuk produksi?',
                'Bagaimana cara hitung break-even point?',
                'Strategi pricing yang efektif?'
            ]
        },
        {
            'category': 'Pajak Lainnya',
            'questions': [
                'Apa bedanya PPh 21 dan PPh 23?',
                'Bagaimana cara optimasi PPN?',
                'Kapan waktu terbaik bayar pajak?'
            ]
        }
    ]
