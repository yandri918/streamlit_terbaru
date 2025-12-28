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

# Horticulture Export Specific Data
HORTICULTURE_EXPORT = {
    "Mangga Harum Manis": {
        "export_grade": "Grade A (>250g/buah)",
        "price_domestic": 15000,  # Rp/kg
        "price_export": 45000,  # Rp/kg
        "premium": "200%",
        "main_markets": ["Japan", "Korea", "Middle East"],
        "certifications_required": ["GAP", "Phytosanitary"],
        "shelf_life": "14-21 days (cold storage)",
        "packaging": "Carton 5kg, individual wrapping",
        "cold_chain": "10-13°C",
        "rejection_rate": "5-10%",
        "export_costs": {
            "sorting_grading": 2000,  # Rp/kg
            "packaging": 3000,
            "cold_storage": 1500,
            "phytosanitary": 500,
            "shipping": 8000,
            "insurance": 500,
            "documentation": 300
        }
    },
    
    "Pisang Cavendish": {
        "export_grade": "Grade A (18-22cm)",
        "price_domestic": 12000,
        "price_export": 28000,
        "premium": "133%",
        "main_markets": ["China", "Japan", "Middle East"],
        "certifications_required": ["GlobalGAP", "Phytosanitary"],
        "shelf_life": "30-40 days (controlled atmosphere)",
        "packaging": "Carton 13kg",
        "cold_chain": "13-14°C",
        "rejection_rate": "8-12%",
        "export_costs": {
            "sorting_grading": 1500,
            "packaging": 2500,
            "cold_storage": 2000,
            "phytosanitary": 500,
            "shipping": 6000,
            "insurance": 400,
            "documentation": 300
        }
    },
    
    "Cabai Merah Keriting": {
        "export_grade": "Grade A (>12cm, merah sempurna)",
        "price_domestic": 25000,
        "price_export": 65000,
        "premium": "160%",
        "main_markets": ["Singapore", "Malaysia", "Thailand"],
        "certifications_required": ["GAP", "Pesticide residue test"],
        "shelf_life": "7-10 days (cold storage)",
        "packaging": "Plastic crate 5kg",
        "cold_chain": "7-10°C",
        "rejection_rate": "10-15%",
        "export_costs": {
            "sorting_grading": 3000,
            "packaging": 2000,
            "cold_storage": 2500,
            "phytosanitary": 600,
            "shipping": 5000,
            "insurance": 600,
            "documentation": 300
        }
    },
    
    "Tomat Cherry": {
        "export_grade": "Grade A (uniform size, no blemish)",
        "price_domestic": 30000,
        "price_export": 80000,
        "premium": "167%",
        "main_markets": ["Singapore", "Hong Kong", "Japan"],
        "certifications_required": ["GlobalGAP", "Organic (premium)"],
        "shelf_life": "10-14 days (cold storage)",
        "packaging": "Plastic punnet 250g",
        "cold_chain": "10-12°C",
        "rejection_rate": "12-18%",
        "export_costs": {
            "sorting_grading": 4000,
            "packaging": 5000,
            "cold_storage": 3000,
            "phytosanitary": 700,
            "shipping": 7000,
            "insurance": 800,
            "documentation": 300
        }
    },
    
    # ===== REMPAH-REMPAH (SPICES) =====
    "Jahe Merah": {
        "export_grade": "Grade A (fresh, >150g/rhizome)",
        "price_domestic": 35000,  # Rp/kg
        "price_export": 95000,  # Rp/kg
        "premium": "171%",
        "main_markets": ["China", "USA", "Europe", "Middle East"],
        "certifications_required": ["GAP", "Organic (premium)", "Pesticide residue test"],
        "shelf_life": "30-45 days (cold storage)",
        "packaging": "Carton 10kg, ventilated",
        "cold_chain": "13-15°C, 90% humidity",
        "rejection_rate": "8-12%",
        "export_costs": {
            "sorting_grading": 3500,  # Rp/kg
            "packaging": 2500,
            "cold_storage": 2000,
            "phytosanitary": 600,
            "shipping": 7000,
            "insurance": 700,
            "documentation": 300
        }
    },
    
    "Kunyit (Turmeric)": {
        "export_grade": "Grade A (bright yellow, >8% curcumin)",
        "price_domestic": 25000,
        "price_export": 75000,
        "premium": "200%",
        "main_markets": ["India", "USA", "Europe", "Japan"],
        "certifications_required": ["GAP", "Organic", "Curcumin content test"],
        "shelf_life": "60-90 days (dried)",
        "packaging": "Jute bags 25kg or carton 10kg",
        "cold_chain": "Ambient (dry, <25°C)",
        "rejection_rate": "10-15%",
        "export_costs": {
            "sorting_grading": 3000,
            "packaging": 2000,
            "cold_storage": 1000,
            "phytosanitary": 500,
            "shipping": 6000,
            "insurance": 600,
            "documentation": 300
        }
    },
    
    "Lada Hitam (Black Pepper)": {
        "export_grade": "Grade A (>500g/L bulk density, 3% piperine)",
        "price_domestic": 80000,
        "price_export": 180000,
        "premium": "125%",
        "main_markets": ["USA", "Europe", "Middle East", "Singapore"],
        "certifications_required": ["GAP", "HACCP", "Pesticide residue test"],
        "shelf_life": "12-24 months (dried)",
        "packaging": "Jute bags 50kg or vacuum pack",
        "cold_chain": "Ambient (dry, <20°C)",
        "rejection_rate": "5-8%",
        "export_costs": {
            "sorting_grading": 4000,
            "packaging": 3000,
            "cold_storage": 800,
            "phytosanitary": 500,
            "shipping": 8000,
            "insurance": 1000,
            "documentation": 300
        }
    },
    
    "Vanili (Vanilla Pods)": {
        "export_grade": "Grade A (>16cm, 25-30% moisture, gourmet)",
        "price_domestic": 800000,
        "price_export": 2500000,
        "premium": "213%",
        "main_markets": ["France", "USA", "Germany", "Japan"],
        "certifications_required": ["Organic", "Fair Trade", "Origin certification"],
        "shelf_life": "24-36 months (vacuum sealed)",
        "packaging": "Vacuum sealed, individual wrapping",
        "cold_chain": "15-20°C, 60-70% humidity",
        "rejection_rate": "12-18%",
        "export_costs": {
            "sorting_grading": 50000,  # High labor cost
            "packaging": 30000,  # Premium packaging
            "cold_storage": 10000,
            "phytosanitary": 1000,
            "shipping": 15000,
            "insurance": 5000,  # High value
            "documentation": 500
        }
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
    def calculate_horticulture_export(product_name, volume_kg):
        """
        Calculate export profitability for horticulture products
        
        Args:
            product_name: Name of horticulture product
            volume_kg: Export volume in kg
            
        Returns:
            dict with detailed cost breakdown and profit analysis
        """
        product_data = HORTICULTURE_EXPORT.get(product_name, HORTICULTURE_EXPORT["Mangga Harum Manis"])
        
        # Calculate costs
        costs = product_data["export_costs"]
        
        cost_sorting = volume_kg * costs["sorting_grading"]
        cost_packaging = volume_kg * costs["packaging"]
        cost_cold_storage = volume_kg * costs["cold_storage"]
        cost_phytosanitary = volume_kg * costs["phytosanitary"]
        cost_shipping = volume_kg * costs["shipping"]
        cost_insurance = volume_kg * costs["insurance"]
        cost_documentation = volume_kg * costs["documentation"]
        
        # Product cost (farm gate price)
        cost_product = volume_kg * product_data["price_domestic"]
        
        # Rejection/wastage
        rejection_rate = float(product_data["rejection_rate"].split("-")[0]) / 100
        saleable_volume = volume_kg * (1 - rejection_rate)
        
        # Total costs
        total_export_costs = (cost_sorting + cost_packaging + cost_cold_storage + 
                             cost_phytosanitary + cost_shipping + cost_insurance + 
                             cost_documentation)
        total_cost = cost_product + total_export_costs
        
        # Revenue
        revenue = saleable_volume * product_data["price_export"]
        
        # Profit
        profit = revenue - total_cost
        profit_margin = (profit / revenue * 100) if revenue > 0 else 0
        
        return {
            "product_name": product_name,
            "volume_kg": volume_kg,
            "saleable_volume": saleable_volume,
            "rejection_rate": product_data["rejection_rate"],
            "export_grade": product_data["export_grade"],
            "price_domestic": product_data["price_domestic"],
            "price_export": product_data["price_export"],
            "premium": product_data["premium"],
            "main_markets": product_data["main_markets"],
            "certifications_required": product_data["certifications_required"],
            "cold_chain": product_data["cold_chain"],
            "shelf_life": product_data["shelf_life"],
            "cost_breakdown": {
                "product_cost": cost_product,
                "sorting_grading": cost_sorting,
                "packaging": cost_packaging,
                "cold_storage": cost_cold_storage,
                "phytosanitary": cost_phytosanitary,
                "shipping": cost_shipping,
                "insurance": cost_insurance,
                "documentation": cost_documentation,
                "total_export_costs": total_export_costs,
                "total_cost": total_cost
            },
            "revenue": revenue,
            "profit": profit,
            "profit_margin": round(profit_margin, 1),
            "roi": round((profit / total_cost * 100), 1) if total_cost > 0 else 0
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
