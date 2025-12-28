"""
Service module for Evidence-Based Jamu Calculator
Based on B2P2TOOT Saintifikasi Jamu research and clinical trials
"""

# ===== VALIDATED JAMU FORMULAS (from Clinical Trials) =====
JAMU_FORMULAS = {
    "Antidiabetes (Hiperglikemia)": {
        "ingredients": {
            "Daun Salam (Syzygium polyanthum)": 5,  # grams
            "Sambiloto (Andrographis paniculata)": 5,
            "Kayu Manis (Cinnamomum burmani)": 7,
            "Temulawak (Curcuma xanthorrhiza)": 10
        },
        "preparation": "Rebus dengan 600 ml air hingga tersisa 300 ml",
        "dosage": "150 ml, 2x sehari (pagi dan sore)",
        "duration": "Konsumsi rutin minimal 4 minggu",
        "clinical_evidence": "Setara dengan metformin dalam menurunkan glukosa darah (RCT Phase I)",
        "contraindications": ["Kehamilan", "Menyusui", "Hipoglikemia", "Gangguan hati berat"],
        "side_effects": "Dapat meningkatkan enzim transaminase pada beberapa pasien",
        "research_ref": "B2P2TOOT Clinical Trial - Antihyperglycemic Jamu Formula"
    },
    
    "Penurun Kolesterol": {
        "ingredients": {
            "Temulawak (Curcuma xanthorrhiza)": 15,
            "Kunyit (Curcuma longa)": 10,
            "Jahe Merah (Zingiber officinale)": 8,
            "Daun Salam (Syzygium polyanthum)": 5,
            "Seledri (Apium graveolens)": 5,
            "Bawang Putih (Allium sativum)": 3,
            "Daun Jati Belanda (Guazuma ulmifolia)": 5
        },
        "preparation": "Rebus dengan 800 ml air hingga tersisa 400 ml",
        "dosage": "200 ml, 2x sehari selama 28 hari",
        "duration": "Minimal 4 minggu, evaluasi setelah 8 minggu",
        "clinical_evidence": "Aman, tidak mengubah fungsi hati/ginjal secara signifikan",
        "contraindications": ["Kehamilan", "Menyusui", "Gangguan pembekuan darah"],
        "side_effects": "Peningkatan frekuensi BAB ringan (masih normal), nyeri perut ringan",
        "research_ref": "B2P2TOOT Clinical Trial - Cholesterol-Lowering Jamu"
    },
    
    "Hepatoprotektif (Pelindung Hati)": {
        "ingredients": {
            "Kunyit (Curcuma longa)": 15,
            "Temulawak (Curcuma xanthorrhiza)": 15,
            "Daun Jombang (Taraxacum officinale)": 10
        },
        "preparation": "Rebus dengan 600 ml air hingga tersisa 300 ml",
        "dosage": "150 ml, 2x sehari",
        "duration": "Minimal 4 minggu",
        "clinical_evidence": "Terbukti melindungi fungsi hati (Saintifikasi Jamu)",
        "contraindications": ["Kehamilan", "Obstruksi saluran empedu"],
        "side_effects": "Minimal, dapat menyebabkan mual ringan pada awal konsumsi",
        "research_ref": "B2P2TOOT Saintifikasi Jamu - Hepatoprotective Formula"
    },
    
    "Peningkat Imunitas": {
        "ingredients": {
            "Temulawak (Curcuma xanthorrhiza)": 12,
            "Kunyit (Curcuma longa)": 10,
            "Jahe Merah (Zingiber officinale)": 10,
            "Kencur (Kaempferia galanga)": 8,
            "Serai (Cymbopogon citratus)": 5,
            "Daun Sirsak (Annona muricata)": 5
        },
        "preparation": "Rebus dengan 800 ml air hingga tersisa 400 ml",
        "dosage": "200 ml, 1-2x sehari",
        "duration": "Konsumsi rutin, terutama saat musim pancaroba",
        "clinical_evidence": "Meningkatkan sistem imun (penelitian fitokimia)",
        "contraindications": ["Kehamilan trimester 1", "Alergi terhadap komponen"],
        "side_effects": "Minimal, aman untuk konsumsi jangka panjang",
        "research_ref": "Traditional use + Phytochemical studies"
    },
    
    "Penurun Asam Urat": {
        "ingredients": {
            "Daun Salam (Syzygium polyanthum)": 10,
            "Seledri (Apium graveolens)": 8,
            "Daun Sirsak (Annona muricata)": 7,
            "Temulawak (Curcuma xanthorrhiza)": 10
        },
        "preparation": "Rebus dengan 600 ml air hingga tersisa 300 ml",
        "dosage": "200 ml, 1x sehari",
        "duration": "Minimal 4 minggu",
        "clinical_evidence": "Terbukti menurunkan kadar asam urat (penelitian klinis)",
        "contraindications": ["Kehamilan", "Menyusui", "Gangguan ginjal berat"],
        "side_effects": "Minimal, dapat meningkatkan frekuensi buang air kecil",
        "research_ref": "Clinical study on uric acid reduction"
    },
    
    "Beras Kencur (Stamina & Nafsu Makan)": {
        "ingredients": {
            "Kencur (Kaempferia galanga)": 15,
            "Beras (Oryza sativa)": 50,
            "Jahe (Zingiber officinale)": 10,
            "Asam Jawa (Tamarindus indica)": 10,
            "Gula Aren": 50
        },
        "preparation": "Rendam beras 2 jam, haluskan dengan kencur dan jahe, rebus dengan 800 ml air",
        "dosage": "200 ml, 1-2x sehari",
        "duration": "Konsumsi sesuai kebutuhan",
        "clinical_evidence": "Tradisional, terbukti meningkatkan stamina dan nafsu makan",
        "contraindications": ["Diabetes (karena gula)", "Obesitas"],
        "side_effects": "Minimal, perhatikan kandungan gula",
        "research_ref": "Traditional Indonesian Medicine"
    },
    
    "Kunyit Asam (Kesehatan Wanita)": {
        "ingredients": {
            "Kunyit (Curcuma longa)": 20,
            "Asam Jawa (Tamarindus indica)": 15,
            "Gula Aren": 30
        },
        "preparation": "Parut kunyit, rebus dengan 600 ml air, tambahkan asam jawa",
        "dosage": "200 ml, 1-2x sehari",
        "duration": "Konsumsi rutin, terutama saat menstruasi",
        "clinical_evidence": "Tradisional, anti-inflamasi untuk nyeri haid",
        "contraindications": ["Kehamilan", "Gangguan pembekuan darah", "Obstruksi empedu"],
        "side_effects": "Minimal, dapat menyebabkan mual jika berlebihan",
        "research_ref": "Traditional use + Curcumin anti-inflammatory studies"
    },
    
    "Hipertensi (Penurun Tekanan Darah)": {
        "ingredients": {
            "Daun Salam (Syzygium polyanthum)": 10,
            "Seledri (Apium graveolens)": 10,
            "Bawang Putih (Allium sativum)": 5,
            "Mengkudu (Morinda citrifolia)": 50,
            "Daun Sirsak (Annona muricata)": 7
        },
        "preparation": "Rebus dengan 800 ml air hingga tersisa 400 ml",
        "dosage": "200 ml, 2x sehari",
        "duration": "Minimal 4 minggu, monitor tekanan darah",
        "clinical_evidence": "Saintifikasi Jamu - terbukti menurunkan tekanan darah",
        "contraindications": ["Hipotensi", "Kehamilan", "Gangguan ginjal"],
        "side_effects": "Dapat menyebabkan penurunan tekanan darah berlebihan jika dikombinasi dengan obat",
        "research_ref": "B2P2TOOT Saintifikasi Jamu - Hypertension Formula"
    },
    
    "Maag & Asam Lambung": {
        "ingredients": {
            "Kunyit (Curcuma longa)": 15,
            "Temulawak (Curcuma xanthorrhiza)": 12,
            "Jahe (Zingiber officinale)": 8,
            "Daun Sembung (Blumea balsamifera)": 7
        },
        "preparation": "Rebus dengan 600 ml air hingga tersisa 300 ml",
        "dosage": "150 ml, 2x sehari sebelum makan",
        "duration": "2-4 minggu",
        "clinical_evidence": "Kurkumin terbukti melindungi mukosa lambung",
        "contraindications": ["Obstruksi saluran cerna", "Alergi"],
        "side_effects": "Minimal",
        "research_ref": "Curcumin gastroprotective studies"
    },
    
    "Batuk & Flu": {
        "ingredients": {
            "Jahe Merah (Zingiber officinale)": 15,
            "Kencur (Kaempferia galanga)": 10,
            "Jeruk Nipis (Citrus aurantifolia)": 2,  # buah
            "Madu": 30,  # ml
            "Daun Mint (Mentha)": 5
        },
        "preparation": "Rebus jahe dan kencur dengan 500 ml air, tambahkan jeruk nipis dan madu setelah dingin",
        "dosage": "100-150 ml, 3x sehari",
        "duration": "Hingga gejala membaik (3-7 hari)",
        "clinical_evidence": "Gingerol dan ethyl p-methoxycinnamate sebagai ekspektoran",
        "contraindications": ["Diabetes (perhatikan madu)", "Alergi madu"],
        "side_effects": "Minimal",
        "research_ref": "Ginger and Kencur as expectorant - traditional + modern studies"
    },
    
    "Rematik & Nyeri Sendi": {
        "ingredients": {
            "Jahe Merah (Zingiber officinale)": 15,
            "Kunyit (Curcuma longa)": 15,
            "Temulawak (Curcuma xanthorrhiza)": 12,
            "Sambiloto (Andrographis paniculata)": 5,
            "Daun Salam (Syzygium polyanthum)": 7
        },
        "preparation": "Rebus dengan 800 ml air hingga tersisa 400 ml",
        "dosage": "200 ml, 2x sehari",
        "duration": "Minimal 4 minggu",
        "clinical_evidence": "Gingerol dan curcumin sebagai anti-inflamasi (setara ibuprofen)",
        "contraindications": ["Kehamilan", "Gangguan pembekuan darah", "Tukak lambung"],
        "side_effects": "Dapat menyebabkan iritasi lambung jika berlebihan",
        "research_ref": "Ginger and Curcumin anti-inflammatory studies (COX-2 inhibition)"
    }
}

# ===== INGREDIENT DATABASE (Active Compounds) =====
INGREDIENT_DATABASE = {
    "Daun Salam (Syzygium polyanthum)": {
        "active_compounds": ["Flavonoid", "Tanin", "Minyak atsiri"],
        "benefits": ["Menurunkan gula darah", "Menurunkan kolesterol", "Menurunkan asam urat", "Antioksidan"],
        "mechanism": "Menghambat enzim alfa-glukosidase, meningkatkan sensitivitas insulin",
        "safe_dose": "5-15 gram/hari (daun segar)",
        "contraindications": ["Hipoglikemia", "Hipotensi"],
        "drug_interactions": ["Obat diabetes", "Obat hipertensi"]
    },
    
    "Sambiloto (Andrographis paniculata)": {
        "active_compounds": ["Andrographolide 2-4%", "Deoxyandrographolide"],
        "benefits": ["Imunomodulator", "Hepatoprotektor", "Anti-diabetes", "Anti-virus"],
        "mechanism": "Meningkatkan CD4+, inhibisi alfa-glukosidase",
        "safe_dose": "3-10 gram/hari (herba kering), 400-1200 mg ekstrak/hari",
        "contraindications": ["Kehamilan", "Menyusui", "Gangguan kesuburan"],
        "drug_interactions": ["Obat imunosupresan", "Obat diabetes"]
    },
    
    "Kayu Manis (Cinnamomum burmani)": {
        "active_compounds": ["Cinnamaldehyde", "Coumarin", "Eugenol"],
        "benefits": ["Menurunkan gula darah", "Antioksidan", "Anti-inflamasi"],
        "mechanism": "Meningkatkan sensitivitas insulin, menghambat enzim pencernaan karbohidrat",
        "safe_dose": "1-6 gram/hari (bubuk)",
        "contraindications": ["Gangguan hati (coumarin tinggi)", "Kehamilan"],
        "drug_interactions": ["Obat diabetes", "Antikoagulan"]
    },
    
    "Temulawak (Curcuma xanthorrhiza)": {
        "active_compounds": ["Xanthorrhizol", "Curcumin", "Minyak atsiri"],
        "benefits": ["Hepatoprotektor (paten Jerman)", "Meningkatkan nafsu makan", "Anti-kolesterol", "Antioksidan"],
        "mechanism": "Melindungi sel hati, meningkatkan produksi empedu",
        "safe_dose": "10-20 gram/hari (rimpang segar)",
        "contraindications": ["Obstruksi saluran empedu", "Batu empedu"],
        "drug_interactions": ["Obat diabetes", "Obat kolesterol"]
    },
    
    "Kunyit (Curcuma longa)": {
        "active_compounds": ["Curcumin 3-5%", "Demethoxycurcumin", "Bisdemethoxycurcumin"],
        "benefits": ["Anti-inflamasi (setara ibuprofen)", "Hepatoprotektor", "Antioksidan", "Anti-kanker (in-vitro)"],
        "mechanism": "Inhibisi COX-2 dan LOX, antioksidan kuat",
        "safe_dose": "10-20 gram/hari (rimpang segar), 1.5-3 gram/hari (bubuk)",
        "contraindications": ["Kehamilan", "Gangguan pembekuan darah", "Obstruksi empedu"],
        "drug_interactions": ["Antikoagulan", "Obat diabetes", "Obat kemoterapi"]
    },
    
    "Jahe Merah (Zingiber officinale)": {
        "active_compounds": ["Gingerol 2-3%", "Shogaol", "Zingeron"],
        "benefits": ["Anti-inflamasi", "Antioksidan", "Ekspektoran", "Anti-mual", "Meningkatkan sirkulasi"],
        "mechanism": "Inhibisi COX-2 dan LOX, meningkatkan thermogenesis",
        "safe_dose": "1-4 gram/hari (rimpang segar), hingga 10 gram untuk kondisi tertentu",
        "contraindications": ["Gangguan pembekuan darah", "Tukak lambung aktif"],
        "drug_interactions": ["Antikoagulan", "Obat diabetes"]
    },
    
    "Kencur (Kaempferia galanga)": {
        "active_compounds": ["Ethyl p-methoxycinnamate", "Minyak atsiri"],
        "benefits": ["Ekspektoran", "Anti-inflamasi", "Meningkatkan stamina", "Aromaterapi"],
        "mechanism": "Relaksasi otot bronkus, anti-inflamasi",
        "safe_dose": "5-15 gram/hari (rimpang segar)",
        "contraindications": ["Kehamilan trimester 1", "Alergi"],
        "drug_interactions": ["Minimal"]
    },
    
    "Seledri (Apium graveolens)": {
        "active_compounds": ["Apigenin", "Luteolin", "3-n-Butylphthalide"],
        "benefits": ["Menurunkan tekanan darah", "Menurunkan asam urat", "Diuretik ringan"],
        "mechanism": "Vasodilatasi, meningkatkan ekskresi asam urat",
        "safe_dose": "5-10 gram/hari (daun segar)",
        "contraindications": ["Hipotensi", "Gangguan ginjal berat"],
        "drug_interactions": ["Obat hipertensi", "Diuretik"]
    },
    
    "Bawang Putih (Allium sativum)": {
        "active_compounds": ["Allicin", "Ajoene", "S-allyl cysteine"],
        "benefits": ["Menurunkan kolesterol", "Menurunkan tekanan darah", "Antitrombotik", "Antimikroba"],
        "mechanism": "Inhibisi HMG-CoA reductase, vasodilatasi",
        "safe_dose": "1-3 siung/hari (segar), 600-1200 mg ekstrak/hari",
        "contraindications": ["Gangguan pembekuan darah", "Operasi (hentikan 7 hari sebelum)"],
        "drug_interactions": ["Antikoagulan", "Obat HIV (saquinavir)"]
    },
    
    "Daun Sirsak (Annona muricata)": {
        "active_compounds": ["Acetogenins", "Alkaloid", "Flavonoid"],
        "benefits": ["Anti-kanker (in-vitro)", "Menurunkan asam urat", "Antioksidan"],
        "mechanism": "Sitotoksik terhadap sel kanker, antioksidan",
        "safe_dose": "5-10 gram/hari (daun kering)",
        "contraindications": ["Kehamilan", "Parkinson (neurotoksik jika berlebihan)"],
        "drug_interactions": ["Obat hipertensi", "Obat diabetes"]
    }
}

# ===== RESEARCH REFERENCES =====
RESEARCH_REFERENCES = {
    "Antidiabetes": [
        {
            "title": "Uji Klinis Fase I Jamu Antihiperglikemia",
            "authors": "B2P2TOOT Research Team",
            "year": 2018,
            "finding": "Formula jamu (daun salam 5g + sambiloto 5g + kayu manis 7g + temulawak 10g) setara dengan metformin dalam menurunkan glukosa darah",
            "source": "Universitas Wahid Hasyim - Clinical Trial Report"
        },
        {
            "title": "Andrographis paniculata in diabetes management",
            "authors": "Jayakumar et al.",
            "year": 2013,
            "journal": "Phytotherapy Research",
            "finding": "Andrographolide menurunkan glukosa darah melalui inhibisi alfa-glukosidase"
        }
    ],
    
    "Kolesterol": [
        {
            "title": "Uji Klinis Jamu Penurun Kolesterol",
            "authors": "B2P2TOOT",
            "year": 2019,
            "finding": "Formula 7 tanaman aman, tidak mengubah fungsi hati/ginjal, efektif menurunkan kolesterol",
            "source": "ResearchGate - Clinical Trial Publication"
        }
    ],
    
    "Hepatoprotektif": [
        {
            "title": "Saintifikasi Jamu Hepatoprotektif",
            "authors": "B2P2TOOT",
            "year": 2020,
            "finding": "Formula kunyit + temulawak + daun jombang terbukti melindungi fungsi hati",
            "source": "Universitas Padjadjaran Research"
        }
    ],
    
    "Curcumin": [
        {
            "title": "Curcumin: A Review of Its Effects on Human Health",
            "authors": "Hewlings & Kalman",
            "year": 2017,
            "journal": "Foods",
            "finding": "Curcumin memiliki efek anti-inflamasi setara ibuprofen, hepatoprotektor, antioksidan"
        },
        {
            "title": "Therapeutic Roles of Curcumin",
            "authors": "Gupta et al.",
            "year": 2013,
            "journal": "Biochimica et Biophysica Acta",
            "finding": "Curcumin efektif untuk berbagai kondisi inflamasi dan metabolik"
        }
    ],
    
    "Ginger": [
        {
            "title": "Ginger—An Herbal Medicinal Product with Broad Anti-Inflammatory Actions",
            "authors": "Grzanna et al.",
            "year": 2005,
            "journal": "Journal of Medicinal Food",
            "finding": "Gingerol menghambat COX-2 dan LOX, efektif untuk inflamasi"
        }
    ]
}


class JamuCalculatorService:
    """Service class for jamu formulation calculations"""
    
    @staticmethod
    def get_formula_by_condition(condition):
        """Get validated jamu formula by health condition"""
        return JAMU_FORMULAS.get(condition, {})
    
    @staticmethod
    def calculate_ingredients(condition, servings=1, body_weight=60, age_group="adult"):
        """
        Calculate precise ingredient quantities
        
        Args:
            condition: Health condition
            servings: Number of servings (1 serving = 1 day typically)
            body_weight: Body weight in kg (for dosage adjustment)
            age_group: 'adult' or 'elderly'
        
        Returns:
            dict with calculated ingredients and instructions
        """
        formula = JAMU_FORMULAS.get(condition)
        if not formula:
            return None
        
        # Weight adjustment factor
        if body_weight < 50:
            weight_factor = 0.8
        elif body_weight > 80:
            weight_factor = 1.2
        else:
            weight_factor = 1.0
        
        # Age adjustment
        if age_group == "elderly":
            age_factor = 0.9
        else:
            age_factor = 1.0
        
        # Calculate adjusted ingredients
        adjusted_ingredients = {}
        for ingredient, base_amount in formula["ingredients"].items():
            adjusted_amount = base_amount * weight_factor * age_factor * servings
            adjusted_ingredients[ingredient] = round(adjusted_amount, 1)
        
        # Adjust preparation instructions for multiple servings
        preparation = formula["preparation"]
        # Extract water volumes and multiply by servings
        import re
        water_match = re.search(r'(\d+)\s*ml\s*air', preparation)
        if water_match:
            base_water = int(water_match.group(1))
            adjusted_water = base_water * servings
            preparation = preparation.replace(f"{base_water} ml air", f"{adjusted_water} ml air")
        
        # Also adjust the resulting volume
        result_match = re.search(r'tersisa\s*(\d+)\s*ml', preparation)
        if result_match:
            base_result = int(result_match.group(1))
            adjusted_result = base_result * servings
            preparation = preparation.replace(f"tersisa {base_result} ml", f"tersisa {adjusted_result} ml")
        
        return {
            "condition": condition,
            "servings": servings,
            "body_weight": body_weight,
            "age_group": age_group,
            "ingredients": adjusted_ingredients,
            "preparation": preparation,
            "dosage": formula["dosage"],
            "duration": formula["duration"],
            "clinical_evidence": formula["clinical_evidence"],
            "contraindications": formula["contraindications"],
            "side_effects": formula["side_effects"]
        }
    
    @staticmethod
    def get_ingredient_info(ingredient_name):
        """Get detailed information about an ingredient"""
        return INGREDIENT_DATABASE.get(ingredient_name, {})
    
    @staticmethod
    def check_contraindications(condition, user_profile):
        """
        Check for contraindications based on user profile
        
        Args:
            condition: Health condition
            user_profile: dict with keys like 'pregnant', 'medications', 'conditions'
        
        Returns:
            list of warnings
        """
        formula = JAMU_FORMULAS.get(condition, {})
        contraindications = formula.get("contraindications", [])
        warnings = []
        
        # Check pregnancy
        if user_profile.get('pregnant') and "Kehamilan" in contraindications:
            warnings.append("⚠️ TIDAK DIANJURKAN untuk ibu hamil")
        
        # Check breastfeeding
        if user_profile.get('breastfeeding') and "Menyusui" in contraindications:
            warnings.append("⚠️ TIDAK DIANJURKAN untuk ibu menyusui")
        
        # Check existing conditions
        user_conditions = user_profile.get('conditions', [])
        for contra in contraindications:
            if any(cond.lower() in contra.lower() for cond in user_conditions):
                warnings.append(f"⚠️ PERHATIAN: {contra}")
        
        # Check drug interactions
        if user_profile.get('taking_medications'):
            warnings.append("⚠️ KONSULTASI DOKTER: Anda sedang mengonsumsi obat. Periksa interaksi obat.")
        
        return warnings
    
    @staticmethod
    def calculate_cost(condition, servings=7, ingredient_prices=None):
        """
        Calculate cost of jamu ingredients
        
        Args:
            condition: Health condition
            servings: Number of servings
            ingredient_prices: dict of ingredient prices per 100g (optional)
        
        Returns:
            dict with cost breakdown
        """
        # Default prices (Rp per 100 gram)
        default_prices = {
            "Daun Salam": 5000,
            "Sambiloto": 15000,
            "Kayu Manis": 25000,
            "Temulawak": 8000,
            "Kunyit": 6000,
            "Jahe Merah": 12000,
            "Kencur": 10000,
            "Seledri": 8000,
            "Bawang Putih": 15000,
            "Daun Sirsak": 10000,
            "Daun Jombang": 12000,
            "Beras": 3000,
            "Asam Jawa": 8000,
            "Gula Aren": 20000,
            "Madu": 50000,
            "Daun Mint": 15000,
            "Mengkudu": 5000,
            "Daun Sembung": 10000,
            "Jeruk Nipis": 10000
        }
        
        prices = ingredient_prices or default_prices
        
        calculation = JamuCalculatorService.calculate_ingredients(condition, servings)
        if not calculation:
            return None
        
        cost_breakdown = {}
        total_cost = 0
        
        for ingredient, amount_grams in calculation["ingredients"].items():
            # Extract base ingredient name (before parentheses)
            base_name = ingredient.split("(")[0].strip()
            
            # Find matching price
            price_per_100g = 0
            for price_key, price_value in prices.items():
                if price_key in base_name:
                    price_per_100g = price_value
                    break
            
            if price_per_100g == 0:
                price_per_100g = 10000  # default
            
            item_cost = (amount_grams / 100) * price_per_100g
            cost_breakdown[ingredient] = {
                "amount_grams": amount_grams,
                "price_per_100g": price_per_100g,
                "total_cost": item_cost
            }
            total_cost += item_cost
        
        cost_per_serving = total_cost / servings if servings > 0 else 0
        
        return {
            "condition": condition,
            "servings": servings,
            "cost_breakdown": cost_breakdown,
            "total_cost": total_cost,
            "cost_per_serving": cost_per_serving,
            "cost_per_day": cost_per_serving  # assuming 1 serving = 1 day
        }
    
    @staticmethod
    def get_research_references(condition):
        """Get scientific references for a condition"""
        # Map condition to research category
        if "Diabetes" in condition or "Hiperglikemia" in condition:
            return RESEARCH_REFERENCES.get("Antidiabetes", [])
        elif "Kolesterol" in condition:
            return RESEARCH_REFERENCES.get("Kolesterol", [])
        elif "Hepato" in condition or "Hati" in condition:
            return RESEARCH_REFERENCES.get("Hepatoprotektif", [])
        elif "Kunyit" in condition or "Rematik" in condition or "Maag" in condition:
            return RESEARCH_REFERENCES.get("Curcumin", [])
        elif "Batuk" in condition or "Flu" in condition or "Nyeri" in condition:
            return RESEARCH_REFERENCES.get("Ginger", [])
        else:
            return []
    
    @staticmethod
    def get_all_conditions():
        """Get list of all available health conditions"""
        return list(JAMU_FORMULAS.keys())
