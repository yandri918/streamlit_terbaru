"""Recommendation service for fertilizer and crop recommendations."""
import numpy as np
from app.ml_models.model_loader import ModelLoader
from app.utils.data_loader import DataLoader


class RecommendationService:
    """Service for fertilizer and crop recommendations."""
    
    @staticmethod
    def get_fertilizer_recommendation(data):
        """Get fertilizer recommendation based on soil and crop data."""
        ph_tanah = float(data['ph_tanah'])
        skor_bwd = float(data.get('skor_bwd', 50))
        kelembaban_tanah = float(data.get('kelembaban_tanah', 60))
        umur_tanaman_hari = int(data.get('umur_tanaman_hari', 30))
        
        # pH-based recommendations
        if ph_tanah < 6.0:
            rekomendasi_utama = "Prioritaskan aplikasi Dolomit untuk menaikkan pH."
            peringatan = ["Peringatan: Ketersediaan Fosfor (P) sangat rendah pada pH asam."]
        elif ph_tanah > 7.2:
            rekomendasi_utama = "Pertimbangkan aplikasi Belerang (Sulfur) untuk menurunkan pH."
            peringatan = ["Peringatan: Ketersediaan unsur mikro (Besi, Mangan, Seng) rendah pada pH basa."]
        else:
            rekomendasi_utama = "Kondisi pH tanah optimal. Lanjutkan dengan pemupukan berikut:"
            peringatan = []
        
        # Try to use ML model
        try:
            model = ModelLoader.get_model('recommendation')
            if model is not None:
                input_df = np.array([[
                    ph_tanah,
                    skor_bwd,
                    kelembaban_tanah,
                    umur_tanaman_hari
                ]])
                
                prediksi_ml = model.predict(input_df)[0]
                
                rekomendasi_pupuk_ml = {
                    "Nitrogen (N)": f"{round(float(prediksi_ml[0]), 2)} kg/ha",
                    "Fosfor (P)": f"{round(float(prediksi_ml[1]), 2)} kg/ha",
                    "Kalium (K)": f"{round(float(prediksi_ml[2]), 2)} kg/ha"
                }
            else:
                raise RuntimeError("Model not available")
        except Exception as e:
            # Fallback to rule-based recommendation
            # Base NPK on plant age and BWD score
            if umur_tanaman_hari < 30:
                # Vegetative phase - high N
                n_dose = 120 - (skor_bwd * 0.5)  # Lower N if plant is stressed
                p_dose = 60
                k_dose = 60
            elif umur_tanaman_hari < 60:
                # Transition phase
                n_dose = 100 - (skor_bwd * 0.3)
                p_dose = 80
                k_dose = 80
            else:
                # Generative phase - high P and K
                n_dose = 80
                p_dose = 100
                k_dose = 120
            
            # Adjust for pH
            if ph_tanah < 6.0:
                p_dose *= 1.2  # Increase P for acidic soil
            elif ph_tanah > 7.2:
                n_dose *= 0.9  # Reduce N for alkaline soil
            
            rekomendasi_pupuk_ml = {
                "Nitrogen (N)": f"{round(n_dose, 2)} kg/ha",
                "Fosfor (P)": f"{round(p_dose, 2)} kg/ha",
                "Kalium (K)": f"{round(k_dose, 2)} kg/ha"
            }
        
        # 1. Analisa BWD (Leaf Color Chart Analysis)
        if skor_bwd < 30:
            analisa_bwd = "Status: 🔴 Defisiensi Nitrogen Berat. Daun menguning signifikan. Perlu penambahan Urea segera."
        elif skor_bwd < 50:
            analisa_bwd = "Status: 🟡 Defisiensi Nitrogen Ringan. Daun hijau muda. Tambahkan pupuk N secukupnya."
        elif skor_bwd < 75:
            analisa_bwd = "Status: 🟢 Sehat/Optimal. Warna daun hijau ideal. Pertahankan pemupukan berimbang."
        else:
            analisa_bwd = "Status: 🔵 Kelebihan Nitrogen. Daun hijau pekat gelap. Kurangi dosis Urea untuk mencegah rebah."

        # 2. Analisa Kesehatan & Risiko Penyakit (Health & Disease Risk Analysis)
        analisa_kesehatan = []
        
        # Risk based on Moisture
        if kelembaban_tanah > 80:
            analisa_kesehatan.append("⚠️ Risiko Tinggi Jamur/Busuk Akar: Kelembaban tanah sangat tinggi. Waspada penyakit layu fusarium atau busuk akar.")
        elif kelembaban_tanah < 40:
             analisa_kesehatan.append("⚠️ Stres Kekeringan: Kelembaban rendah menghambat penyerapan nutrisi. Lakukan penyiraman segera.")

        # Risk based on pH
        if ph_tanah < 5.5:
             analisa_kesehatan.append("⚠️ Risiko Penyakit Akar: pH masam memicu perkembangan jamur patogen tertentu dan menghambat penyerapan P.")
        
        # Combined Risk
        if skor_bwd < 40 and kelembaban_tanah > 70:
             analisa_kesehatan.append("🚨 Indikasi Klorosis/Penyakit: Daun kuning + tanah basah bisa mengindikasikan serangan virus atau gangguan akar, bukan hanya kurang pupuk.")

        if not analisa_kesehatan:
            analisa_kesehatan.append("✅ Kondisi Lingkungan Kondusif: Parameter tanah dan tanaman mendukung pertumbuhan sehat.")

        return {
            "rekomendasi_utama": rekomendasi_utama,
            "rekomendasi_pupuk_ml": rekomendasi_pupuk_ml,
            "analisa_bwd": analisa_bwd,
            "analisa_kesehatan": analisa_kesehatan,
            "peringatan_penting": peringatan
        }
    
    @staticmethod
    def calculate_fertilizer_dosage(commodity, area_sqm, ph_tanah, soil_texture='lempung', target_yield=0, inventory=None, previous_crop='bukan_legum'):
        """Calculate fertilizer dosage for specific crop and area with precision agriculture adjustments."""
        dosage_db = DataLoader.get_fertilizer_dosage_db()
        dosage_data = dosage_db.get(commodity)
        
        if not dosage_data:
            return None
        
        area_ha = area_sqm / 10000.0
        results = {"anorganik": {}, "organik": {}, "perbaikan_tanah": {}, "schedule": {}, "adjustments": []}
        
        # --- 1. Yield Scaling Factor ---
        # Standard yields (ton/ha) reference
        standard_yields = {
            "padi": 6.0, "jagung": 8.0, "kedelai": 2.5, "cabai": 10.0, 
            "tomat": 40.0, "kentang": 20.0, "bawang_merah": 10.0,
            "melon": 25.0, "semangka": 30.0
        }
        
        yield_factor = 1.0
        if target_yield > 0:
            std_yield = standard_yields.get(commodity, 0)
            if std_yield > 0:
                # Calculate factor but clamp to safe limits (0.5x to 1.5x) to prevent overdosing
                raw_factor = target_yield / std_yield
                yield_factor = max(0.5, min(raw_factor, 1.5))
                
                if yield_factor != 1.0:
                    results["adjustments"].append(f"Dosis disesuaikan {int(yield_factor*100)}% untuk target panen {target_yield} ton/ha")

        # --- 2. Previous Crop Credit (Nitrogen) ---
        n_credit_kg_ha = 0
        if previous_crop == 'legum': # Kacang-kacangan
            n_credit_kg_ha = 20 # Credit 20 kg N/ha ~ 45 kg Urea
            results["adjustments"].append("Pengurangan dosis Urea/N karena tanaman sebelumnya adalah Legum (Kacang-kacangan)")

        # Calculate anorganic fertilizers (Total)
        if "anorganik_kg_ha" in dosage_data:
            for fert, dose in dosage_data["anorganik_kg_ha"].items():
                # Apply Yield Factor
                adjusted_dose = dose * yield_factor
                
                # Apply Nitrogen Credit
                if "Urea" in fert or "ZA" in fert:
                    # Convert N credit to fertilizer weight (approx)
                    # Urea is 46% N, so 20 kg N = 43 kg Urea
                    fert_credit = n_credit_kg_ha * (100/46 if "Urea" in fert else 100/21)
                    adjusted_dose = max(0, adjusted_dose - fert_credit)
                
                results["anorganik"][fert] = round(adjusted_dose * area_ha, 2)
        
        # Calculate organic fertilizers
        if "organik_ton_ha" in dosage_data:
            for fert, dose in dosage_data["organik_ton_ha"].items():
                # Organic usually not scaled strictly by yield target in short term, but we scale it for maintenance
                results["organik"][fert] = round((dose * 1000) * area_ha, 2)
        
        # Calculate dolomite if pH is acidic
        if ph_tanah < 6.0:
            dose_dolomit = dosage_data.get("dolomit_ton_ha_asam", 0)
            # Adjust dolomite based on how acidic
            if ph_tanah < 5.0: dose_dolomit *= 1.5
            results["perbaikan_tanah"]["Dolomit"] = round((dose_dolomit * 1000) * area_ha, 2)
            
        # Calculate Complex Schedule (Stage-based)
        if "complex_schedule" in dosage_data:
            for stage, details in dosage_data["complex_schedule"].items():
                stage_result = {"fertilizers": {}, "notes": details.get("notes", "")}
                
                # --- 3. Soil Texture Adjustment ---
                if soil_texture == 'pasir':
                    stage_result["notes"] += " <br><strong>Tips Tanah Pasir:</strong> Bagi dosis menjadi 2x aplikasi (selang 3-4 hari) untuk mencegah pupuk hanyut."
                elif soil_texture == 'liat':
                    stage_result["notes"] += " <br><strong>Tips Tanah Liat:</strong> Tanah liat mengikat air, pastikan drainase baik sebelum memupuk."

                for key, val in details.items():
                    if key != "notes":
                        # Calculate dose based on area and yield factor
                        # Note: Schedule doses usually sum up to total. We apply yield factor here too.
                        adjusted_val = val * yield_factor
                        
                        # Apply N credit to vegetative stages mostly
                        if previous_crop == 'legum' and ("Urea" in key or "ZA" in key) and ("Vegetatif" in stage or "Awal" in stage):
                             fert_credit = n_credit_kg_ha * (100/46 if "Urea" in key else 100/21)
                             # Split credit across stages? For simplicity, apply reduction proportionally or just to total. 
                             # Here we applied to total above. For schedule, we just scale by yield. 
                             # Ideally, we should sync schedule sum with total. 
                             # Simplified: Just scale by yield factor for schedule to keep it consistent.
                             pass

                        stage_result["fertilizers"][key] = round(adjusted_val * area_ha, 2)
                results["schedule"][stage] = stage_result
        
        # --- 4. Inventory Check & Substitution ---
        if inventory:
            # Check if recommended fertilizers are in inventory
            recommended_ferts = list(results["anorganik"].keys()) # Use list to allow modification
            user_inventory = set(inventory)
            
            # SUBSTITUTION LOGIC: Singles -> NPK 15-15-15
            # If user has NPK 15-15-15 and is missing one of the singles (or just prefers NPK)
            # We try to fulfill P and K needs with NPK first, then top up with Urea/KCL
            if "NPK 15-15-15" in user_inventory:
                # Calculate total N, P, K needed from current recommendation
                n_needed = 0
                p_needed = 0
                k_needed = 0
                
                # Helper to get nutrient content
                def get_content(fert_name):
                    # Simple lookup for standard fertilizers
                    if "Urea" in fert_name: return {"N": 0.46, "P": 0, "K": 0}
                    if "SP-36" in fert_name: return {"N": 0, "P": 0.36, "K": 0}
                    if "KCl" in fert_name or "KCL" in fert_name: return {"N": 0, "P": 0, "K": 0.60}
                    if "ZA" in fert_name: return {"N": 0.21, "P": 0, "K": 0} # Ignore S for now
                    if "NPK 15-15-15" in fert_name: return {"N": 0.15, "P": 0.15, "K": 0.15}
                    return {"N": 0, "P": 0, "K": 0}

                # Calculate current nutrients provided by the recommendation
                current_recs = results["anorganik"].copy()
                for fert, amount in current_recs.items():
                    c = get_content(fert)
                    n_needed += amount * c["N"]
                    p_needed += amount * c["P"]
                    k_needed += amount * c["K"]
                
                # We want to use NPK 15-15-15 (15% N, 15% P, 15% K)
                # Determine limiting factor (usually P or K) to avoid overdose
                # Max NPK we can use is determined by the lowest requirement among P and K (ignore N as it's usually high)
                # If P needed is 36 kg, max NPK = 36 / 0.15 = 240 kg
                
                # Only substitute if we actually have P and K needs (to avoid using NPK for pure Urea needs)
                if p_needed > 0 and k_needed > 0:
                    max_npk_by_p = p_needed / 0.15
                    max_npk_by_k = k_needed / 0.15
                    
                    # Use the smaller of the two to be safe
                    npk_amount = min(max_npk_by_p, max_npk_by_k)
                    
                    # Round to reasonable number
                    npk_amount = round(npk_amount, 2)
                    
                    if npk_amount > 0:
                        # Apply NPK
                        results["anorganik"]["NPK 15-15-15"] = npk_amount
                        
                        # Subtract nutrients provided by NPK
                        n_supplied = npk_amount * 0.15
                        p_supplied = npk_amount * 0.15
                        k_supplied = npk_amount * 0.15
                        
                        n_remaining = max(0, n_needed - n_supplied)
                        p_remaining = max(0, p_needed - p_supplied)
                        k_remaining = max(0, k_needed - k_supplied)
                        
                        # Re-calculate singles needed
                        new_anorganik = {"NPK 15-15-15": npk_amount}
                        
                        # Top up N (Urea or ZA)
                        if n_remaining > 1: # Threshold to ignore small amounts
                            # Prefer Urea if available or if ZA not forced
                            if "Urea" in user_inventory or "Urea" in current_recs:
                                urea_needed = n_remaining / 0.46
                                new_anorganik["Urea"] = round(urea_needed, 2)
                            elif "ZA" in user_inventory:
                                za_needed = n_remaining / 0.21
                                new_anorganik["ZA"] = round(za_needed, 2)
                            else:
                                # Default back to Urea if nothing else
                                urea_needed = n_remaining / 0.46
                                new_anorganik["Urea"] = round(urea_needed, 2)

                        # Top up P (SP-36)
                        if p_remaining > 1:
                            sp36_needed = p_remaining / 0.36
                            new_anorganik["SP-36"] = round(sp36_needed, 2)
                            
                        # Top up K (KCL)
                        if k_remaining > 1:
                            kcl_needed = k_remaining / 0.60
                            new_anorganik["KCL"] = round(kcl_needed, 2)
                            
                        # Replace the recommendation
                        results["anorganik"] = new_anorganik
                        
                        results["adjustments"].append(f"<strong>Optimasi NPK:</strong> Formula disesuaikan menggunakan NPK 15-15-15 ({npk_amount} kg) untuk efisiensi stok.")
                        
                        # Clear schedule notes as they might be confusing now
                        # Ideally we recalculate schedule, but for now we just keep total correct
                        for stage in results["schedule"]:
                             results["schedule"][stage]["notes"] += " <br>(Sesuaikan aplikasi NPK dan tunggal secara proporsional)"


            # SUBSTITUTION LOGIC: Urea -> ZA (Only if NPK logic didn't already handle it or if NPK wasn't used)
            # Check if Urea is still in the list
            if "Urea" in results["anorganik"] and "Urea" not in user_inventory and "ZA" in user_inventory:
                urea_dose = results["anorganik"].pop("Urea")
                za_dose = urea_dose * (46 / 21)
                current_za = results["anorganik"].get("ZA", 0)
                results["anorganik"]["ZA"] = round(current_za + za_dose, 2)
                results["adjustments"].append(f"<strong>Substitusi:</strong> Urea diganti ZA ({round(za_dose, 2)} kg).")

            # Re-check missing after substitution
            recommended_ferts_final = set(results["anorganik"].keys())
            missing = recommended_ferts_final - user_inventory
            
            if missing:
                missing_str = ", ".join(missing)
                results["adjustments"].append(f"<strong>Perhatian Stok:</strong> Anda tidak memiliki {missing_str}. Pertimbangkan substitusi atau beli stok.")

        results["commodity_name"] = dosage_data['name']
        results["area_sqm"] = area_sqm
        
        return results
    
    @staticmethod
    def get_integrated_recommendation(ketinggian, iklim, fase, masalah):
        """Get integrated recommendation for bibit, pemupukan, penyemprotan."""
        
        # 1. Rekomendasi Bibit & Varietas
        bibit_db = {
            "dataran_tinggi": {
                "desc": "Varietas adaptif suhu sejuk (16-23°C).",
                "examples": ["Kentang (Granola, Atlantik)", "Wortel (Gundaling)", "Kubis (Green Nova)", "Stroberi (Sweet Charlie)"],
                "tips": "Gunakan mulsa plastik hitam perak untuk menjaga suhu tanah."
            },
            "dataran_rendah": {
                "desc": "Varietas tahan panas (>27°C) dan toleran kekeringan.",
                "examples": ["Cabai (Lado, PM 999)", "Tomat (Tymoti, Servo)", "Bawang Merah (Bima Brebes)", "Jagung (Bisi-18)"],
                "tips": "Pastikan irigasi cukup dan drainase lancar untuk mencegah genangan."
            },
            "tropis": {
                "desc": "Varietas Day-Neutral, tidak sensitif panjang hari.",
                "examples": ["Pepaya (California)", "Pisang (Cavendish)", "Padi (Inpari 32)"],
                "tips": "Waspada kelembaban tinggi yang memicu jamur."
            },
            "subtropis": {
                "desc": "Varietas yang membutuhkan vernalisasi atau periode dingin.",
                "examples": ["Anggur", "Apel (Manalagi)", "Jeruk (Keprok)"],
                "tips": "Lakukan pemangkasan rutin untuk mengatur kelembaban tajuk."
            }
        }
        
        # 2. Rekomendasi Pemupukan
        pupuk_db = {
            "vegetatif": {
                "focus": "Pertumbuhan Daun & Akar",
                "ratio": "N Tinggi, P Sedang, K Rendah",
                "recommendation": "Gunakan Urea atau NPK 25-7-7. Tambahkan pupuk kandang matang untuk memperbaiki struktur tanah.",
                "foliar": "Semprot pupuk daun tinggi Nitrogen (misal: Gandasil D) setiap 7-10 hari."
            },
            "generatif": {
                "focus": "Pembungaan & Pembuahan",
                "ratio": "N Rendah, P Tinggi, K Tinggi",
                "recommendation": "Gunakan NPK 16-16-16 atau MKP (Mono Kalium Phosphate). Kurangi Urea untuk mencegah rontok bunga.",
                "foliar": "Semprot pupuk daun tinggi Kalium (misal: Gandasil B) dan Kalsium untuk memperkuat buah."
            }
        }
        
        # 3. Rekomendasi Pengendalian Masalah (Integrated Pest Management)
        pest_strategy = None
        if masalah and masalah != 'none':
            # Try to get detailed strategy from existing method
            pest_details = RecommendationService.get_spraying_recommendation(masalah)
            if pest_details:
                pest_strategy = pest_details
            else:
                # Fallback for simple problems
                pest_strategy = {
                    "strategy": {
                        "name": f"Penanganan {masalah.replace('_', ' ').title()}",
                        "description": "Lakukan sanitasi lahan dan monitoring rutin.",
                        "cycles": []
                    },
                    "protocol": {
                        "title": "Protokol Umum",
                        "steps": ["Bersihkan gulma inang", "Gunakan pestisida nabati sebagai pencegahan"]
                    }
                }

        # Construct Response
        bibit_info = bibit_db.get(ketinggian, bibit_db.get("dataran_rendah"))
        pupuk_info = pupuk_db.get(fase, pupuk_db.get("vegetatif"))
        
        return {
            "bibit": {
                "kriteria": bibit_info["desc"],
                "rekomendasi": bibit_info["examples"],
                "tips": bibit_info["tips"]
            },
            "pemupukan": {
                "fase": pupuk_info["focus"],
                "rasio_npk": pupuk_info["ratio"],
                "aplikasi_tanah": pupuk_info["recommendation"],
                "aplikasi_daun": pupuk_info["foliar"]
            },
            "pengendalian": pest_strategy
        }
    
    @staticmethod
    def get_spraying_recommendation(pest):
        """Get spraying strategy recommendation."""
        strategy_db = {
            "thrips": {
                "name": "Strategi Pengendalian Thrips",
                "description": "Siklus rotasi 9 minggu untuk mencegah resistensi.",
                "cycles": [
                    {
                        "weeks": "Minggu 1-3",
                        "level": "Level 1: Kontak & Translaminar",
                        "active_ingredient": "Abamektin",
                        "irac_code": "Grup 6",
                        "sop": "Aplikasikan setiap 5-7 hari sekali."
                    },
                    {
                        "weeks": "Minggu 4-6",
                        "level": "Level 2: Sistemik Lokal",
                        "active_ingredient": "Spinetoram atau Spinosad",
                        "irac_code": "Grup 5",
                        "sop": "Aplikasikan setiap 5-7 hari sekali."
                    },
                    {
                        "weeks": "Minggu 7-9",
                        "level": "Level 3: Sistemik Penuh",
                        "active_ingredient": "Imidakloprid atau Tiametoksam",
                        "irac_code": "Grup 4A",
                        "sop": "Aplikasikan setiap 7-10 hari sekali."
                    }
                ]
            },
            "ulat_grayak": {
                "name": "Strategi Pengendalian Ulat Grayak (Spodoptera litura)",
                "description": "Program rotasi insektisida untuk mencegah resistensi ulat pemakan daun.",
                "cycles": [
                    {
                        "weeks": "Minggu 1-2",
                        "level": "Level 1: Bioinsektisida",
                        "active_ingredient": "Bacillus thuringiensis (Bt)",
                        "irac_code": "Grup 11A",
                        "sop": "Semprot saat ulat masih instar 1-2 (kecil). Aplikasi sore hari untuk efektivitas maksimal."
                    },
                    {
                        "weeks": "Minggu 3-4",
                        "level": "Level 2: Insektisida Kontak",
                        "active_ingredient": "Klorfenapir atau Indoksakarb",
                        "irac_code": "Grup 13 atau 22A",
                        "sop": "Semprot merata ke seluruh permukaan daun. Interval 5-7 hari."
                    },
                    {
                        "weeks": "Minggu 5-6",
                        "level": "Level 3: Sistemik",
                        "active_ingredient": "Emamektin Benzoat",
                        "irac_code": "Grup 6",
                        "sop": "Aplikasi sistemik untuk perlindungan jangka panjang. Interval 7-10 hari."
                    }
                ]
            },
            "ulat_tanah": {
                "name": "Strategi Pengendalian Ulat Tanah (Agrotis sp.)",
                "description": "Pengendalian ulat yang menyerang pangkal batang dan akar tanaman muda.",
                "cycles": [
                    {
                        "weeks": "Minggu 1-2",
                        "level": "Level 1: Pencegahan Awal",
                        "active_ingredient": "Karbofuran Granul (aplikasi tanah)",
                        "irac_code": "Grup 1A",
                        "sop": "Aplikasikan granul di sekitar pangkal batang saat tanam. Dosis 10-15 kg/ha."
                    },
                    {
                        "weeks": "Minggu 3-4",
                        "level": "Level 2: Penyiraman Insektisida",
                        "active_ingredient": "Klorpirifos atau Profenofos",
                        "irac_code": "Grup 1B",
                        "sop": "Siramkan larutan insektisida ke pangkal batang. Aplikasi sore hari."
                    },
                    {
                        "weeks": "Minggu 5-6",
                        "level": "Level 3: Kombinasi",
                        "active_ingredient": "Fipronil + Imidakloprid",
                        "irac_code": "Grup 2A + 4A",
                        "sop": "Kombinasi sistemik untuk perlindungan total. Interval 10-14 hari."
                    }
                ]
            },
            "penggerek_batang": {
                "name": "Strategi Pengendalian Penggerek Batang",
                "description": "Pengendalian hama penggerek yang menyerang batang padi, jagung, dan tebu.",
                "cycles": [
                    {
                        "weeks": "Minggu 1-3",
                        "level": "Level 1: Preventif Biologis",
                        "active_ingredient": "Beauveria bassiana atau Metarhizium anisopliae",
                        "irac_code": "Bioinsektisida",
                        "sop": "Aplikasi preventif sejak fase vegetatif awal. Semprot batang dan daun."
                    },
                    {
                        "weeks": "Minggu 4-6",
                        "level": "Level 2: Sistemik Granul",
                        "active_ingredient": "Karbofuran atau Karbosulfan Granul",
                        "irac_code": "Grup 1A",
                        "sop": "Aplikasi granul ke pucuk tanaman (untuk padi) atau pangkal batang."
                    },
                    {
                        "weeks": "Minggu 7-9",
                        "level": "Level 3: Insektisida Sistemik",
                        "active_ingredient": "Fipronil atau Klorantraniliprol",
                        "irac_code": "Grup 2A atau 28",
                        "sop": "Semprot atau siram untuk perlindungan sistemik. Interval 10-14 hari."
                    }
                ]
            },
            "antraknosa": {
                "name": "Strategi Pengendalian Antraknosa (Colletotrichum sp.)",
                "description": "Program rotasi fungisida untuk mengendalikan penyakit antraknosa pada cabai dan buah.",
                "cycles": [
                    {
                        "weeks": "Minggu 1-3",
                        "level": "Level 1: Fungisida Kontak",
                        "active_ingredient": "Mankozeb atau Propineb",
                        "irac_code": "FRAC M3",
                        "sop": "Aplikasi preventif setiap 5-7 hari. Semprot merata ke daun dan buah."
                    },
                    {
                        "weeks": "Minggu 4-6",
                        "level": "Level 2: Fungisida Sistemik",
                        "active_ingredient": "Azoksistrobin atau Difenokonazol",
                        "irac_code": "FRAC 11 atau 3",
                        "sop": "Aplikasi kuratif saat gejala muncul. Interval 7-10 hari."
                    },
                    {
                        "weeks": "Minggu 7-9",
                        "level": "Level 3: Kombinasi",
                        "active_ingredient": "Mankozeb + Metalaksil atau Propineb + Heksakonazol",
                        "irac_code": "FRAC M3 + 4 atau M3 + 3",
                        "sop": "Kombinasi kontak dan sistemik untuk perlindungan maksimal."
                    }
                ]
            },
            "blas": {
                "name": "Strategi Pengendalian Blas Padi (Pyricularia oryzae)",
                "description": "Program pengendalian penyakit blas pada tanaman padi.",
                "cycles": [
                    {
                        "weeks": "Minggu 1-3 (Fase Vegetatif)",
                        "level": "Level 1: Preventif",
                        "active_ingredient": "Trisiklazol atau Isoprotiolan",
                        "irac_code": "FRAC I1 atau I2",
                        "sop": "Aplikasi preventif saat tanaman umur 21-30 HST. Interval 7-10 hari."
                    },
                    {
                        "weeks": "Minggu 4-6 (Fase Generatif Awal)",
                        "level": "Level 2: Kuratif",
                        "active_ingredient": "Tebukonazol atau Propikonazol",
                        "irac_code": "FRAC 3",
                        "sop": "Aplikasi saat gejala awal muncul. Semprot merata ke daun dan malai."
                    },
                    {
                        "weeks": "Minggu 7-9 (Fase Pengisian Bulir)",
                        "level": "Level 3: Proteksi Malai",
                        "active_ingredient": "Azoksistrobin + Difenokonazol",
                        "irac_code": "FRAC 11 + 3",
                        "sop": "Kombinasi untuk melindungi malai. Aplikasi 1-2 kali saat pembungaan."
                    }
                ]
            },
            "busuk_daun": {
                "name": "Strategi Pengendalian Busuk Daun (Phytophthora sp.)",
                "description": "Pengendalian penyakit busuk daun yang disebabkan oleh jamur air (oomycetes).",
                "cycles": [
                    {
                        "weeks": "Minggu 1-3",
                        "level": "Level 1: Preventif Kontak",
                        "active_ingredient": "Mankozeb atau Klorotalonil",
                        "irac_code": "FRAC M3 atau M5",
                        "sop": "Aplikasi preventif sebelum musim hujan. Interval 5-7 hari."
                    },
                    {
                        "weeks": "Minggu 4-6",
                        "level": "Level 2: Sistemik Spesifik",
                        "active_ingredient": "Metalaksil atau Dimetomorf",
                        "irac_code": "FRAC 4 atau 40",
                        "sop": "Fungisida spesifik anti-oomycetes. Aplikasi saat gejala muncul."
                    },
                    {
                        "weeks": "Minggu 7-9",
                        "level": "Level 3: Kombinasi Kuat",
                        "active_ingredient": "Metalaksil + Mankozeb atau Dimetomorf + Ametoctradin",
                        "irac_code": "FRAC 4 + M3 atau 40 + 45",
                        "sop": "Kombinasi untuk pengendalian maksimal. Interval 7-10 hari."
                    }
                ]
            },
            "lalat_buah": {
                "name": "Strategi Pengendalian Lalat Buah (Bactrocera sp.)",
                "description": "Program terpadu pengendalian lalat buah pada tanaman hortikultura.",
                "cycles": [
                    {
                        "weeks": "Minggu 1-4",
                        "level": "Level 1: Perangkap Massal",
                        "active_ingredient": "Metil Eugenol + Insektisida (perangkap)",
                        "irac_code": "Non-kimia + Grup 1A",
                        "sop": "Pasang perangkap petrogenol 20-40 unit/ha. Ganti umpan setiap 2 minggu."
                    },
                    {
                        "weeks": "Minggu 5-8",
                        "level": "Level 2: Pembungkusan Buah",
                        "active_ingredient": "Pembungkusan fisik + Penyemprotan spot",
                        "irac_code": "Non-kimia",
                        "sop": "Bungkus buah muda dengan kantong kertas/plastik. Semprot spot jika diperlukan."
                    },
                    {
                        "weeks": "Minggu 9-12",
                        "level": "Level 3: Protein Bait",
                        "active_ingredient": "Protein Hidrolisat + Spinosad",
                        "irac_code": "Grup 5",
                        "sop": "Semprot umpan protein ke tajuk pohon. Aplikasi spot, bukan total."
                    }
                ]
            },
            "kutu_daun": {
                "name": "Strategi Pengendalian Kutu Daun (Aphids)",
                "description": "Pengendalian kutu daun yang menjadi vektor virus pada tanaman.",
                "cycles": [
                    {
                        "weeks": "Minggu 1-3",
                        "level": "Level 1: Insektisida Nabati",
                        "active_ingredient": "Ekstrak Nimba atau Minyak Nabati",
                        "irac_code": "Bioinsektisida",
                        "sop": "Semprot dengan surfaktan. Aplikasi setiap 3-5 hari untuk populasi rendah."
                    },
                    {
                        "weeks": "Minggu 4-6",
                        "level": "Level 2: Sistemik Cepat",
                        "active_ingredient": "Imidakloprid atau Asetamiprid",
                        "irac_code": "Grup 4A",
                        "sop": "Aplikasi sistemik via semprot atau siram. Interval 7-10 hari."
                    },
                    {
                        "weeks": "Minggu 7-9",
                        "level": "Level 3: Alternatif MOA",
                        "active_ingredient": "Flonikamid atau Pimetrozin",
                        "irac_code": "Grup 9B atau 9C",
                        "sop": "Insektisida dengan mode aksi berbeda. Interval 7-10 hari."
                    }
                ]
            }
        }
        
        protocol = {
            "title": "Protokol Penyemprotan Profesional",
            "steps": [
                "Waktu: Pagi (sebelum 09:00) atau sore (setelah 15:00)",
                "Urutan: Air → pH adjuster → Pestisida → Perekat",
                "Gunakan perekat & perata untuk efektivitas maksimal",
                "Kalibrasi alat semprot untuk kabut halus dan merata",
                "Rotasi bahan aktif sesuai grup IRAC/FRAC untuk mencegah resistensi",
                "Perhatikan masa tunggu (harvest interval) sebelum panen"
            ]
        }
        
        strategy = strategy_db.get(pest)
        if not strategy:
            return None
        
        return {"strategy": strategy, "protocol": protocol}
