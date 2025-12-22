import os
import pandas as pd
import numpy as np
from flask import current_app
from werkzeug.utils import secure_filename
import cv2
from inference_sdk import InferenceHTTPClient
import uuid
from app.ml_models.model_loader import ModelLoader

# --- MANAJEMEN DATASET ---
def get_dataset_path(filename):
    """Get path to dataset file."""
    return os.path.join(current_app.config['ML_MODELS_PATH'], filename)

class MLService:
    """
    Berisi semua logika bisnis untuk fungsionalitas Machine Learning.
    Ini dipanggil oleh file routes/ml.py.
    """

    @staticmethod
    def recommend_crop(data):
        """Recommend crop based on soil and environmental conditions."""
        crop_model = ModelLoader.get_model('crop_recommendation')
        if crop_model is None:
            current_app.logger.warning("⚠️ Crop recommendation model not available, using fallback")
            # Fallback logic based on NPK ratios
            n = float(data.get('n_value', 0))
            p = float(data.get('p_value', 0))
            k = float(data.get('k_value', 0))
            
            # Simple heuristic
            if n > 80 and p > 40: return "Rice"
            elif k > 40: return "Cotton"
            elif p > 50: return "Wheat"
            else: return "Maize"
        
        # Nama fitur harus sama persis dengan saat pelatihan
        features = [
            float(data.get('n_value', 0)),
            float(data.get('p_value', 0)),
            float(data.get('k_value', 0)),
            float(data.get('temperature', 0)),
            float(data.get('humidity', 0)),
            float(data.get('ph', 0)),
            float(data.get('rainfall', 0))
        ]
        input_data = np.array([features])
        
        # Get prediction and probability if available
        prediction = crop_model.predict(input_data)[0]
        crop_name = prediction.capitalize()
        
        confidence = 0.0
        if hasattr(crop_model, 'predict_proba'):
            probs = crop_model.predict_proba(input_data)[0]
            confidence = round(max(probs) * 100, 2)
        else:
            confidence = 85.0  # Default confidence if predict_proba not available

        # Detailed crop knowledge
        crop_details = {
            "Rice": {
                "description": "Padi adalah tanaman pangan utama yang membutuhkan banyak air.",
                "optimal_conditions": "Suhu 20-35°C, Curah hujan tinggi, pH 5.5-7.0.",
                "care_tips": "Pastikan pengairan cukup (tergenang), berikan pupuk Urea dan SP-36 secara teratur."
            },
            "Maize": {
                "description": "Jagung adalah tanaman serbaguna untuk pangan dan pakan ternak.",
                "optimal_conditions": "Suhu 20-30°C, Tanah gembur kaya organik, pH 5.8-7.0.",
                "care_tips": "Lakukan pembumbunan akar, waspadai ulat grayak, dan pupuk NPK seimbang."
            },
            "Chickpea": {
                "description": "Kacang Arab, sumber protein nabati tinggi.",
                "optimal_conditions": "Iklim sejuk hingga hangat, tanah berpasir/lempung, pH 6.0-9.0.",
                "care_tips": "Hindari tanah yang tergenang air, butuh sinar matahari penuh."
            },
            "Kidneybeans": {
                "description": "Kacang Merah, kaya serat dan protein.",
                "optimal_conditions": "Suhu 15-25°C, Curah hujan sedang, pH 6.0-7.0.",
                "care_tips": "Perlu ajir/lanjaran untuk merambat, jaga kelembaban tanah."
            },
            "Pigeonpeas": {
                "description": "Kacang Gude, tanaman tahan kering.",
                "optimal_conditions": "Suhu 18-30°C, Tahan kekeringan, pH 5.0-7.0.",
                "care_tips": "Bisa ditanam sebagai tanaman sela atau pagar hidup."
            },
            "Mothbeans": {
                "description": "Kacang Moth, sangat tahan kekeringan.",
                "optimal_conditions": "Iklim kering/semi-kering, Suhu tinggi, pH 6.5-8.0.",
                "care_tips": "Sangat minim perawatan, hindari penyiraman berlebih."
            },
            "Mungbean": {
                "description": "Kacang Hijau, umur pendek dan mudah tumbuh.",
                "optimal_conditions": "Suhu 25-35°C, Iklim panas, pH 5.8-7.0.",
                "care_tips": "Panen serempak saat polong berwarna hitam/coklat tua."
            },
            "Blackgram": {
                "description": "Kacang Hitam (Urad Dal), populer di Asia Selatan.",
                "optimal_conditions": "Suhu 25-35°C, Tanah liat berpasir, pH 6.0-7.0.",
                "care_tips": "Peka terhadap genangan air, butuh drainase baik."
            },
            "Lentil": {
                "description": "Lentil, tanaman legum biji-bijian.",
                "optimal_conditions": "Iklim dingin, Tanah berpasir, pH 6.0-7.5.",
                "care_tips": "Tanam di akhir musim hujan atau awal musim kemarau."
            },
            "Pomegranate": {
                "description": "Delima, tanaman buah perdu.",
                "optimal_conditions": "Iklim semi-kering, Suhu panas, pH 5.5-7.0.",
                "care_tips": "Lakukan pemangkasan rutin untuk bentuk pohon dan produksi buah."
            },
            "Banana": {
                "description": "Pisang, buah tropis populer.",
                "optimal_conditions": "Suhu 27°C, Curah hujan tinggi merata, pH 6.0-7.0.",
                "care_tips": "Butuh banyak air dan pupuk Kalium, bersihkan anakan secara rutin."
            },
            "Mango": {
                "description": "Mangga, raja buah tropis.",
                "optimal_conditions": "Suhu 24-30°C, Musim kering tegas untuk pembungaan, pH 5.5-7.5.",
                "care_tips": "Pangkas cabang air, berikan paclobutrazol untuk memacu bunga di luar musim."
            },
            "Grapes": {
                "description": "Anggur, tanaman merambat.",
                "optimal_conditions": "Iklim kering saat pematangan, Suhu hangat, pH 6.5-7.5.",
                "care_tips": "Sangat butuh pemangkasan dan penjarangan buah."
            },
            "Watermelon": {
                "description": "Semangka, tanaman merambat semusim.",
                "optimal_conditions": "Suhu panas 25-30°C, Tanah berpasir, pH 6.0-7.0.",
                "care_tips": "Kurangi penyiraman menjelang panen untuk meningkatkan kemanisan."
            },
            "Muskmelon": {
                "description": "Melon, buah segar beraroma wangi.",
                "optimal_conditions": "Suhu 25-30°C, Kelembaban rendah, pH 6.0-7.0.",
                "care_tips": "Hindari air hujan langsung pada buah (gunakan mulsa/greenhouse)."
            },
            "Apple": {
                "description": "Apel, tanaman buah subtropis.",
                "optimal_conditions": "Suhu sejuk, Butuh chilling hours, pH 6.0-7.0.",
                "care_tips": "Hanya cocok di dataran tinggi (Batu, Malang) di Indonesia."
            },
            "Orange": {
                "description": "Jeruk, kaya vitamin C.",
                "optimal_conditions": "Suhu 13-35°C, Sinar matahari penuh, pH 6.0-7.0.",
                "care_tips": "Waspadai penyakit CVPD, lakukan pemupukan berimbang."
            },
            "Papaya": {
                "description": "Pepaya, buah sepanjang tahun.",
                "optimal_conditions": "Suhu 21-33°C, Tanah gembur drainase baik, pH 6.0-7.0.",
                "care_tips": "Sangat rentan busuk akar jika tergenang air."
            },
            "Coconut": {
                "description": "Kelapa, pohon kehidupan.",
                "optimal_conditions": "Suhu 27°C, Curah hujan tinggi, pH 5.5-7.0.",
                "care_tips": "Berikan garam (NaCl) dan pupuk KCL untuk produksi optimal."
            },
            "Cotton": {
                "description": "Kapas, tanaman serat.",
                "optimal_conditions": "Suhu panas, Musim kering panjang saat panen, pH 6.0-8.0.",
                "care_tips": "Pengendalian hama (bollworm) sangat krusial."
            },
            "Jute": {
                "description": "Yute, serat emas.",
                "optimal_conditions": "Suhu 24-37°C, Kelembaban tinggi, pH 6.0-7.0.",
                "care_tips": "Butuh air rendaman untuk proses pembusukan batang (retting)."
            },
            "Coffee": {
                "description": "Kopi, tanaman perkebunan bernilai tinggi.",
                "optimal_conditions": "Suhu 18-24°C (Arabika), Naungan cukup, pH 5.0-6.0.",
                "care_tips": "Pangkas lepas panen, jaga naungan, dan pemupukan organik."
            }
        }

        details = crop_details.get(crop_name, {
            "description": f"Tanaman {crop_name} direkomendasikan berdasarkan kondisi tanah Anda.",
            "optimal_conditions": "Sesuaikan dengan standar budidaya tanaman ini.",
            "care_tips": "Lakukan pemupukan dan pengairan sesuai SOP."
        })

        return {
            "crop": crop_name,
            "confidence": confidence,
            "details": details
        }


    @staticmethod
    def predict_yield(data):
        """Predict crop yield based on environmental factors."""
        yield_model = ModelLoader.get_model('yield_prediction')
        if yield_model is None:
            current_app.logger.warning("⚠️ Yield prediction model not available, using fallback")
            # Fallback: simple estimation based on NPK
            n = float(data.get('nitrogen', 0))
            p = float(data.get('phosphorus', 0))
            k = float(data.get('potassium', 0))
            # Simple linear estimation (ton/ha)
            estimated_yield = (n * 0.03 + p * 0.05 + k * 0.02) / 10
            return max(1.0, min(10.0, round(estimated_yield, 2)))
        
        # Nama fitur harus sama persis dengan saat pelatihan
        features = [
            float(data.get('nitrogen', 0)),
            float(data.get('phosphorus', 0)),
            float(data.get('potassium', 0)),
            float(data.get('temperature', 0)),
            float(data.get('rainfall', 0)),
            float(data.get('ph', 0))
        ]
        input_data = np.array([features])
        prediction = yield_model.predict(input_data)[0]
        return round(float(prediction) / 1000, 2) # Konversi dari kg/ha ke ton/ha

    @staticmethod
    def predict_yield_advanced(data):
        advanced_model = ModelLoader.get_model('advanced_yield')
        explainer = ModelLoader.get_model('shap_explainer')
        
        feature_names = ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Rainfall', 'pH']
        features = [float(data.get(name.lower(), 0)) for name in feature_names]
        
        # Fallback if models are not available
        if advanced_model is None or explainer is None:
            current_app.logger.warning("⚠️ Advanced yield model not available, using fallback with insights")
            
            # 1. Calculate Yield (Simple Formula)
            n, p, k, temp, rain, ph = features
            # Base yield + nutrient contribution - stress factors
            estimated_yield = (n * 0.025 + p * 0.045 + k * 0.015) 
            
            # Adjust for environmental factors (simplified logic)
            if temp < 20 or temp > 35: estimated_yield *= 0.8
            if rain < 100 or rain > 300: estimated_yield *= 0.9
            if ph < 5.5 or ph > 7.5: estimated_yield *= 0.85
            
            estimated_yield = max(1.0, min(12.0, round(estimated_yield / 10, 2))) # Scale to ton/ha
            
            # 2. Generate Mock Feature Importances (Logic-based)
            # Nutrients usually have high importance
            importances = [0.35, 0.25, 0.15, 0.10, 0.10, 0.05]
            feature_importance_dict = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)
            
            # 3. Generate Mock SHAP Values (Directional)
            # If value is high/optimal -> positive SHAP, else negative
            shap_dict = {}
            base_value = 4.5 # Average yield
            
            # Nitrogen (Optimal ~100)
            shap_dict['Nitrogen'] = 0.5 if n > 80 else -0.2
            # Phosphorus (Optimal ~50)
            shap_dict['Phosphorus'] = 0.4 if p > 40 else -0.1
            # Potassium (Optimal ~50)
            shap_dict['Potassium'] = 0.2 if k > 40 else -0.1
            # Temperature (Optimal 25-30)
            shap_dict['Temperature'] = 0.3 if 25 <= temp <= 30 else -0.3
            # Rainfall (Optimal 150-250)
            shap_dict['Rainfall'] = 0.2 if 150 <= rain <= 250 else -0.2
            # pH (Optimal 6-7)
            shap_dict['pH'] = 0.1 if 6.0 <= ph <= 7.0 else -0.2
            
            return {
                'predicted_yield_ton_ha': estimated_yield,
                'feature_importances': feature_importance_dict,
                'shap_values': shap_dict,
                'base_value': base_value
            }

        input_data = pd.DataFrame([features], columns=feature_names)
        
        prediction = advanced_model.predict(input_data)[0]
        importances = advanced_model.feature_importances_
        feature_importance_dict = sorted(zip(feature_names, [float(i) for i in importances]), key=lambda x: x[1], reverse=True)
        shap_values = explainer.shap_values(input_data)
        shap_dict = {name: round(float(val), 2) for name, val in zip(feature_names, shap_values[0])}
        
        return {
            'predicted_yield_ton_ha': round(float(prediction) / 1000, 2),
            'feature_importances': feature_importance_dict,
            'shap_values': shap_dict,
            'base_value': round(float(explainer.expected_value) / 1000, 2)
        }

    @staticmethod
    def calculate_fertilizer_bags(nutrient_needed, nutrient_amount_kg, fertilizer_type):
        from app.services.knowledge_service import KnowledgeService
        FERTILIZER_DATA = KnowledgeService.get_fertilizer_data()
        
        fert_data = FERTILIZER_DATA.get(fertilizer_type)
        if not fert_data:
            return None
            
        nutrient_percentage = fert_data["content"].get(nutrient_needed, 0)
        if nutrient_percentage == 0:
            return None
            
        required_fertilizer_kg = nutrient_amount_kg / nutrient_percentage
        return {
            'required_kg': round(required_fertilizer_kg, 2),
            'fertilizer_name': fert_data["name"],
            'nutrient_needed': nutrient_needed,
            'nutrient_amount_kg': nutrient_amount_kg
        }


    @staticmethod
    def generate_yield_plan(commodity=None, target_yield_ton_ha=None):
        """Generate comprehensive plan to achieve target yield with commodity-specific recommendations."""
        from app.data.yield_benchmarks import YieldBenchmarks
        
        # Handle both old (single param) and new (two params) signatures
        if target_yield_ton_ha is None and commodity is not None:
            # Old signature: only target_yield_ton_ha provided as first param
            target_yield_ton_ha = float(commodity) if isinstance(commodity, (int, float, str)) else None
            commodity = "umum"  # Default to general
        
        if target_yield_ton_ha is None:
            raise ValueError("target_yield_ton_ha is required")
        
        # If commodity is specified and supported, use benchmark data
        if commodity and commodity != "umum":
            commodity_data = YieldBenchmarks.get_commodity_data().get(commodity)
            if commodity_data:
                return MLService._generate_commodity_specific_plan(commodity, target_yield_ton_ha, commodity_data)
        
        # Fallback to EDA dataset for general/unsupported commodities
        dataset_path = get_dataset_path('EDA_500.csv')
        if not os.path.exists(dataset_path):
            raise RuntimeError("Dataset EDA_500.csv tidak ditemukan.")
        
        df = pd.read_csv(dataset_path)
        df['Yield'] = pd.to_numeric(df['Yield'], errors='coerce')
        df.dropna(subset=['Yield'], inplace=True)
        
        target_yield_kg = float(target_yield_ton_ha) * 1000
        best_match_row = df.iloc[(df['Yield'] - target_yield_kg).abs().argsort()[:1]]
        
        if best_match_row.empty:
            return None

        result = best_match_row.iloc[0]
        plan = {
            "commodity_name": "Umum",
            "target_yield": target_yield_ton_ha,
            "feasibility": "unknown",
            "npk_requirements": {
                "Nitrogen (kg/ha)": round(float(result['Nitrogen']), 2),
                "Phosphorus (kg/ha)": round(float(result['Phosphorus']), 2),
                "Potassium (kg/ha)": round(float(result['Potassium']), 2)
            },
            "environmental_conditions": {
                "Temperature (°C)": round(float(result['Temperature']), 2),
                "Rainfall (mm)": round(float(result['Rainfall']), 2),
                "pH Tanah": round(float(result['pH']), 2)
            },
            "actual_yield_from_data": f"{round(float(result['Yield'])/1000, 2)} ton/ha"
        }
        return plan
    
    @staticmethod
    def _generate_commodity_specific_plan(commodity, target_yield, commodity_data):
        """Generate detailed commodity-specific yield plan."""
        from app.data.yield_benchmarks import YieldBenchmarks
        
        # Assess feasibility
        yield_category = YieldBenchmarks.get_yield_category(commodity, target_yield)
        benchmarks = commodity_data["benchmarks"]
        
        # Determine feasibility status
        if yield_category == "very_low":
            feasibility = "Sangat Rendah - Target di bawah standar"
            feasibility_color = "red"
        elif yield_category == "low":
            feasibility = "Rendah - Dapat dicapai dengan input minimal"
            feasibility_color = "orange"
        elif yield_category == "average":
            feasibility = "Realistis - Target standar petani"
            feasibility_color = "green"
        elif yield_category == "high":
            feasibility = "Tinggi - Memerlukan manajemen intensif"
            feasibility_color = "blue"
        else:  # record
            feasibility = "Sangat Tinggi - Target ambisius, perlu teknologi canggih"
            feasibility_color = "purple"
        
        # Get NPK recommendations
        npk = YieldBenchmarks.get_npk_for_yield(commodity, target_yield)
        
        # Get variety recommendations
        varieties = YieldBenchmarks.get_variety_recommendations(commodity, target_yield)
        
        # Convert NPK to fertilizer products
        fertilizers = MLService._convert_npk_to_fertilizers(npk['N'], npk['P'], npk['K'])
        
        # Calculate costs (estimated)
        costs = MLService._calculate_input_costs(fertilizers, commodity, target_yield)
        
        # Generate timeline
        timeline = MLService._generate_cultivation_timeline(commodity, commodity_data['growth_duration'])
        
        # Build comprehensive plan
        plan = {
            "commodity_name": commodity_data["name"],
            "commodity_icon": commodity_data["icon"],
            "target_yield": target_yield,
            "yield_unit": commodity_data["unit"],
            "feasibility": {
                "status": feasibility,
                "color": feasibility_color,
                "category": yield_category,
                "benchmark_range": {
                    "low": f"{benchmarks['low']['min']}-{benchmarks['low']['max']} {commodity_data['unit']}",
                    "average": f"{benchmarks['average']['min']}-{benchmarks['average']['max']} {commodity_data['unit']}",
                    "high": f"{benchmarks['high']['min']}-{benchmarks['high']['max']} {commodity_data['unit']}",
                    "record": f"{benchmarks['record']['min']}-{benchmarks['record']['max']} {commodity_data['unit']}"
                }
            },
            "npk_requirements": {
                "Nitrogen (N)": f"{npk['N']} kg/ha",
                "Phosphorus (P)": f"{npk['P']} kg/ha",
                "Potassium (K)": f"{npk['K']} kg/ha"
            },
            "fertilizer_products": fertilizers,
            "environmental_conditions": {
                "Suhu Optimal": f"{commodity_data['optimal_conditions']['temperature']['min']}-{commodity_data['optimal_conditions']['temperature']['max']} °C",
                "Curah Hujan": f"{commodity_data['optimal_conditions']['rainfall']['min']}-{commodity_data['optimal_conditions']['rainfall']['max']} {commodity_data['optimal_conditions']['rainfall']['unit']}",
                "pH Tanah": f"{commodity_data['optimal_conditions']['ph']['min']}-{commodity_data['optimal_conditions']['ph']['max']}",
                "Ketinggian": f"{commodity_data['optimal_conditions']['altitude']['min']}-{commodity_data['optimal_conditions']['altitude']['max']} {commodity_data['optimal_conditions']['altitude']['unit']}"
            },
            "recommended_varieties": varieties,
            "critical_factors": commodity_data["critical_factors"],
            "cost_estimate": costs,
            "cultivation_timeline": timeline,
            "growth_duration": f"{commodity_data['growth_duration']} hari"
        }
        
        return plan
    
    @staticmethod
    def _convert_npk_to_fertilizers(n_kg, p_kg, k_kg):
        """Convert NPK kg/ha to actual fertilizer products."""
        fertilizers = {}
        
        # Urea for Nitrogen (46% N)
        if n_kg > 0:
            urea_kg = round(n_kg / 0.46, 2)
            fertilizers["Urea (46% N)"] = f"{urea_kg} kg/ha"
        
        # SP-36 for Phosphorus (36% P2O5 = ~15.8% P)
        if p_kg > 0:
            sp36_kg = round(p_kg / 0.158, 2)
            fertilizers["SP-36 (36% P2O5)"] = f"{sp36_kg} kg/ha"
        
        # KCl for Potassium (60% K2O = ~50% K)
        if k_kg > 0:
            kcl_kg = round(k_kg / 0.50, 2)
            fertilizers["KCl (60% K2O)"] = f"{kcl_kg} kg/ha"
        
        # Add organic fertilizer recommendation
        fertilizers["Pupuk Kandang/Kompos"] = "2-5 ton/ha (aplikasi dasar)"
        
        return fertilizers
    
    @staticmethod
    def _calculate_input_costs(fertilizers, commodity, target_yield):
        """Calculate estimated input costs."""
        # Estimated prices (Rp/kg) - can be updated with real market data
        prices = {
            "Urea": 2500,
            "SP-36": 3000,
            "KCl": 4500,
            "Pupuk Kandang": 500,
            "Benih": 50000  # per kg or unit
        }
        
        total_fertilizer_cost = 0
        breakdown = {}
        
        for fert_name, amount_str in fertilizers.items():
            if "Pupuk Kandang" in fert_name or "Kompos" in fert_name:
                # Extract ton amount
                avg_ton = 3.5  # average of 2-5 ton
                cost = avg_ton * 1000 * prices["Pupuk Kandang"]
                breakdown[fert_name] = f"Rp {cost:,.0f}"
                total_fertilizer_cost += cost
            else:
                # Extract kg amount
                try:
                    kg = float(amount_str.split()[0])
                    fert_type = fert_name.split()[0]
                    if fert_type in prices:
                        cost = kg * prices[fert_type]
                        breakdown[fert_name] = f"Rp {cost:,.0f}"
                        total_fertilizer_cost += cost
                except:
                    pass
        
        # Estimate seed cost (varies by commodity)
        seed_costs = {
            "padi": 100000,
            "jagung": 500000,
            "kedelai": 200000,
            "cabai": 2000000,
            "tomat": 1500000
        }
        seed_cost = seed_costs.get(commodity, 300000)
        
        # Estimate labor and other costs
        labor_cost = 3000000  # Rp 3 juta for land prep, planting, maintenance
        pesticide_cost = 1500000  # Rp 1.5 juta
        
        total_cost = total_fertilizer_cost + seed_cost + labor_cost + pesticide_cost
        
        # Estimate revenue (very rough, needs market price data)
        price_per_ton = {
            "padi": 5000000,
            "jagung": 4000000,
            "kedelai": 8000000,
            "cabai": 15000000,
            "tomat": 8000000
        }
        commodity_price = price_per_ton.get(commodity, 5000000)
        estimated_revenue = target_yield * commodity_price
        estimated_profit = estimated_revenue - total_cost
        
        return {
            "fertilizer_breakdown": breakdown,
            "total_fertilizer": f"Rp {total_fertilizer_cost:,.0f}",
            "seed_cost": f"Rp {seed_cost:,.0f}",
            "labor_cost": f"Rp {labor_cost:,.0f}",
            "pesticide_cost": f"Rp {pesticide_cost:,.0f}",
            "total_input_cost": f"Rp {total_cost:,.0f}",
            "estimated_revenue": f"Rp {estimated_revenue:,.0f}",
            "estimated_profit": f"Rp {estimated_profit:,.0f}",
            "note": "Estimasi kasar, sesuaikan dengan harga lokal"
        }
    
    @staticmethod
    def _generate_cultivation_timeline(commodity, growth_duration):
        """Generate week-by-week cultivation timeline."""
        timeline = []
        
        # Generic timeline structure
        phases = [
            {
                "phase": "Persiapan Lahan",
                "weeks": "2 minggu sebelum tanam",
                "activities": [
                    "Pembajakan dan penggemburan tanah",
                    "Aplikasi pupuk kandang/kompos",
                    "Pengapuran jika pH rendah",
                    "Pembuatan bedengan (jika perlu)"
                ]
            },
            {
                "phase": "Penanaman",
                "weeks": "Minggu 0",
                "activities": [
                    "Penanaman benih/bibit berkualitas",
                    "Aplikasi pupuk dasar (P dan K)",
                    "Penyiraman awal"
                ]
            },
            {
                "phase": "Vegetatif Awal",
                "weeks": "Minggu 1-3",
                "activities": [
                    "Penyulaman tanaman mati",
                    "Penyiangan gulma",
                    "Aplikasi pupuk N pertama",
                    "Monitoring hama/penyakit"
                ]
            },
            {
                "phase": "Vegetatif Lanjut",
                "weeks": f"Minggu 4-{growth_duration//14}",
                "activities": [
                    "Aplikasi pupuk N susulan",
                    "Pengendalian hama/penyakit",
                    "Pengairan teratur",
                    "Pewiwilan (untuk tanaman tertentu)"
                ]
            },
            {
                "phase": "Generatif",
                "weeks": f"Minggu {growth_duration//14 + 1}-{growth_duration//7}",
                "activities": [
                    "Aplikasi pupuk K tinggi",
                    "Pengurangan N",
                    "Monitoring pembungaan/pembuahan",
                    "Pengendalian hama buah/bulir"
                ]
            },
            {
                "phase": "Pematangan & Panen",
                "weeks": f"Minggu {growth_duration//7 + 1}-{growth_duration//7 + 2}",
                "activities": [
                    "Pengurangan pengairan",
                    "Monitoring kematangan",
                    "Persiapan alat panen",
                    "Panen tepat waktu"
                ]
            }
        ]
        
        return phases


    @staticmethod
    def predict_success(data):
        """Predict farming success probability."""
        success_model = ModelLoader.get_model('success_model')
        if success_model is None:
            current_app.logger.warning("⚠️ Success prediction model not available, using fallback")
            # Fallback: heuristic based on optimal ranges
            ph = float(data.get('ph', 7.0))
            rainfall = float(data.get('rainfall', 0))
            temp = float(data.get('temperature', 25))
            
            # Score based on optimal conditions
            score = 0
            if 6.0 <= ph <= 7.5: score += 30
            if 500 <= rainfall <= 1500: score += 30
            if 20 <= temp <= 30: score += 40
            
            status = "Berhasil" if score >= 60 else "Berisiko Tinggi"
            return {'status': status, 'probability_of_success': score}
        
        features = [
            float(data.get('nitrogen', 0)),
            float(data.get('phosphorus', 0)),
            float(data.get('potassium', 0)),
            float(data.get('temperature', 0)),
            float(data.get('rainfall', 0)),
            float(data.get('ph', 0))
        ]
        input_data = np.array([features])
        
        prediction = success_model.predict(input_data)[0]
        probability = success_model.predict_proba(input_data)[0]
        
        status = "Berhasil" if prediction == 1 else "Berisiko Tinggi"
        prob_percent = round(probability[1] * 100, 2)
        
        return {
            'status': status,
            'probability_of_success': prob_percent
        }

