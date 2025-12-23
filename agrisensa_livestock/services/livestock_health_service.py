"""
Livestock Health Monitoring Service
Comprehensive health management tools for precision livestock farming
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

# ==========================================
# 📊 BODY CONDITION SCORE (BCS) SYSTEM
# ==========================================

BCS_STANDARDS = {
    "Sapi Potong": {
        1: {
            "description": "Sangat Kurus (Emaciated)",
            "visual": "Tulang rusuk, pinggul, dan tulang belakang sangat menonjol",
            "recommendation": "Emergency feeding - tingkatkan energi 30-40%",
            "risk": "Tinggi - gangguan reproduksi, penurunan imunitas"
        },
        2: {
            "description": "Kurus (Thin)",
            "visual": "Tulang rusuk mudah terlihat, sedikit lemak punggung",
            "recommendation": "Tingkatkan konsentrat 20-30%",
            "risk": "Sedang - performa reproduksi suboptimal"
        },
        3: {
            "description": "Sedang (Moderate)",
            "visual": "Tulang rusuk teraba tapi tidak menonjol, lemak punggung tipis",
            "recommendation": "Pertahankan pakan saat ini - kondisi ideal",
            "risk": "Rendah - kondisi optimal untuk produksi"
        },
        4: {
            "description": "Gemuk (Fat)",
            "visual": "Tulang rusuk sulit diraba, lemak punggung tebal",
            "recommendation": "Kurangi konsentrat 15-20%, tingkatkan hijauan",
            "risk": "Sedang - risiko kesulitan melahirkan"
        },
        5: {
            "description": "Sangat Gemuk (Obese)",
            "visual": "Tulang tidak teraba, lemak berlebih di seluruh tubuh",
            "recommendation": "Diet ketat - kurangi energi 30%, tingkatkan serat",
            "risk": "Tinggi - metabolic disorders, calving difficulty"
        }
    },
    "Sapi Perah": {
        # 9-point scale for dairy cattle
        1: {"description": "Sangat Kurus", "stage": "Semua fase", "recommendation": "Emergency feeding"},
        2: {"description": "Kurus", "stage": "Semua fase", "recommendation": "Tingkatkan energi"},
        3: {"description": "Sedang-Kurus", "stage": "Laktasi awal", "recommendation": "Target ideal laktasi awal"},
        4: {"description": "Sedang", "stage": "Laktasi tengah", "recommendation": "Pertahankan"},
        5: {"description": "Sedang-Gemuk", "stage": "Laktasi akhir", "recommendation": "Ideal untuk laktasi akhir"},
        6: {"description": "Gemuk", "stage": "Kering kandang", "recommendation": "Kurangi konsentrat"},
        7: {"description": "Sangat Gemuk", "stage": "Tidak direkomendasikan", "recommendation": "Diet ketat"},
        8: {"description": "Obese", "stage": "Berbahaya", "recommendation": "Konsultasi dokter hewan"},
        9: {"description": "Extremely Obese", "stage": "Kritis", "recommendation": "Intervensi medis"}
    },
    "Kambing/Domba": {
        1: {"description": "Sangat Kurus", "recommendation": "Emergency feeding"},
        2: {"description": "Kurus", "recommendation": "Tingkatkan pakan"},
        3: {"description": "Sedang", "recommendation": "Ideal - pertahankan"},
        4: {"description": "Gemuk", "recommendation": "Kurangi konsentrat"},
        5: {"description": "Sangat Gemuk", "recommendation": "Diet ketat"}
    }
}

# ==========================================
# 🦠 DISEASE DATABASE
# ==========================================

DISEASE_DATABASE = {
    "Mastitis": {
        "category": "Penyakit Produksi",
        "species": ["Sapi Perah", "Kambing Perah"],
        "symptoms": [
            "Ambing bengkak dan panas",
            "Susu berubah warna (kekuningan/berdarah)",
            "Gumpalan pada susu",
            "Penurunan produksi susu mendadak",
            "Demam (>39.5°C)"
        ],
        "causes": [
            "Infeksi bakteri (Staphylococcus, Streptococcus, E.coli)",
            "Kebersihan kandang buruk",
            "Luka pada puting",
            "Teknik pemerahan salah"
        ],
        "treatment": [
            "Antibiotik intramammary (Penicillin, Cephalosporin)",
            "Anti-inflamasi (Flunixin meglumine)",
            "Perah lebih sering (4-6x/hari)",
            "Kompres hangat pada ambing",
            "Isolasi susu terinfeksi"
        ],
        "prevention": [
            "Teat dipping pre & post milking",
            "Dry cow therapy",
            "Sanitasi alat perah",
            "Pemeriksaan CMT rutin",
            "Culling sapi mastitis kronis"
        ],
        "severity": "Sedang-Tinggi",
        "economic_impact": "Tinggi - kerugian produksi 10-30%"
    },
    "FMD (Penyakit Mulut dan Kuku)": {
        "category": "Penyakit Viral",
        "species": ["Sapi", "Kambing", "Domba", "Babi"],
        "symptoms": [
            "Lepuh/blister di mulut, lidah, gusi",
            "Lepuh di kuku dan celah kuku",
            "Demam tinggi (40-41°C)",
            "Hipersalivasi (ngiler berlebihan)",
            "Pincang/kesulitan berjalan",
            "Penurunan nafsu makan drastis"
        ],
        "causes": [
            "Virus FMD (Aphthovirus) - 7 serotipe",
            "Penularan sangat cepat (udara, kontak, pakan)",
            "Hewan carrier tanpa gejala"
        ],
        "treatment": [
            "TIDAK ADA PENGOBATAN SPESIFIK",
            "Supportive care (vitamin, antibiotik sekunder)",
            "Isolasi ketat",
            "Desinfeksi kandang",
            "Pelaporan wajib ke Dinas"
        ],
        "prevention": [
            "Vaksinasi rutin (3-6 bulan sekali)",
            "Biosecurity ketat",
            "Karantina hewan baru",
            "Kontrol lalu lintas ternak"
        ],
        "severity": "Sangat Tinggi",
        "economic_impact": "Sangat Tinggi - mortalitas anak 50%, penurunan produksi 40%"
    },
    "Bloat (Kembung)": {
        "category": "Gangguan Pencernaan",
        "species": ["Sapi", "Kambing", "Domba"],
        "symptoms": [
            "Perut kiri membesar (rumen distensi)",
            "Kesulitan bernapas",
            "Gelisah, menendang perut",
            "Berhenti makan dan ruminasi",
            "Berdiri dengan kaki depan lebih tinggi"
        ],
        "causes": [
            "Konsumsi legume segar berlebihan (alfalfa, clover)",
            "Makan terlalu cepat",
            "Pakan biji-bijian halus berlebihan",
            "Gangguan motilitas rumen"
        ],
        "treatment": [
            "EMERGENCY - trocar jika parah",
            "Pemberian minyak nabati 250-500ml",
            "Antifoaming agent (poloxalene)",
            "Massage rumen",
            "Berdirikan dengan kaki depan lebih tinggi"
        ],
        "prevention": [
            "Introduksi legume bertahap",
            "Campur dengan rumput kering",
            "Hindari legume basah embun",
            "Pemberian anti-bloat sebelum penggembalaan"
        ],
        "severity": "Tinggi - dapat fatal dalam 1-2 jam",
        "economic_impact": "Tinggi - mortalitas 10-30% jika tidak ditangani"
    },
    "Scabies (Kudis/Gudig)": {
        "category": "Penyakit Kulit",
        "species": ["Sapi", "Kambing", "Domba"],
        "symptoms": [
            "Gatal hebat - menggaruk terus menerus",
            "Kerontokan bulu/rambut",
            "Kulit menebal dan berkerak",
            "Luka akibat garukan",
            "Penurunan kondisi tubuh"
        ],
        "causes": [
            "Tungau Sarcoptes scabiei",
            "Penularan kontak langsung",
            "Kandang lembab dan kotor"
        ],
        "treatment": [
            "Ivermectin injeksi (200 mcg/kg BB)",
            "Mandi dengan acaricide (Amitraz)",
            "Ulangi treatment 14 hari kemudian",
            "Desinfeksi kandang dan peralatan"
        ],
        "prevention": [
            "Karantina hewan baru",
            "Sanitasi kandang rutin",
            "Hindari kepadatan berlebihan",
            "Pemeriksaan kulit berkala"
        ],
        "severity": "Sedang",
        "economic_impact": "Sedang - penurunan produksi 15-25%"
    },
    "Pneumonia": {
        "category": "Penyakit Pernapasan",
        "species": ["Sapi", "Kambing", "Domba"],
        "symptoms": [
            "Batuk kering atau berdahak",
            "Napas cepat dan dangkal",
            "Demam (>39.5°C)",
            "Discharge hidung (mukus/nanah)",
            "Nafsu makan menurun",
            "Lesu dan lemah"
        ],
        "causes": [
            "Bakteri (Pasteurella, Mannheimia)",
            "Virus (BRSV, PI3, BVD)",
            "Stress (transport, cuaca ekstrem)",
            "Ventilasi kandang buruk"
        ],
        "treatment": [
            "Antibiotik broad spectrum (Oxytetracycline, Florfenicol)",
            "Anti-inflamasi (Flunixin)",
            "Vitamin A, D, E",
            "Perbaiki ventilasi",
            "Isolasi hewan sakit"
        ],
        "prevention": [
            "Vaksinasi (Pasteurella, BRSV)",
            "Ventilasi kandang baik",
            "Hindari stress",
            "Nutrisi optimal",
            "Karantina hewan baru"
        ],
        "severity": "Tinggi",
        "economic_impact": "Tinggi - mortalitas 10-40%, penurunan ADG 30%"
    }
}

# ==========================================
# 💉 VACCINATION SCHEDULES
# ==========================================

VACCINATION_SCHEDULES = {
    "Sapi Potong": [
        {
            "age_months": 2,
            "vaccine": "HS (Hemorrhagic Septicemia)",
            "dose": "2 ml SC/IM",
            "booster_months": 6,
            "frequency": "Setiap 6 bulan"
        },
        {
            "age_months": 3,
            "vaccine": "Anthrax (Antraks)",
            "dose": "1 ml SC",
            "booster_months": 12,
            "frequency": "Tahunan"
        },
        {
            "age_months": 3,
            "vaccine": "FMD (Penyakit Mulut dan Kuku)",
            "dose": "2 ml IM",
            "booster_months": 4,
            "frequency": "Setiap 4-6 bulan"
        },
        {
            "age_months": 4,
            "vaccine": "BEF (Bovine Ephemeral Fever)",
            "dose": "2 ml SC",
            "booster_months": 12,
            "frequency": "Tahunan"
        },
        {
            "age_months": 6,
            "vaccine": "Brucellosis (Betina saja - S19/RB51)",
            "dose": "2 ml SC",
            "booster_months": None,
            "frequency": "Sekali seumur hidup"
        }
    ],
    "Sapi Perah": [
        {
            "age_months": 2,
            "vaccine": "HS",
            "dose": "2 ml SC/IM",
            "booster_months": 6,
            "frequency": "Setiap 6 bulan"
        },
        {
            "age_months": 3,
            "vaccine": "FMD",
            "dose": "2 ml IM",
            "booster_months": 4,
            "frequency": "Setiap 4 bulan"
        },
        {
            "age_months": 6,
            "vaccine": "Brucellosis (S19/RB51)",
            "dose": "2 ml SC",
            "booster_months": None,
            "frequency": "Sekali"
        },
        {
            "age_months": "Pre-calving",
            "vaccine": "E. coli Mastitis Vaccine",
            "dose": "2 ml IM",
            "booster_months": "Setiap laktasi",
            "frequency": "60 & 30 hari sebelum calving"
        }
    ],
    "Kambing/Domba": [
        {
            "age_months": 2,
            "vaccine": "HS",
            "dose": "1 ml SC",
            "booster_months": 6,
            "frequency": "Setiap 6 bulan"
        },
        {
            "age_months": 3,
            "vaccine": "Anthrax",
            "dose": "0.5 ml SC",
            "booster_months": 12,
            "frequency": "Tahunan"
        },
        {
            "age_months": 3,
            "vaccine": "FMD",
            "dose": "1 ml IM",
            "booster_months": 6,
            "frequency": "Setiap 6 bulan"
        },
        {
            "age_months": 4,
            "vaccine": "Enterotoxemia (Clostridial)",
            "dose": "2 ml SC",
            "booster_months": 12,
            "frequency": "Tahunan"
        }
    ]
}

# ==========================================
# 🐛 DEWORMING PROTOCOLS
# ==========================================

DEWORMING_PROTOCOLS = {
    "Sapi": {
        "frequency": "Setiap 3-4 bulan",
        "products": [
            {"name": "Ivermectin", "dose": "200 mcg/kg BB", "route": "SC/PO"},
            {"name": "Albendazole", "dose": "10 mg/kg BB", "route": "PO"},
            {"name": "Levamisole", "dose": "7.5 mg/kg BB", "route": "SC/PO"}
        ],
        "critical_times": [
            "Sebelum musim hujan",
            "Sebelum breeding",
            "Pre-calving (60 hari sebelum)",
            "Post-calving (30 hari setelah)"
        ]
    },
    "Kambing/Domba": {
        "frequency": "Setiap 2-3 bulan",
        "products": [
            {"name": "Ivermectin", "dose": "200 mcg/kg BB", "route": "SC/PO"},
            {"name": "Albendazole", "dose": "5-10 mg/kg BB", "route": "PO"},
            {"name": "Closantel", "dose": "10 mg/kg BB", "route": "PO"}
        ],
        "critical_times": [
            "Sebelum breeding",
            "Pre-lambing (30 hari sebelum)",
            "Post-weaning",
            "Sebelum musim hujan"
        ]
    }
}

# ==========================================
# 🐄 REPRODUCTIVE PERFORMANCE CALCULATORS
# ==========================================

def calculate_calving_interval(calving_dates: List[str]) -> Dict:
    """
    Calculate calving interval from list of calving dates
    Target: 12-13 months for optimal production
    """
    if len(calving_dates) < 2:
        return {"error": "Minimal 2 data calving diperlukan"}
    
    dates = [datetime.strptime(d, "%Y-%m-%d") for d in sorted(calving_dates)]
    intervals = []
    
    for i in range(1, len(dates)):
        interval_days = (dates[i] - dates[i-1]).days
        intervals.append(interval_days)
    
    avg_interval = sum(intervals) / len(intervals)
    avg_months = avg_interval / 30.44
    
    status = "Optimal" if 365 <= avg_interval <= 395 else ("Terlalu Pendek" if avg_interval < 365 else "Terlalu Panjang")
    
    return {
        "average_interval_days": round(avg_interval, 1),
        "average_interval_months": round(avg_months, 1),
        "status": status,
        "intervals": intervals,
        "recommendation": get_calving_interval_recommendation(avg_interval)
    }

def get_calving_interval_recommendation(days: float) -> str:
    """Get recommendation based on calving interval"""
    if days < 365:
        return "Interval terlalu pendek - risiko involusi uterus tidak sempurna. Perpanjang voluntary waiting period."
    elif days <= 395:
        return "Interval optimal - pertahankan manajemen reproduksi saat ini."
    elif days <= 450:
        return "Interval agak panjang - evaluasi deteksi birahi dan timing inseminasi."
    else:
        return "Interval terlalu panjang - periksa fertilitas, nutrisi, dan kesehatan reproduksi. Konsultasi dokter hewan."

def calculate_conception_rate(services: int, pregnancies: int) -> Dict:
    """
    Calculate conception rate
    Target: >50% for first service, >70% overall
    """
    if services == 0:
        return {"error": "Jumlah service tidak boleh 0"}
    
    cr = (pregnancies / services) * 100
    
    status = "Baik" if cr >= 50 else ("Cukup" if cr >= 40 else "Buruk")
    
    return {
        "conception_rate": round(cr, 1),
        "status": status,
        "services": services,
        "pregnancies": pregnancies,
        "recommendation": get_cr_recommendation(cr)
    }

def get_cr_recommendation(cr: float) -> str:
    """Get recommendation based on conception rate"""
    if cr >= 60:
        return "Conception rate sangat baik - pertahankan manajemen saat ini."
    elif cr >= 50:
        return "Conception rate baik - monitor terus dan tingkatkan deteksi birahi."
    elif cr >= 40:
        return "Conception rate cukup - evaluasi kualitas semen, timing IB, dan body condition score."
    else:
        return "Conception rate buruk - segera evaluasi: nutrisi, kesehatan reproduksi, kualitas semen, dan teknik IB. Konsultasi dokter hewan."

def calculate_service_per_conception(total_services: int, total_pregnancies: int) -> Dict:
    """
    Calculate S/C (Services per Conception)
    Target: <1.8 (ideal <1.5)
    """
    if total_pregnancies == 0:
        return {"error": "Tidak ada kebuntingan tercatat"}
    
    sc = total_services / total_pregnancies
    
    status = "Baik" if sc <= 1.8 else ("Cukup" if sc <= 2.5 else "Buruk")
    
    return {
        "service_per_conception": round(sc, 2),
        "status": status,
        "total_services": total_services,
        "total_pregnancies": total_pregnancies,
        "recommendation": get_sc_recommendation(sc)
    }

def get_sc_recommendation(sc: float) -> str:
    """Get recommendation based on S/C"""
    if sc <= 1.5:
        return "S/C sangat baik - efisiensi reproduksi optimal."
    elif sc <= 1.8:
        return "S/C baik - pertahankan manajemen reproduksi."
    elif sc <= 2.5:
        return "S/C cukup - tingkatkan deteksi birahi dan evaluasi timing IB."
    else:
        return "S/C buruk - segera evaluasi: fertilitas pejantan/semen, kesehatan reproduksi betina, nutrisi, dan manajemen IB."

# ==========================================
# 🥛 MILK RECORDING & QUALITY
# ==========================================

def analyze_milk_production(daily_records: List[Dict]) -> Dict:
    """
    Analyze milk production data
    daily_records format: [{"date": "2024-01-01", "morning": 10, "evening": 8}, ...]
    """
    if not daily_records:
        return {"error": "Tidak ada data produksi"}
    
    df = pd.DataFrame(daily_records)
    df['total'] = df['morning'] + df['evening']
    
    avg_daily = df['total'].mean()
    peak_production = df['total'].max()
    current_production = df['total'].iloc[-1]
    
    # Estimate lactation stage based on trend
    if len(df) >= 7:
        recent_avg = df['total'].tail(7).mean()
        prev_avg = df['total'].head(7).mean()
        trend = "Naik" if recent_avg > prev_avg else ("Turun" if recent_avg < prev_avg else "Stabil")
    else:
        trend = "Insufficient data"
    
    return {
        "average_daily_production": round(avg_daily, 2),
        "peak_production": round(peak_production, 2),
        "current_production": round(current_production, 2),
        "trend": trend,
        "total_days": len(df),
        "total_production": round(df['total'].sum(), 2)
    }

def calculate_scc_status(scc_value: int) -> Dict:
    """
    Evaluate Somatic Cell Count (SCC)
    Normal: <200,000 cells/ml
    Subclinical mastitis: 200,000-500,000
    Clinical mastitis: >500,000
    """
    if scc_value < 200000:
        status = "Normal"
        risk = "Rendah"
        action = "Pertahankan manajemen kebersihan saat ini"
    elif scc_value < 500000:
        status = "Subclinical Mastitis"
        risk = "Sedang"
        action = "Tingkatkan kebersihan, periksa CMT, pertimbangkan kultur bakteri"
    else:
        status = "Clinical Mastitis"
        risk = "Tinggi"
        action = "Segera treatment - antibiotik intramammary, isolasi susu, konsultasi dokter hewan"
    
    return {
        "scc_value": scc_value,
        "status": status,
        "risk_level": risk,
        "action": action,
        "quality_impact": "Kualitas susu menurun" if scc_value >= 200000 else "Kualitas baik"
    }

# ==========================================
# 🩺 DISEASE EXPERT SYSTEM
# ==========================================

def diagnose_by_symptoms(selected_symptoms: List[str], species: str = "Sapi") -> List[Dict]:
    """
    Simple expert system to suggest possible diseases based on symptoms
    Returns list of possible diseases ranked by symptom match
    """
    results = []
    
    for disease_name, disease_data in DISEASE_DATABASE.items():
        # Check if species matches
        if species not in disease_data.get("species", []):
            continue
        
        # Calculate symptom match
        disease_symptoms = disease_data["symptoms"]
        matches = sum(1 for symptom in selected_symptoms if any(s.lower() in symptom.lower() or symptom.lower() in s.lower() for s in disease_symptoms))
        
        if matches > 0:
            match_percentage = (matches / len(selected_symptoms)) * 100
            results.append({
                "disease": disease_name,
                "match_percentage": round(match_percentage, 1),
                "matched_symptoms": matches,
                "total_symptoms": len(selected_symptoms),
                "severity": disease_data["severity"],
                "category": disease_data["category"],
                "data": disease_data
            })
    
    # Sort by match percentage
    results.sort(key=lambda x: x["match_percentage"], reverse=True)
    
    return results

# ==========================================
# 📊 BCS CALCULATOR
# ==========================================

def get_bcs_recommendation(species: str, bcs_score: float, production_stage: str = "General") -> Dict:
    """
    Get detailed BCS recommendation
    """
    if species not in BCS_STANDARDS:
        return {"error": f"Species {species} tidak tersedia"}
    
    bcs_int = int(round(bcs_score))
    
    if species == "Sapi Perah" and bcs_int > 9:
        bcs_int = 9
    elif species in ["Sapi Potong", "Kambing/Domba"] and bcs_int > 5:
        bcs_int = 5
    
    bcs_data = BCS_STANDARDS[species].get(bcs_int, {})
    
    return {
        "species": species,
        "bcs_score": bcs_score,
        "bcs_category": bcs_int,
        "description": bcs_data.get("description", ""),
        "visual_guide": bcs_data.get("visual", ""),
        "recommendation": bcs_data.get("recommendation", ""),
        "risk_level": bcs_data.get("risk", ""),
        "production_stage": production_stage
    }
