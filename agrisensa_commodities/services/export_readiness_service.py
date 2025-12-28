# Export Readiness & Certification Service

CERTIFICATIONS = {
    "GAP (Good Agricultural Practices)": {
        "cost": "Rp 20-40 juta/tahun",
        "validity": "3 years",
        "applicable_to": ["Hortikultura", "Buah", "Sayuran", "Tanaman Pangan"],
        "requirements": [
            "Sistem traceability (penelusuran produk)",
            "Manajemen pestisida terstandar",
            "Pengujian kualitas air",
            "Keselamatan pekerja",
            "Pencatatan aktivitas budidaya"
        ],
        "benefits": "Akses pasar EU, USA, Japan, premium price 15-25%",
        "certification_body": "ASEAN GAP, Indonesia GAP (Kementan)",
        "process_time": "3-6 bulan",
        "renewal": "Annual audit required"
    },
    
    "Organic (USDA/EU/SNI)": {
        "cost": "Rp 50-100 juta/tahun",
        "validity": "1 year",
        "applicable_to": ["Semua komoditas pertanian"],
        "requirements": [
            "Masa transisi 3 tahun (tanpa pestisida sintetik)",
            "Hanya pupuk organik",
            "Buffer zone 8-10 meter dari lahan konvensional",
            "Dokumentasi lengkap",
            "Audit tahunan"
        ],
        "benefits": "Premium price 30-50%, akses pasar premium global",
        "certification_body": "IFOAM, Control Union, Ecocert, Inofice",
        "process_time": "3-4 tahun (termasuk transisi)",
        "renewal": "Annual certification"
    },
    
    "GlobalGAP": {
        "cost": "Rp 30-60 juta/tahun",
        "validity": "1 year",
        "applicable_to": ["Hortikultura", "Livestock", "Aquaculture"],
        "requirements": [
            "Risk assessment komprehensif",
            "Prinsip HACCP",
            "Manajemen lingkungan",
            "Social compliance (pekerja)",
            "Traceability system"
        ],
        "benefits": "Akses ke retailer Eropa (Carrefour, Tesco, Aldi)",
        "certification_body": "GlobalGAP approved certification bodies",
        "process_time": "6-12 bulan",
        "renewal": "Annual audit"
    },
    
    "HACCP (Hazard Analysis Critical Control Point)": {
        "cost": "Rp 40-80 juta/tahun",
        "validity": "3 years",
        "applicable_to": ["Produk olahan", "Livestock", "Seafood"],
        "requirements": [
            "Analisis bahaya (biological, chemical, physical)",
            "Identifikasi critical control points",
            "Prosedur monitoring",
            "Corrective actions",
            "Verifikasi & dokumentasi"
        ],
        "benefits": "Mandatory untuk export, akses major retailers",
        "certification_body": "SGS, TUV, Bureau Veritas, Sucofindo",
        "process_time": "4-6 bulan",
        "renewal": "Audit every 3 years"
    },
    
    "Halal": {
        "cost": "Rp 10-30 juta/tahun",
        "validity": "2 years",
        "applicable_to": ["Semua produk makanan & minuman"],
        "requirements": [
            "Tidak ada bahan haram",
            "Lini produksi terpisah",
            "Auditor Muslim",
            "Sertifikat bahan baku halal"
        ],
        "benefits": "Akses pasar Middle East & Muslim (1.8B konsumen)",
        "certification_body": "MUI, JAKIM, Halal International",
        "process_time": "2-3 bulan",
        "renewal": "Biennial"
    },
    
    "Fair Trade": {
        "cost": "Rp 30-60 juta/tahun",
        "validity": "3 years",
        "applicable_to": ["Kopi", "Kakao", "Teh", "Gula", "Buah"],
        "requirements": [
            "Fair wages untuk pekerja",
            "No child labor",
            "Community development fund",
            "Environmental sustainability",
            "Democratic organization"
        ],
        "benefits": "Premium price 20-30%, kontrak jangka panjang",
        "certification_body": "Fairtrade International, Fair Trade USA",
        "process_time": "6-12 bulan",
        "renewal": "Audit every 3 years"
    }
}

# Export Documentation Requirements
EXPORT_DOCUMENTS = {
    "Pre-Export Registration": {
        "NPWP": "Nomor Pokok Wajib Pajak",
        "NIB": "Nomor Induk Berusaha (via OSS)",
        "API": "Angka Pengenal Importir",
        "Customs_Registration": "Registrasi di Bea Cukai",
        "Product_Certification": "Sesuai jenis produk"
    },
    
    "Shipping Documents": {
        "Commercial_Invoice": "Faktur komersial (nilai barang)",
        "Packing_List": "Daftar isi kemasan",
        "Bill_of_Lading": "B/L - bukti pengiriman",
        "Certificate_of_Origin": "SKA - surat keterangan asal",
        "Phytosanitary_Certificate": "Untuk produk pertanian",
        "Health_Certificate": "Untuk produk makanan/ternak",
        "Insurance_Certificate": "Asuransi pengiriman"
    },
    
    "Payment Documents": {
        "Letter_of_Credit": "L/C - jaminan pembayaran",
        "Payment_Terms": "Kesepakatan pembayaran",
        "Bank_Documents": "SWIFT, remittance advice"
    }
}

# Phytosanitary Certificate Process
PHYTOSANITARY_PROCESS = {
    "definition": "Sertifikat kesehatan tanaman yang menyatakan produk bebas hama & penyakit",
    "validity": "14 hari sejak penerbitan",
    "issuing_authority": "Balai Karantina Pertanian",
    "requirements": [
        "Produk bebas hama karantina",
        "Fumigasi (jika diperlukan)",
        "Inspeksi lapangan",
        "Uji laboratorium",
        "Dokumen pendukung (invoice, packing list)"
    ],
    "process_steps": [
        "1. Daftar online di IQFAST (karantina.pertanian.go.id)",
        "2. Upload dokumen (invoice, packing list, sertifikat)",
        "3. Jadwalkan inspeksi lapangan",
        "4. Petugas karantina inspeksi produk",
        "5. Sampling & uji lab (jika perlu)",
        "6. Penerbitan sertifikat (1-3 hari)",
        "7. Ambil sertifikat atau kirim digital"
    ],
    "cost": "Rp 500,000 - 2,000,000 (tergantung volume)",
    "processing_time": "3-7 hari kerja"
}

# Packaging & Labeling Standards
PACKAGING_STANDARDS = {
    "International_Requirements": {
        "Product_Name": "Nama produk (English)",
        "Net_Weight": "Berat bersih (kg/g)",
        "Country_of_Origin": "Made in Indonesia",
        "Ingredients": "Daftar bahan (descending order)",
        "Nutrition_Facts": "Kalori, protein, lemak, karbohidrat",
        "Allergen_Info": "Contains: nuts, dairy, etc.",
        "Barcode": "EAN-13 (EU), UPC (USA)",
        "Batch_Number": "Production batch",
        "Expiry_Date": "Best before / Use by",
        "Storage_Instructions": "Store in cool dry place"
    },
    
    "Material_Standards": {
        "Food_Grade": "FDA approved, BPA-free",
        "Temperature_Indicators": "Untuk cold chain",
        "Moisture_Barriers": "Untuk produk kering",
        "Tamper_Evident": "Seal yang jelas jika dibuka",
        "Recyclable": "Eco-friendly packaging preferred"
    },
    
    "Label_Design": {
        "Font_Size": "Minimum 2mm untuk ingredients",
        "Language": "English + local language",
        "Color_Coding": "Green = organic, Red = allergen",
        "QR_Code": "Traceability & product info"
    }
}

# Major International Buyers
BUYERS_DIRECTORY = {
    "USA": [
        {"name": "Whole Foods Market", "products": ["Organic VCO", "Coconut Sugar", "Organic Produce"], "contact": "supplier@wholefoods.com"},
        {"name": "Trader Joe's", "products": ["Organic products", "Specialty foods"], "contact": "vendor@traderjoes.com"},
        {"name": "Costco Wholesale", "products": ["Bulk commodities", "Organic"], "contact": "supplier@costco.com"},
        {"name": "Walmart", "products": ["Fresh produce", "Packaged foods"], "contact": "supplier@walmart.com"},
        {"name": "Amazon Fresh", "products": ["Organic", "Specialty items"], "contact": "vendor@amazon.com"}
    ],
    
    "European Union": [
        {"name": "Alnatura (Germany)", "products": ["Organic products"], "contact": "lieferanten@alnatura.de"},
        {"name": "Bio Company (Germany)", "products": ["Organic foods"], "contact": "einkauf@biocompany.de"},
        {"name": "Carrefour Bio (France)", "products": ["Organic produce"], "contact": "fournisseurs@carrefour.com"},
        {"name": "Tesco (UK)", "products": ["Fresh produce", "Packaged goods"], "contact": "supplier@tesco.com"},
        {"name": "Albert Heijn (Netherlands)", "products": ["Organic", "Fair Trade"], "contact": "inkoop@ah.nl"}
    ],
    
    "Middle East": [
        {"name": "Lulu Hypermarket", "products": ["Halal products", "Fresh produce"], "contact": "supplier@luluhypermarket.com"},
        {"name": "Carrefour ME", "products": ["Halal certified", "Organic"], "contact": "suppliers.me@carrefour.com"},
        {"name": "Spinneys", "products": ["Premium foods", "Organic"], "contact": "procurement@spinneys.com"},
        {"name": "Al Maya Group", "products": ["Halal products"], "contact": "supplier@almaya.com"}
    ],
    
    "Asia": [
        {"name": "Aeon (Japan)", "products": ["Organic", "Fresh produce"], "contact": "supplier@aeon.jp"},
        {"name": "Muji (Japan)", "products": ["Natural products", "Organic"], "contact": "vendor@muji.com"},
        {"name": "FairPrice (Singapore)", "products": ["Fresh produce", "Packaged foods"], "contact": "supplier@fairprice.com.sg"},
        {"name": "Lotte Mart (Korea)", "products": ["Fresh produce", "Organic"], "contact": "vendor@lottemart.com"}
    ]
}

# Cold Chain & Logistics
COLD_CHAIN_GUIDE = {
    "Temperature_Requirements": {
        "Fresh_Produce": "2-8°C",
        "Frozen_Products": "-18°C to -25°C",
        "Chilled_Products": "0-4°C",
        "Ambient": "15-25°C (controlled)"
    },
    
    "Cold_Chain_Components": [
        "Pre-cooling facilities (setelah panen)",
        "Cold storage warehouse",
        "Refrigerated trucks (reefer trucks)",
        "Reefer containers (20ft/40ft)",
        "Temperature monitoring devices",
        "Backup power generators",
        "Insulated packaging"
    ],
    
    "Logistics_Partners": {
        "Freight_Forwarders": ["DHL", "FedEx", "Agility", "Kuehne+Nagel"],
        "Shipping_Lines": ["Maersk", "MSC", "CMA CGM", "Evergreen"],
        "Cold_Storage": ["Agro Cold Storage", "Kaltim Cold Storage"],
        "Customs_Brokers": ["Schenker", "DB Schenker", "Expeditors"]
    },
    
    "Shipping_Routes": {
        "USA": "Jakarta → Singapore → Los Angeles (25-30 days)",
        "EU": "Jakarta → Rotterdam (30-35 days)",
        "Middle_East": "Jakarta → Jebel Ali (15-20 days)",
        "Asia": "Jakarta → Tokyo/Singapore (7-14 days)"
    }
}

class ExportReadinessService:
    """Service for export readiness assessment and guidance"""
    
    @staticmethod
    def calculate_certification_cost(certifications_selected):
        """Calculate total certification cost"""
        total_cost = 0
        details = []
        
        for cert_name in certifications_selected:
            cert_data = CERTIFICATIONS.get(cert_name, {})
            cost_str = cert_data.get("cost", "Rp 0")
            
            # Parse cost range (e.g., "Rp 20-40 juta")
            cost_parts = cost_str.replace("Rp ", "").replace(" juta/tahun", "").split("-")
            avg_cost = (int(cost_parts[0]) + int(cost_parts[1])) / 2 * 1000000 if len(cost_parts) == 2 else 0
            
            total_cost += avg_cost
            details.append({
                "certification": cert_name,
                "cost": avg_cost,
                "validity": cert_data.get("validity", "N/A")
            })
        
        return {
            "total_cost": total_cost,
            "details": details,
            "annual_cost": total_cost  # Most certs are annual
        }
    
    @staticmethod
    def assess_readiness(commodity, has_gap, has_organic, has_haccp, has_documentation):
        """Assess export readiness score"""
        score = 0
        recommendations = []
        
        # Certification score (40%)
        if has_gap:
            score += 15
        else:
            recommendations.append("✅ Dapatkan sertifikasi GAP untuk akses pasar internasional")
        
        if has_organic:
            score += 15
        else:
            recommendations.append("✅ Sertifikasi Organic untuk premium price 30-50%")
        
        if has_haccp:
            score += 10
        else:
            recommendations.append("✅ HACCP diperlukan untuk produk olahan")
        
        # Documentation score (30%)
        if has_documentation:
            score += 30
        else:
            recommendations.append("✅ Lengkapi dokumen ekspor (NIB, API, SKA)")
        
        # Commodity-specific (30%)
        if commodity in ["Hortikultura", "Buah", "Sayuran"]:
            score += 30
            recommendations.append("✅ Komoditas Anda memiliki demand tinggi di pasar export")
        else:
            score += 15
            recommendations.append("✅ Pertimbangkan value-added processing untuk premium price")
        
        # Readiness level
        if score >= 80:
            level = "READY"
            message = "🎉 Anda siap untuk ekspor!"
        elif score >= 60:
            level = "ALMOST READY"
            message = "⚠️ Beberapa perbaikan diperlukan"
        else:
            level = "NOT READY"
            message = "❌ Perlu persiapan lebih lanjut"
        
        return {
            "score": score,
            "level": level,
            "message": message,
            "recommendations": recommendations
        }
