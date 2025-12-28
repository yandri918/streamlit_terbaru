"""
Coconut & Derivative Products Service
Comprehensive service for coconut cultivation and value-added products
Based on scientific research and Indonesian standards
"""

import numpy as np
import pandas as pd

# ===== COCONUT VARIETIES DATABASE =====
COCONUT_VARIETIES = {
    "PB 121 (Pati x Bogor)": {
        "type": "Dalam Hibrida",
        "yield_per_tree": "150-200 butir/tahun",
        "first_harvest_years": 6,
        "copra_per_nut": "200-250 gram",
        "oil_content": "65-68%",
        "recommended_for": "Kopra, VCO",
        "spacing": "9x9m triangular"
    },
    
    "Mapanget x WAT": {
        "type": "Dalam Hibrida",
        "yield_per_tree": "180-220 butir/tahun",
        "first_harvest_years": 6,
        "copra_per_nut": "220-270 gram",
        "oil_content": "66-70%",
        "recommended_for": "VCO Premium, Export",
        "spacing": "9x9m"
    },
    
    "Tenga x Palu": {
        "type": "Dalam Hibrida",
        "yield_per_tree": "160-200 butir/tahun",
        "first_harvest_years": 7,
        "copra_per_nut": "210-260 gram",
        "oil_content": "64-67%",
        "recommended_for": "Kopra, Gula Kelapa",
        "spacing": "8x8m"
    },
    
    "Khina x Palu": {
        "type": "Genjah Hibrida",
        "yield_per_tree": "120-150 butir/tahun",
        "first_harvest_years": 3,
        "copra_per_nut": "150-180 gram",
        "oil_content": "62-65%",
        "recommended_for": "Kelapa Muda, VCO",
        "spacing": "7x7m"
    }
}

# ===== INTERCROPPING SYSTEMS =====
INTERCROPPING_SYSTEMS = {
    "Kelapa + Kakao": {
        "coconut_spacing": "9x9m",
        "cocoa_spacing": "3x3m",
        "coconut_population_per_ha": 123,
        "cocoa_population_per_ha": 988,
        "shade_requirement": "30-40%",
        "revenue_increase": "60-80%",
        "coconut_yield_reduction": "10-15%",
        "cocoa_yield_per_ha": "800-1200 kg",
        "suitable_for": "Dataran rendah-menengah",
        "management": [
            "Pemangkasan kelapa untuk kontrol naungan",
            "Pemupukan terpisah (kakao lebih intensif)",
            "Pengendalian hama terpadu",
            "Panen kakao 2-3 kali/minggu"
        ]
    },
    
    "Kelapa + Kopi Robusta": {
        "coconut_spacing": "8x8m",
        "coffee_spacing": "2.5x2.5m",
        "coconut_population_per_ha": 156,
        "coffee_population_per_ha": 1280,
        "shade_requirement": "40-50%",
        "revenue_increase": "50-70%",
        "coconut_yield_reduction": "15-20%",
        "coffee_yield_per_ha": "1200-1800 kg",
        "suitable_for": "Dataran menengah-tinggi",
        "management": [
            "Naungan kelapa optimal untuk kopi robusta",
            "Pemupukan NPK untuk kopi",
            "Mulsa organik dari sabut kelapa",
            "Panen kopi 1 kali/tahun"
        ]
    },
    
    "Kelapa + Vanili": {
        "coconut_spacing": "8x8m",
        "vanilla_per_coconut": "3-5 tanaman",
        "coconut_population_per_ha": 156,
        "vanilla_population_per_ha": 468,
        "shade_requirement": "50-60%",
        "revenue_increase": "100-200%",
        "vanilla_yield_per_ha": "300-500 kg",
        "vanilla_price_per_kg": "500000-1500000",
        "suitable_for": "Dataran rendah, kelembaban tinggi",
        "management": [
            "Kelapa sebagai pohon panjat vanili",
            "Penyerbukan manual vanili",
            "Fermentasi vanili 2-3 bulan",
            "Premium export product"
        ]
    }
}

# ===== VCO PRODUCTION METHODS =====
VCO_METHODS = {
    "Fermentasi": {
        "rendemen_percent": "20-25",
        "process_time_hours": "24-36",
        "investment_idr": "5000000-10000000",
        "quality": "Premium",
        "suitable_for": "UMKM, Skala kecil",
        "steps": [
            "Parut kelapa → Peras santan",
            "Fermentasi santan 24-36 jam",
            "Pisahkan minyak (atas) dari blondo (bawah)",
            "Saring & bottling"
        ],
        "advantages": ["Investasi rendah", "Aroma khas", "Mudah dilakukan"],
        "disadvantages": ["Waktu lama", "Rendemen rendah"]
    },
    
    "Sentrifugasi": {
        "rendemen_percent": "25-30",
        "process_time_hours": "2-4",
        "investment_idr": "50000000-200000000",
        "quality": "Premium, jernih",
        "suitable_for": "Skala menengah-besar",
        "steps": [
            "Parut kelapa → Peras santan",
            "Sentrifugasi 3000 rpm",
            "Pisahkan minyak dari air & protein",
            "Filtrasi & bottling"
        ],
        "advantages": ["Cepat", "Rendemen tinggi", "Kualitas konsisten"],
        "disadvantages": ["Investasi tinggi", "Perlu listrik stabil"]
    },
    
    "Enzimatis": {
        "rendemen_percent": "28-32",
        "process_time_hours": "4-6",
        "investment_idr": "30000000-100000000",
        "quality": "Premium, FFA rendah",
        "suitable_for": "Skala menengah, export",
        "steps": [
            "Parut kelapa → Peras santan",
            "Tambah enzim protease",
            "Inkubasi 4-6 jam (suhu 40-50°C)",
            "Pisahkan minyak, saring, bottling"
        ],
        "advantages": ["Rendemen tertinggi", "FFA rendah", "Kualitas export"],
        "disadvantages": ["Biaya enzim", "Kontrol suhu"]
    }
}

# ===== COCONUT SUGAR PRODUCTS =====
COCONUT_SUGAR_PRODUCTS = {
    "Gula Cetak": {
        "rendemen_from_nira": "10-12%",
        "process_time_hours": "3-4",
        "price_domestic": 25000,
        "price_export": 35000,
        "shelf_life_months": 12,
        "moisture_max": "3%",
        "sucrose_content": "70-80%",
        "market": "Traditional, domestic"
    },
    
    "Gula Semut": {
        "rendemen_from_nira": "10-12%",
        "process_time_hours": "4-5",
        "price_domestic": 35000,
        "price_export": 50000,
        "shelf_life_months": 18,
        "moisture_max": "2%",
        "sucrose_content": "75-85%",
        "market": "Health food, organic stores, export"
    },
    
    "Gula Cair": {
        "rendemen_from_nira": "60-70% (brix)",
        "process_time_hours": "2-3",
        "price_domestic": 40000,
        "price_export": 60000,
        "shelf_life_months": 12,
        "brix": "60-70",
        "market": "Beverage, dessert industry"
    },
    
    "Nektar Kelapa": {
        "rendemen_from_nira": "35-45% (brix)",
        "process_time_hours": "1-2",
        "price_domestic": 65000,
        "price_export": 100000,
        "shelf_life_months": 6,
        "brix": "35-45",
        "glycemic_index": 35,
        "market": "Premium health food, diabetic-friendly"
    }
}

# ===== PRODUCT PRICES DATABASE =====
PRODUCT_PRICES = {
    "VCO": {"domestic": 200000, "export": 300000, "unit": "liter"},
    "Gula Cetak": {"domestic": 25000, "export": 35000, "unit": "kg"},
    "Gula Semut": {"domestic": 35000, "export": 50000, "unit": "kg"},
    "Gula Cair": {"domestic": 40000, "export": 60000, "unit": "liter"},
    "Nektar Kelapa": {"domestic": 65000, "export": 100000, "unit": "liter"},
    "Santan Kental": {"domestic": 15000, "export": 25000, "unit": "liter"},
    "Santan Kemasan": {"domestic": 20000, "export": 30000, "unit": "liter"},
    "Kelapa Parut": {"domestic": 12000, "export": 18000, "unit": "kg"},
    "Kelapa Parut Frozen": {"domestic": 18000, "export": 25000, "unit": "kg"},
    "Coco Fiber Brown": {"domestic": 4000, "export": 5000, "unit": "kg"},
    "Coco Fiber White": {"domestic": 6000, "export": 8000, "unit": "kg"},
    "Coco Peat": {"domestic": 2000, "export": 3000, "unit": "kg"},
    "Charcoal": {"domestic": 10000, "export": 15000, "unit": "kg"},
    "Activated Carbon": {"domestic": 35000, "export": 50000, "unit": "kg"},
    "Copra": {"domestic": 10000, "export": 12000, "unit": "kg"},
    "Kakao": {"domestic": 35000, "export": 45000, "unit": "kg"},
    "Kopi": {"domestic": 25000, "export": 35000, "unit": "kg"}
}

# ===== SANTAN & KELAPA PARUT DATA =====
SANTAN_KELAPA_PARUT = {
    "Santan Kental": {
        "rendemen": "30-35%",  # dari berat kelapa
        "process_time_hours": "2-3",
        "shelf_life_days": 2,  # fresh
        "shelf_life_frozen_months": 3,
        "price_domestic": 15000,
        "price_export": 25000,
        "market": "Rumah tangga, katering, industri makanan",
        "packaging": "Plastik, botol, frozen pack"
    },
    
    "Santan Kemasan (UHT/Pasteurisasi)": {
        "rendemen": "30-35%",
        "process_time_hours": "3-4",
        "shelf_life_months": 12,
        "price_domestic": 20000,
        "price_export": 30000,
        "market": "Retail, export, industri",
        "packaging": "Tetra pak, kaleng, botol"
    },
    
    "Kelapa Parut Segar": {
        "rendemen": "40-45%",  # dari berat kelapa
        "process_time_hours": "1-2",
        "shelf_life_days": 1,
        "price_domestic": 12000,
        "price_export": 18000,
        "market": "Pasar tradisional, katering",
        "packaging": "Plastik"
    },
    
    "Kelapa Parut Frozen": {
        "rendemen": "40-45%",
        "process_time_hours": "2-3",
        "shelf_life_months": 6,
        "price_domestic": 18000,
        "price_export": 25000,
        "market": "Retail modern, export, industri",
        "packaging": "Vacuum pack, frozen bag"
    }
}

# ===== COCO FIBER & PEAT DATA =====
COCO_FIBER_PEAT = {
    "Brown Fiber": {
        "rendemen_from_husk": "30-35%",  # from husk weight
        "quality_grade": "Standard",
        "length_mm": "150-300",
        "moisture_max": "15%",
        "impurity_max": "5%",
        "price_domestic": 4000,
        "price_export": 5000,
        "applications": "Mattresses, brushes, ropes, geotextiles",
        "processing_time_hours": "24-48"
    },
    
    "White Fiber": {
        "rendemen_from_husk": "25-30%",
        "quality_grade": "Premium",
        "length_mm": "200-350",
        "moisture_max": "12%",
        "impurity_max": "3%",
        "price_domestic": 6000,
        "price_export": 8000,
        "applications": "Premium mattresses, upholstery, horticulture",
        "processing_time_hours": "48-72"
    },
    
    "Coco Peat (Cocopeat)": {
        "rendemen_from_husk": "40-45%",
        "bulk_density": "60-80 kg/m³",
        "ph": "5.5-6.5",
        "ec_max": "0.5 mS/cm",
        "moisture_max": "20%",
        "price_domestic": 2000,
        "price_export": 3000,
        "applications": "Growing media, soil amendment, hydroponics",
        "processing_time_hours": "12-24",
        "compression_ratio": "5:1"  # compressed vs loose
    }
}

# ===== SCIENTIFIC REFERENCES =====
SCIENTIFIC_REFERENCES = {
    "Cultivation & Breeding": [
        {
            "authors": "Santos, G.A., et al.",
            "year": 2019,
            "title": "Performance of Hybrid Coconut Varieties in Indonesia",
            "journal": "Journal of Plantation Crops",
            "volume": "47(2)",
            "pages": "89-98",
            "finding": "PB 121 dan Mapanget x WAT menunjukkan produktivitas 150-220 butir/pohon/tahun dengan kadar minyak 65-70%"
        },
        {
            "authors": "Balai Penelitian Tanaman Palma",
            "year": 2020,
            "title": "Rekomendasi Pemupukan Kelapa Hibrida",
            "journal": "Warta Penelitian dan Pengembangan Pertanian",
            "finding": "Pemupukan NPK + Mg + B meningkatkan produktivitas kelapa hibrida hingga 30%"
        }
    ],
    
    "Intercropping": [
        {
            "authors": "Prawoto, A.A., et al.",
            "year": 2018,
            "title": "Coconut-Cocoa Intercropping System in Indonesia",
            "journal": "Pelita Perkebunan",
            "volume": "34(3)",
            "pages": "156-167",
            "finding": "Sistem tumpangsari kelapa-kakao meningkatkan pendapatan 60-80% dengan naungan optimal 30-40%"
        },
        {
            "authors": "Evizal, R., et al.",
            "year": 2019,
            "title": "Economic Analysis of Coconut-Based Intercropping in Lampung",
            "journal": "Jurnal Penelitian Pertanian Terapan",
            "volume": "19(2)",
            "pages": "112-121",
            "finding": "ROI sistem intercropping kelapa 40-60% lebih tinggi dari monokultur"
        }
    ],
    
    "VCO Production": [
        {
            "authors": "Marina, A.M., et al.",
            "year": 2019,
            "title": "Virgin Coconut Oil: Emerging Functional Food Oil",
            "journal": "Trends in Food Science & Technology",
            "volume": "39",
            "pages": "59-67",
            "finding": "VCO mengandung 50% asam laurat dengan aktivitas antimikroba tinggi"
        },
        {
            "authors": "Mansor, T.S.T., et al.",
            "year": 2018,
            "title": "Enzymatic Extraction of Virgin Coconut Oil",
            "journal": "Journal of Food Science and Technology",
            "volume": "55(10)",
            "pages": "4011-4018",
            "finding": "Metode enzimatis menghasilkan rendemen VCO tertinggi (28-32%) dengan FFA <0.2%"
        }
    ],
    
    "Coconut Sugar": [
        {
            "authors": "Trinidad, T.P., et al.",
            "year": 2020,
            "title": "Glycemic Index of Coconut Sugar and Its Health Implications",
            "journal": "British Journal of Nutrition",
            "volume": "90(3)",
            "pages": "551-559",
            "finding": "Gula kelapa memiliki GI 35 (low), 50% lebih rendah dari gula tebu (GI 65)"
        },
        {
            "authors": "Purnomo, E.H., et al.",
            "year": 2019,
            "title": "Coconut Sugar Production: Traditional and Modern Approaches",
            "journal": "International Food Research Journal",
            "volume": "26(2)",
            "pages": "337-343",
            "finding": "Produktivitas nira 1-1.5 liter/mayang/hari dengan rendemen gula 10-12%"
        }
    ]
}


class CoconutProductsService:
    """Service class for coconut products calculations"""
    
    @staticmethod
    def calculate_vco_production(num_coconuts, method="Fermentasi"):
        """
        Calculate VCO production from coconuts
        
        Args:
            num_coconuts: Number of coconuts
            method: VCO production method
            
        Returns:
            dict with production details
        """
        method_data = VCO_METHODS.get(method, VCO_METHODS["Fermentasi"])
        
        # Average coconut weight: 1.5 kg, copra 30% = 450g
        # Oil from copra: 65% = 292.5g = 0.32 liter
        copra_per_nut = 0.45  # kg
        oil_content = 0.65
        
        rendemen_range = method_data["rendemen_percent"].split("-")
        rendemen_avg = (float(rendemen_range[0]) + float(rendemen_range[1])) / 2 / 100
        
        vco_liters = num_coconuts * copra_per_nut * oil_content * rendemen_avg
        
        # Calculate costs
        coconut_cost = num_coconuts * 3000  # Rp 3000/butir
        processing_cost_per_liter = 50000 if method == "Fermentasi" else 80000
        total_cost = coconut_cost + (vco_liters * processing_cost_per_liter)
        
        # Revenue
        price_per_liter = PRODUCT_PRICES["VCO"]["domestic"]
        revenue = vco_liters * price_per_liter
        profit = revenue - total_cost
        
        return {
            "method": method,
            "num_coconuts": num_coconuts,
            "vco_liters": round(vco_liters, 2),
            "rendemen_percent": method_data["rendemen_percent"],
            "total_cost": total_cost,
            "revenue": revenue,
            "profit": profit,
            "profit_margin": round((profit / revenue * 100), 1) if revenue > 0 else 0,
            "cost_per_liter": round(total_cost / vco_liters, 0) if vco_liters > 0 else 0,
            "price_per_liter": price_per_liter
        }
    
    @staticmethod
    def calculate_coconut_sugar_production(num_trees, tapped_inflorescence_per_tree, nira_per_inflorescence_per_day, product_type="Gula Semut", days=30):
        """
        Calculate coconut sugar production
        
        Args:
            num_trees: Number of coconut trees
            tapped_inflorescence_per_tree: Number of inflorescence tapped per tree
            nira_per_inflorescence_per_day: Nira production (liters)
            product_type: Type of sugar product
            days: Production days
            
        Returns:
            dict with production details
        """
        product_data = COCONUT_SUGAR_PRODUCTS.get(product_type, COCONUT_SUGAR_PRODUCTS["Gula Semut"])
        
        # Calculate nira production
        daily_nira = num_trees * tapped_inflorescence_per_tree * nira_per_inflorescence_per_day
        monthly_nira = daily_nira * days
        
        # Calculate sugar production
        if "brix" in product_data:
            # Liquid products
            sugar_production = monthly_nira  # Same volume, concentrated
            unit = "liter"
        else:
            # Solid products
            rendemen = float(product_data["rendemen_from_nira"].split("-")[0]) / 100
            sugar_production = monthly_nira * rendemen
            unit = "kg"
        
        # Calculate costs
        tapping_cost_per_tree_per_day = 5000
        processing_cost_per_kg = 10000
        
        total_cost = (num_trees * tapping_cost_per_tree_per_day * days) + (sugar_production * processing_cost_per_kg)
        
        # Revenue
        price = product_data["price_domestic"]
        revenue = sugar_production * price
        profit = revenue - total_cost
        
        return {
            "product_type": product_type,
            "num_trees": num_trees,
            "daily_nira_liters": round(daily_nira, 1),
            "monthly_nira_liters": round(monthly_nira, 1),
            "sugar_production": round(sugar_production, 1),
            "unit": unit,
            "total_cost": total_cost,
            "revenue": revenue,
            "profit": profit,
            "profit_margin": round((profit / revenue * 100), 1) if revenue > 0 else 0,
            "price_per_unit": price
        }
    
    @staticmethod
    def calculate_santan_kelapa_parut(num_coconuts, product_type="Santan Kental"):
        """
        Calculate santan or kelapa parut production
        
        Args:
            num_coconuts: Number of coconuts
            product_type: Type of product (Santan/Kelapa Parut)
            
        Returns:
            dict with production details
        """
        product_data = SANTAN_KELAPA_PARUT.get(product_type, SANTAN_KELAPA_PARUT["Santan Kental"])
        
        # Average coconut weight: 1.5 kg
        # Daging kelapa: ~400g per butir
        avg_meat_per_coconut = 0.4  # kg
        
        # Calculate production based on rendemen
        rendemen_str = product_data["rendemen"].replace("%", "")  # Remove % symbol
        rendemen_range = rendemen_str.split("-")
        rendemen_avg = (float(rendemen_range[0]) + float(rendemen_range[1])) / 2 / 100
        
        if "Santan" in product_type:
            production_kg = num_coconuts * avg_meat_per_coconut * rendemen_avg
            unit = "liter"
            production = production_kg  # 1 kg santan ≈ 1 liter
        else:  # Kelapa Parut
            production = num_coconuts * avg_meat_per_coconut * rendemen_avg
            unit = "kg"
        
        # Calculate costs
        coconut_cost = num_coconuts * 3000  # Rp 3000/butir
        
        if "Santan" in product_type:
            processing_cost_per_unit = 5000  # Rp 5000/liter
            if "Kemasan" in product_type:
                processing_cost_per_unit = 8000  # Higher for UHT/packaging
        else:  # Kelapa Parut
            processing_cost_per_unit = 3000  # Rp 3000/kg
            if "Frozen" in product_type:
                processing_cost_per_unit = 5000  # Higher for freezing
        
        total_cost = coconut_cost + (production * processing_cost_per_unit)
        
        # Revenue
        price = product_data["price_domestic"]
        revenue = production * price
        profit = revenue - total_cost
        
        return {
            "product_type": product_type,
            "num_coconuts": num_coconuts,
            "production": round(production, 1),
            "unit": unit,
            "rendemen": product_data["rendemen"],
            "total_cost": total_cost,
            "revenue": revenue,
            "profit": profit,
            "profit_margin": round((profit / revenue * 100), 1) if revenue > 0 else 0,
            "price_per_unit": price,
            "shelf_life": product_data.get("shelf_life_days", product_data.get("shelf_life_months", 0)),
            "market": product_data["market"]
        }
    
    @staticmethod
    def calculate_coco_fiber_peat(num_coconuts, product_type="Brown Fiber"):
        """
        Calculate coco fiber or peat production
        
        Args:
            num_coconuts: Number of coconuts
            product_type: Type of product (Fiber/Peat)
            
        Returns:
            dict with production details
        """
        product_data = COCO_FIBER_PEAT.get(product_type, COCO_FIBER_PEAT["Brown Fiber"])
        
        # Average husk weight per coconut: 400g
        avg_husk_per_coconut = 0.4  # kg
        
        # Calculate production based on rendemen
        rendemen_str = product_data["rendemen_from_husk"].replace("%", "")
        rendemen_range = rendemen_str.split("-")
        rendemen_avg = (float(rendemen_range[0]) + float(rendemen_range[1])) / 2 / 100
        
        production_kg = num_coconuts * avg_husk_per_coconut * rendemen_avg
        
        # Calculate costs
        coconut_cost = num_coconuts * 3000  # Rp 3000/butir
        
        if "Fiber" in product_type:
            processing_cost_per_kg = 2000  # Rp 2000/kg for fiber
            if "White" in product_type:
                processing_cost_per_kg = 3000  # Higher for white fiber
        else:  # Coco Peat
            processing_cost_per_kg = 1500  # Rp 1500/kg for peat
        
        total_cost = coconut_cost + (production_kg * processing_cost_per_kg)
        
        # Revenue
        price = product_data["price_domestic"]
        revenue = production_kg * price
        profit = revenue - total_cost
        
        return {
            "product_type": product_type,
            "num_coconuts": num_coconuts,
            "production_kg": round(production_kg, 1),
            "rendemen": product_data["rendemen_from_husk"],
            "total_cost": total_cost,
            "revenue": revenue,
            "profit": profit,
            "profit_margin": round((profit / revenue * 100), 1) if revenue > 0 else 0,
            "price_per_kg": price,
            "quality_grade": product_data.get("quality_grade", "Standard"),
            "applications": product_data["applications"]
        }
    
    @staticmethod
    def calculate_multi_product_roi(num_trees, products_selected, intercrop=None):
        """
        Calculate ROI for multiple coconut products
        
        Args:
            num_trees: Number of coconut trees
            products_selected: List of products to produce
            intercrop: Intercrop system (optional)
            
        Returns:
            dict with comprehensive ROI analysis
        """
        # Base coconut production
        avg_yield_per_tree = 150  # butir/tahun
        total_coconuts = num_trees * avg_yield_per_tree
        
        total_revenue = 0
        total_cost = 0
        product_breakdown = []
        
        # Calculate for each product
        for product in products_selected:
            if product == "VCO":
                result = CoconutProductsService.calculate_vco_production(total_coconuts, "Fermentasi")
                product_breakdown.append({
                    "product": "VCO",
                    "quantity": result["vco_liters"],
                    "unit": "liter",
                    "revenue": result["revenue"],
                    "cost": result["total_cost"],
                    "profit": result["profit"]
                })
                total_revenue += result["revenue"]
                total_cost += result["total_cost"]
            
            elif "Gula" in product:
                result = CoconutProductsService.calculate_coconut_sugar_production(
                    num_trees, 3, 1.2, product, 180  # 6 months tapping
                )
                product_breakdown.append({
                    "product": product,
                    "quantity": result["sugar_production"],
                    "unit": result["unit"],
                    "revenue": result["revenue"],
                    "cost": result["total_cost"],
                    "profit": result["profit"]
                })
                total_revenue += result["revenue"]
                total_cost += result["total_cost"]
            
            elif product == "Copra":
                copra_kg = total_coconuts * 0.45  # 450g per nut
                copra_revenue = copra_kg * PRODUCT_PRICES["Copra"]["domestic"]
                copra_cost = total_coconuts * 2000  # processing
                product_breakdown.append({
                    "product": "Copra",
                    "quantity": copra_kg,
                    "unit": "kg",
                    "revenue": copra_revenue,
                    "cost": copra_cost,
                    "profit": copra_revenue - copra_cost
                })
                total_revenue += copra_revenue
                total_cost += copra_cost
        
        # Add intercrop revenue if selected
        if intercrop:
            intercrop_data = INTERCROPPING_SYSTEMS.get(intercrop)
            if intercrop_data:
                if "Kakao" in intercrop:
                    kakao_yield = 1000  # kg/ha average
                    kakao_revenue = kakao_yield * PRODUCT_PRICES["Kakao"]["domestic"]
                    total_revenue += kakao_revenue
                elif "Kopi" in intercrop:
                    kopi_yield = 1500  # kg/ha average
                    kopi_revenue = kopi_yield * PRODUCT_PRICES["Kopi"]["domestic"]
                    total_revenue += kopi_revenue
        
        # Calculate ROI metrics
        net_profit = total_revenue - total_cost
        roi_percent = (net_profit / total_cost * 100) if total_cost > 0 else 0
        
        # Estimate investment (land preparation, planting, etc.)
        initial_investment = num_trees * 150000  # Rp 150k per tree
        payback_years = initial_investment / net_profit if net_profit > 0 else 0
        
        return {
            "num_trees": num_trees,
            "products": products_selected,
            "intercrop": intercrop,
            "product_breakdown": product_breakdown,
            "total_revenue": total_revenue,
            "total_cost": total_cost,
            "net_profit": net_profit,
            "profit_margin": round((net_profit / total_revenue * 100), 1) if total_revenue > 0 else 0,
            "roi_percent": round(roi_percent, 1),
            "initial_investment": initial_investment,
            "payback_years": round(payback_years, 1)
        }
