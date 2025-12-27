"""
Service module for Medicinal Plants & Herbal cultivation
Provides cultivation guides, market data, and business calculations
"""

# ===== CULTIVATION DATABASE =====
CULTIVATION_DATABASE = {
    "Jahe Merah": {
        "latin_name": "Zingiber officinale var. rubrum",
        "category": "Rhizome",
        "cycle_months": 10,
        "planting_density": "40,000 rimpang/ha",
        "spacing": "25 cm x 40 cm",
        "altitude": "200-900 mdpl",
        "rainfall": "2500-4000 mm/tahun",
        "soil_ph": "6.0-7.5",
        "soil_type": "Lempung berpasir, gembur, drainase baik",
        "yield_fresh": "20-25 ton/ha",
        "yield_dry": "4-5 ton/ha",
        "drying_ratio": 0.20,
        "fertilizer": {
            "organic": "20 ton/ha pupuk kandang",
            "urea": "200 kg/ha (3x aplikasi)",
            "sp36": "150 kg/ha",
            "kcl": "200 kg/ha (3x aplikasi)"
        },
        "pests": ["Ulat penggerek rimpang", "Kutu daun", "Lalat rimpang"],
        "diseases": ["Layu bakteri", "Bercak daun", "Busuk rimpang"],
        "harvest_indicator": "Daun menguning 80%, umur 10-12 bulan",
        "active_compounds": ["Gingerol", "Shogaol", "Zingeron"],
        "health_benefits": [
            "Anti-inflamasi kuat",
            "Meningkatkan imunitas",
            "Melancarkan sirkulasi darah",
            "Antioksidan tinggi"
        ]
    },
    "Kunyit": {
        "latin_name": "Curcuma longa",
        "category": "Rhizome",
        "cycle_months": 8,
        "planting_density": "50,000 rimpang/ha",
        "spacing": "20 cm x 40 cm",
        "altitude": "0-1200 mdpl",
        "rainfall": "2000-4000 mm/tahun",
        "soil_ph": "5.5-7.0",
        "soil_type": "Lempung berpasir, subur, drainase sempurna",
        "yield_fresh": "25-30 ton/ha",
        "yield_dry": "5-6 ton/ha",
        "drying_ratio": 0.20,
        "fertilizer": {
            "organic": "15 ton/ha pupuk kandang",
            "urea": "150 kg/ha",
            "sp36": "100 kg/ha",
            "kcl": "150 kg/ha"
        },
        "pests": ["Ulat penggerek", "Kutu perisai"],
        "diseases": ["Bercak daun", "Layu bakteri"],
        "harvest_indicator": "Daun kering, umur 8-10 bulan",
        "active_compounds": ["Curcumin", "Demethoxycurcumin", "Bisdemethoxycurcumin"],
        "health_benefits": [
            "Anti-inflamasi (curcumin 3-5%)",
            "Hepatoprotektor (pelindung hati)",
            "Antioksidan kuat",
            "Anti-kanker (penelitian in-vitro)"
        ]
    },
    "Temulawak": {
        "latin_name": "Curcuma xanthorrhiza",
        "category": "Rhizome",
        "cycle_months": 9,
        "planting_density": "40,000 rimpang/ha",
        "spacing": "25 cm x 40 cm",
        "altitude": "0-1500 mdpl",
        "rainfall": "2500-4000 mm/tahun",
        "soil_ph": "6.0-7.5",
        "soil_type": "Lempung berpasir, gembur",
        "yield_fresh": "20-25 ton/ha",
        "yield_dry": "4-5 ton/ha",
        "drying_ratio": 0.20,
        "fertilizer": {
            "organic": "20 ton/ha pupuk kandang",
            "urea": "180 kg/ha",
            "sp36": "120 kg/ha",
            "kcl": "180 kg/ha"
        },
        "pests": ["Ulat penggerek", "Belalang"],
        "diseases": ["Bercak daun", "Busuk rimpang"],
        "harvest_indicator": "Daun menguning, umur 9-12 bulan",
        "active_compounds": ["Xanthorrhizol", "Curcumin", "Essential oils"],
        "health_benefits": [
            "Hepatoprotektor (paten Jerman)",
            "Meningkatkan nafsu makan",
            "Anti-kolesterol",
            "Antioksidan"
        ]
    },
    "Kencur": {
        "latin_name": "Kaempferia galanga",
        "category": "Rhizome",
        "cycle_months": 4,
        "planting_density": "100,000 rimpang/ha",
        "spacing": "15 cm x 20 cm",
        "altitude": "0-600 mdpl",
        "rainfall": "2500-4000 mm/tahun",
        "soil_ph": "6.0-7.0",
        "soil_type": "Lempung berpasir, gembur, naungan 30%",
        "yield_fresh": "15-20 ton/ha",
        "yield_dry": "3-4 ton/ha",
        "drying_ratio": 0.20,
        "fertilizer": {
            "organic": "15 ton/ha pupuk kandang",
            "urea": "100 kg/ha",
            "sp36": "75 kg/ha",
            "kcl": "100 kg/ha"
        },
        "pests": ["Ulat tanah", "Belalang"],
        "diseases": ["Busuk rimpang", "Layu"],
        "harvest_indicator": "Daun kering, umur 4-5 bulan",
        "active_compounds": ["Ethyl p-methoxycinnamate", "Essential oils"],
        "health_benefits": [
            "Ekspektoran (pelega batuk)",
            "Anti-inflamasi",
            "Aromaterapi",
            "Meningkatkan stamina"
        ]
    },
    "Sambiloto": {
        "latin_name": "Andrographis paniculata",
        "category": "Leaf/Herb",
        "cycle_months": 3,
        "planting_density": "200,000 tanaman/ha",
        "spacing": "20 cm x 25 cm",
        "altitude": "0-700 mdpl",
        "rainfall": "2000-3000 mm/tahun",
        "soil_ph": "5.5-7.0",
        "soil_type": "Lempung berpasir, drainase baik",
        "yield_fresh": "10-15 ton/ha",
        "yield_dry": "2-3 ton/ha",
        "drying_ratio": 0.20,
        "fertilizer": {
            "organic": "10 ton/ha pupuk kandang",
            "urea": "100 kg/ha",
            "sp36": "50 kg/ha",
            "kcl": "75 kg/ha"
        },
        "pests": ["Ulat daun", "Kutu daun"],
        "diseases": ["Bercak daun", "Layu fusarium"],
        "harvest_indicator": "Sebelum berbunga, umur 3-4 bulan",
        "active_compounds": ["Andrographolide", "Deoxyandrographolide"],
        "health_benefits": [
            "Imunomodulator (meningkatkan imun)",
            "Hepatoprotektor",
            "Anti-diabetes (penelitian klinis)",
            "Anti-virus (influenza, herpes)"
        ]
    },
    "Pegagan": {
        "latin_name": "Centella asiatica",
        "category": "Leaf/Herb",
        "cycle_months": 2,
        "planting_density": "300,000 tanaman/ha",
        "spacing": "15 cm x 20 cm",
        "altitude": "0-2500 mdpl",
        "rainfall": "2000-3000 mm/tahun",
        "soil_ph": "6.0-7.0",
        "soil_type": "Lempung, lembab, naungan 50%",
        "yield_fresh": "20-30 ton/ha/tahun (panen 6x)",
        "yield_dry": "4-6 ton/ha/tahun",
        "drying_ratio": 0.20,
        "fertilizer": {
            "organic": "15 ton/ha pupuk kandang",
            "urea": "150 kg/ha/tahun",
            "sp36": "75 kg/ha/tahun",
            "kcl": "100 kg/ha/tahun"
        },
        "pests": ["Siput", "Ulat daun"],
        "diseases": ["Bercak daun"],
        "harvest_indicator": "Panen setiap 2 bulan (cutting)",
        "active_compounds": ["Asiaticoside", "Madecassoside", "Asiatic acid"],
        "health_benefits": [
            "Meningkatkan fungsi kognitif",
            "Penyembuhan luka (topikal)",
            "Anti-anxiety (penelitian klinis)",
            "Meningkatkan sirkulasi darah"
        ]
    },
    "Ginseng Jawa": {
        "latin_name": "Talinum paniculatum",
        "category": "Root",
        "cycle_months": 6,
        "planting_density": "100,000 tanaman/ha",
        "spacing": "20 cm x 30 cm",
        "altitude": "0-1000 mdpl",
        "rainfall": "2000-3000 mm/tahun",
        "soil_ph": "6.0-7.0",
        "soil_type": "Lempung berpasir, gembur",
        "yield_fresh": "8-12 ton/ha (akar)",
        "yield_dry": "1.6-2.4 ton/ha",
        "drying_ratio": 0.20,
        "fertilizer": {
            "organic": "20 ton/ha pupuk kandang",
            "urea": "120 kg/ha",
            "sp36": "150 kg/ha",
            "kcl": "100 kg/ha"
        },
        "pests": ["Ulat tanah", "Nematoda"],
        "diseases": ["Busuk akar", "Layu"],
        "harvest_indicator": "Akar besar, umur 6-8 bulan",
        "active_compounds": ["Saponin", "Flavonoid", "Alkaloid"],
        "health_benefits": [
            "Afrodisiak (tradisional)",
            "Meningkatkan stamina",
            "Antioksidan",
            "Adaptogen"
        ]
    },
    "Pasak Bumi": {
        "latin_name": "Eurycoma longifolia",
        "category": "Root",
        "cycle_months": 60,
        "planting_density": "10,000 tanaman/ha",
        "spacing": "100 cm x 100 cm",
        "altitude": "0-500 mdpl",
        "rainfall": "2500-4000 mm/tahun",
        "soil_ph": "5.5-6.5",
        "soil_type": "Lempung berpasir, drainase sempurna",
        "yield_fresh": "5-8 ton/ha (akar, umur 5 tahun)",
        "yield_dry": "1-1.6 ton/ha",
        "drying_ratio": 0.20,
        "fertilizer": {
            "organic": "30 ton/ha pupuk kandang (tahun 1)",
            "urea": "100 kg/ha/tahun",
            "sp36": "150 kg/ha/tahun",
            "kcl": "100 kg/ha/tahun"
        },
        "pests": ["Ulat daun", "Belalang"],
        "diseases": ["Busuk akar", "Bercak daun"],
        "harvest_indicator": "Umur minimal 5 tahun",
        "active_compounds": ["Eurycomanone", "Eurycomanol", "Quassinoid"],
        "health_benefits": [
            "Afrodisiak (penelitian klinis)",
            "Meningkatkan testosteron",
            "Anti-malaria (tradisional)",
            "Meningkatkan massa otot"
        ]
    }
}

# ===== MARKET PRICES (IDR) =====
MARKET_PRICES = {
    "Jahe Merah": {
        "fresh_local": 15000,  # per kg
        "dry_local": 80000,
        "dry_export": 250000,  # Japan, Europe
        "grade_a_premium": 350000
    },
    "Kunyit": {
        "fresh_local": 8000,
        "dry_local": 50000,
        "dry_export": 180000,
        "grade_a_premium": 250000
    },
    "Temulawak": {
        "fresh_local": 10000,
        "dry_local": 60000,
        "dry_export": 200000,
        "grade_a_premium": 280000
    },
    "Kencur": {
        "fresh_local": 12000,
        "dry_local": 70000,
        "dry_export": 220000,
        "grade_a_premium": 300000
    },
    "Sambiloto": {
        "fresh_local": 5000,
        "dry_local": 40000,
        "dry_export": 150000,
        "grade_a_premium": 200000
    },
    "Pegagan": {
        "fresh_local": 6000,
        "dry_local": 45000,
        "dry_export": 160000,
        "grade_a_premium": 220000
    },
    "Ginseng Jawa": {
        "fresh_local": 20000,
        "dry_local": 120000,
        "dry_export": 400000,
        "grade_a_premium": 600000
    },
    "Pasak Bumi": {
        "fresh_local": 50000,
        "dry_local": 300000,
        "dry_export": 1200000,
        "grade_a_premium": 2000000
    }
}

# ===== INVESTMENT COSTS (per hectare) =====
INVESTMENT_COSTS = {
    "Jahe Merah": {
        "land_prep": 5000000,
        "seeds": 40000000,  # 40,000 rimpang @ Rp 1,000
        "fertilizer_organic": 10000000,
        "fertilizer_chemical": 3000000,
        "pesticide": 2000000,
        "labor": 15000000,
        "irrigation": 3000000,
        "drying": 5000000,
        "packaging": 2000000,
        "certification": 5000000,
        "total": 90000000
    },
    "Kunyit": {
        "land_prep": 5000000,
        "seeds": 25000000,
        "fertilizer_organic": 7500000,
        "fertilizer_chemical": 2500000,
        "pesticide": 1500000,
        "labor": 12000000,
        "irrigation": 2500000,
        "drying": 4000000,
        "packaging": 1500000,
        "certification": 5000000,
        "total": 66500000
    },
    "Temulawak": {
        "land_prep": 5000000,
        "seeds": 30000000,
        "fertilizer_organic": 10000000,
        "fertilizer_chemical": 3000000,
        "pesticide": 2000000,
        "labor": 13000000,
        "irrigation": 2500000,
        "drying": 4500000,
        "packaging": 1500000,
        "certification": 5000000,
        "total": 76500000
    },
    "Kencur": {
        "land_prep": 4000000,
        "seeds": 20000000,
        "fertilizer_organic": 7500000,
        "fertilizer_chemical": 2000000,
        "pesticide": 1500000,
        "labor": 10000000,
        "irrigation": 2000000,
        "drying": 3000000,
        "packaging": 1000000,
        "certification": 5000000,
        "total": 56000000
    },
    "Sambiloto": {
        "land_prep": 3000000,
        "seeds": 10000000,
        "fertilizer_organic": 5000000,
        "fertilizer_chemical": 1500000,
        "pesticide": 1000000,
        "labor": 8000000,
        "irrigation": 1500000,
        "drying": 2500000,
        "packaging": 1000000,
        "certification": 5000000,
        "total": 38500000
    },
    "Pegagan": {
        "land_prep": 3000000,
        "seeds": 15000000,
        "fertilizer_organic": 7500000,
        "fertilizer_chemical": 2000000,
        "pesticide": 1000000,
        "labor": 10000000,
        "irrigation": 2000000,
        "drying": 3000000,
        "packaging": 1500000,
        "certification": 5000000,
        "total": 50000000
    },
    "Ginseng Jawa": {
        "land_prep": 5000000,
        "seeds": 20000000,
        "fertilizer_organic": 10000000,
        "fertilizer_chemical": 2500000,
        "pesticide": 1500000,
        "labor": 12000000,
        "irrigation": 2500000,
        "drying": 4000000,
        "packaging": 2000000,
        "certification": 5000000,
        "total": 64500000
    },
    "Pasak Bumi": {
        "land_prep": 8000000,
        "seeds": 50000000,
        "fertilizer_organic": 30000000,  # 5 years
        "fertilizer_chemical": 10000000,
        "pesticide": 5000000,
        "labor": 40000000,  # 5 years
        "irrigation": 5000000,
        "drying": 8000000,
        "packaging": 3000000,
        "certification": 10000000,
        "total": 169000000
    }
}


class MedicinalPlantsService:
    """Service class for medicinal plants calculations and data retrieval"""
    
    @staticmethod
    def get_cultivation_guide(species):
        """Get cultivation guide for a species"""
        return CULTIVATION_DATABASE.get(species, {})
    
    @staticmethod
    def get_market_data(species):
        """Get market price data for a species"""
        return MARKET_PRICES.get(species, {})
    
    @staticmethod
    def calculate_roi(species, area_ha=1.0, market_type="dry_export"):
        """
        Calculate ROI for medicinal plant cultivation
        
        Args:
            species: Plant species name
            area_ha: Cultivation area in hectares
            market_type: 'fresh_local', 'dry_local', 'dry_export', 'grade_a_premium'
        
        Returns:
            dict with investment, revenue, profit, roi_percent, payback_months
        """
        cultivation = CULTIVATION_DATABASE.get(species, {})
        prices = MARKET_PRICES.get(species, {})
        costs = INVESTMENT_COSTS.get(species, {})
        
        if not all([cultivation, prices, costs]):
            return None
        
        # Calculate investment
        investment = costs["total"] * area_ha
        
        # Calculate yield
        yield_dry = cultivation["yield_dry"].split("-")[0]  # Take lower estimate
        yield_dry_tons = float(yield_dry) * area_ha
        yield_dry_kg = yield_dry_tons * 1000
        
        # Calculate revenue
        price_per_kg = prices.get(market_type, prices["dry_local"])
        revenue = yield_dry_kg * price_per_kg
        
        # Calculate profit
        profit = revenue - investment
        
        # Calculate ROI
        roi_percent = (profit / investment) * 100 if investment > 0 else 0
        
        # Calculate payback period
        cycle_months = cultivation["cycle_months"]
        payback_months = cycle_months if roi_percent > 0 else 0
        
        return {
            "species": species,
            "area_ha": area_ha,
            "cycle_months": cycle_months,
            "investment": investment,
            "yield_kg": yield_dry_kg,
            "price_per_kg": price_per_kg,
            "revenue": revenue,
            "profit": profit,
            "roi_percent": roi_percent,
            "payback_months": payback_months,
            "margin_percent": (profit / revenue * 100) if revenue > 0 else 0
        }
    
    @staticmethod
    def calculate_drying_loss(fresh_weight_kg, species):
        """Calculate dry weight from fresh weight"""
        cultivation = CULTIVATION_DATABASE.get(species, {})
        drying_ratio = cultivation.get("drying_ratio", 0.20)
        dry_weight = fresh_weight_kg * drying_ratio
        loss_percent = (1 - drying_ratio) * 100
        
        return {
            "fresh_weight_kg": fresh_weight_kg,
            "dry_weight_kg": dry_weight,
            "loss_percent": loss_percent,
            "drying_ratio": drying_ratio
        }
    
    @staticmethod
    def compare_margins(area_ha=1.0, market_type="dry_export"):
        """Compare profit margins across all species"""
        results = []
        
        for species in CULTIVATION_DATABASE.keys():
            roi_data = MedicinalPlantsService.calculate_roi(species, area_ha, market_type)
            if roi_data:
                results.append({
                    "species": species,
                    "investment": roi_data["investment"],
                    "revenue": roi_data["revenue"],
                    "profit": roi_data["profit"],
                    "roi_percent": roi_data["roi_percent"],
                    "margin_percent": roi_data["margin_percent"],
                    "cycle_months": roi_data["cycle_months"]
                })
        
        # Sort by ROI descending
        results.sort(key=lambda x: x["roi_percent"], reverse=True)
        return results
    
    @staticmethod
    def get_certification_checklist(cert_type="GAP"):
        """Get certification checklist"""
        checklists = {
            "GAP": [
                "Lokasi lahan bebas dari kontaminasi industri",
                "Sumber air bersih dan teruji",
                "Penggunaan benih/bibit bersertifikat",
                "Pencatatan seluruh aktivitas budidaya",
                "Penggunaan pupuk organik terstandar",
                "Pestisida sesuai daftar positif (jika diperlukan)",
                "Peralatan panen dan pasca panen higienis",
                "Penyimpanan terpisah dari bahan kimia",
                "Pelatihan pekerja tentang GAP",
                "Audit internal minimal 2x/tahun"
            ],
            "Organic": [
                "Masa konversi lahan minimal 2 tahun",
                "Tidak ada penggunaan pestisida sintetis",
                "Tidak ada penggunaan pupuk kimia sintetis",
                "Tidak ada GMO (Genetically Modified Organism)",
                "Pencatatan lengkap (traceability)",
                "Buffer zone dari lahan konvensional (min 3m)",
                "Sertifikat kompos/pupuk organik",
                "Audit tahunan oleh lembaga sertifikasi",
                "Biaya sertifikasi: Rp 15-25 juta/tahun",
                "Lembaga: Inofice, Biocert, Control Union"
            ],
            "Halal": [
                "Tidak ada kontaminasi bahan haram",
                "Peralatan tidak digunakan untuk produk haram",
                "Penyimpanan terpisah dari produk non-halal",
                "Pekerja memahami prinsip halal",
                "Dokumentasi proses produksi",
                "Audit oleh LPPOM MUI",
                "Biaya sertifikasi: Rp 3-10 juta",
                "Masa berlaku: 2 tahun",
                "Wajib untuk ekspor ke negara Muslim",
                "Nilai tambah: premium price 10-20%"
            ]
        }
        return checklists.get(cert_type, [])
