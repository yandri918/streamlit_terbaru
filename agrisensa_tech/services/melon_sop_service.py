"""
Melon Precision SOP Service (Target 25 Ton/Ha - MHI Standard)
Calculates Fertigation, Irrigation, and Work Schedule for Melon Cultivation.
"""

class MelonSopService:
    """
    Service SOP Presisi Budidaya Melon.
    Mengacu pada standar MHI (Metode Hayati Indonesia) & GAP Hortikultura.
    Target: 25 Ton/Ha.
    """
    
    # 1. Database Nutrisi & Irigasi per Fase (Standard Drip/Fertigasi)
    NUTRIENT_SCHEDULE = {
        'Fase 1: Vegetatif Awal (HST 0-14)': {
            'desc': 'Pertumbuhan akar & daun.',
            'target_ec': 1.5, # mS/cm
            'ppm_n': 150,
            'ppm_p': 50, 
            'ppm_k': 150,
            'ppm_ca': 120, # Penting untuk dinding sel
            'water_l_plant_day': 0.5, # Drip volume average
            'focus': 'N & P tinggi untuk akar'
        },
        'Fase 2: Pembentukan Sulur (HST 15-25)': {
            'desc': 'Pertumbuhan batang & cabang.',
            'target_ec': 1.8,
            'ppm_n': 180,
            'ppm_p': 60,
            'ppm_k': 200,
            'ppm_ca': 150,
            'water_l_plant_day': 0.8,
            'focus': 'N & K seimbang'
        },
        'Fase 3: Pembungaan & Polinasi (HST 26-35)': {
            'desc': 'Inisiasi bunga, hentikan N sementara.',
            'target_ec': 2.0,
            'ppm_n': 120, # Turunkan N
            'ppm_p': 80,  # Naikkan P
            'ppm_k': 220,
            'ppm_ca': 180, # Cegah rontok bunga
            'water_l_plant_day': 1.0, 
            'focus': 'P & K + Boron (Mikro)'
        },
        'Fase 4: Pembesaran Buah (HST 36-55)': {
            'desc': 'Fase kritis ukuran buah.',
            'target_ec': 2.2, # Maksimal nutrisi
            'ppm_n': 150,
            'ppm_p': 70,
            'ppm_k': 300, # K tinggi untuk translokasi gula
            'ppm_ca': 200, # Cegah Blossom End Rot & Pecah Buah
            'water_l_plant_day': 1.5, # Peak water demand
            'focus': 'Kalium (K) & Kalsium (Ca)'
        },
        'Fase 5: Pematangan/Netting (HST 56-Panen)': {
            'desc': 'Pembentukan net & rasa manis (Brix).',
            'target_ec': 1.8, # Turunkan sedikit
            'ppm_n': 80,
            'ppm_p': 60,
            'ppm_k': 350, # K sangat tinggi
            'ppm_ca': 150,
            'water_l_plant_day': 0.8, # KURANGI AIR (Water Stress) untuk manis
            'focus': 'Kalium Murni (KNO3/SOP)'
        }
    }
    
    # 2. Daily Work Schedule (Mandor Logbook)
    WORK_SCHEDULE = {
        'Pra-Tanam': [
            "Sterilisasi lahan/media (Solarisasi/Kimia).",
            "Cek pH tanah/air & EC awal.",
            "Pemasangan instalasi drip irigasi & cek flow rate.",
            "Desinfeksi GreenHouse (Anteroom, Footbath)."
        ],
        'HST 0-7': [
            "Pindah tanam (sore hari).",
            "Penyiraman jenuh (loading irigasi).",
            "Monitoring hama awal (Thrips/Kutu Kebul) di yellow trap."
        ],
        'HST 8-20': [
            "Pewiwilan (pruning) tunas air di ketiak daun 1-8.",
            "Lilit sulur ke tali rambatan (tiap 2 hari).",
            "Aplikasi fungisida preventif (Mancozeb/Propineb) - FRAC M.",
            "Pupuk susulan 1 (N-Ca)."
        ],
        'HST 21-30': [
            "Persiapan polinasi (masukkan lebah atau manual).",
            "Seleksi bunga betina (biasanya ruas 9-12).",
            "Stop pestisida saat polinasi aktif!"
        ],
        'HST 31-40': [
            "Seleksi buah (Topging): Pilih 1 buah terbaik per tanaman.",
            "Buang buah lain & tunas ujung (Topping) di ruas 25-30.",
            "Gantung buah dengan net/tali.",
            "Monitoring ulat & lalat buah (Perangkap Metil Eugenol)."
        ],
        'HST 41-55': [
            "Fokus Nutriti Pembesaran (K & Ca).",
            "Jaga kelembapan tanah stabil (cegah pecah buah).",
            "Sanitasi daun tua bagian bawah (sirkulasi udara).",
            "Rotasi Fungisida Sistemik (Azoxystrobin/Difenoconazole) - FRAC 11/3."
        ],
        'HST 56-Panen': [
            "Kurangi volume irigasi bertahap (Dry Down).",
            "Stop pupuk N.",
            "Cek Brix berkala (Target > 12).",
            "Panen saat net penuh & crack tangkai (slip) muncul."
        ]
    }

    def calculate_needs(self, num_plants, ha_value=None):
        """
        Hitung total kebutuhan air & estimasi hasil untuk satu musim.
        Jika ha_value diberikan, gunakan target yield pasti: 25 Ton/Ha.
        """
        total_water_liter = 0
        total_days = 70 # approx 70 days cycle
        
        # Average water usage calculation
        avg_water = 1.0 # liter/day average
        total_water_liter = num_plants * avg_water * total_days
        
        # Target Yield Calculation
        if ha_value and ha_value > 0:
            # FORCE logic: 25 Ton per Hectare (MHI Standard)
            target_yield_ton = ha_value * 25.0
        else:
            # Estimate based on per plant if Ha unknown (approx 1.25 kg/plant for 20k pop)
            target_yield_ton = (num_plants * 1.5) / 1000 
        
        return {
            'total_water_m3': total_water_liter / 1000,
            'est_yield_ton': target_yield_ton,
            'est_gross_revenue': target_yield_ton * 15000000 # Asumsi Rp 15rb/kg
        }

    def get_schedule_by_hst(self, hst):
        """
        Return nutrient recipe & work list for specific HST.
        """
        # Determine Phase
        phase_name = "Unknown"
        phase_data = {}
        
        if hst <= 14:
            phase_name = 'Fase 1: Vegetatif Awal (HST 0-14)'
        elif hst <= 25:
            phase_name = 'Fase 2: Pembentukan Sulur (HST 15-25)'
        elif hst <= 35:
            phase_name = 'Fase 3: Pembungaan & Polinasi (HST 26-35)'
        elif hst <= 55:
            phase_name = 'Fase 4: Pembesaran Buah (HST 36-55)'
        else:
            phase_name = 'Fase 5: Pematangan/Netting (HST 56-Panen)'
            
        phase_data = self.NUTRIENT_SCHEDULE.get(phase_name, {})
        
        return {
            'phase': phase_name,
            'data': phase_data
        }
