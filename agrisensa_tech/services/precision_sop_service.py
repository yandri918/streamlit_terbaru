"""
Multi-Commodity Precision SOP Service
Standardized Agronomy Data for Melon, Chili, and Rice.
"""

class PrecisionSopService:
    """
    Service SOP Presisi Multi-Komoditas.
    Mendukung: Melon (MHI), Cabai (Intensif), Padi (Modern).
    """
    
    CROP_CONFIG = {
        'Melon (Eksklusif MHI)': {
            'target_yield_ton_ha': 25.0,
            'pop_per_ha': 20000,
            'cycle_days': 70,
            'price_per_kg': 15000,
            'phases': {
                'vegetative': (0, 25), 'flowering': (26, 35), 'fruiting': (36, 55), 'ripening': (56, 70)
            }
        },
        'Cabai Merah (Intensif)': {
            'target_yield_ton_ha': 18.0, # Target tinggi (intensif)
            'pop_per_ha': 18000,
            'cycle_days': 120, # Sampai panen raya
            'price_per_kg': 25000, # Fluktuatif, ambil rata-rata
            'phases': {
                'vegetative': (0, 30), 'flowering': (31, 50), 'fruiting': (51, 80), 'ripening': (81, 120)
            }
        },
        'Padi Sawah (Modern)': {
            'target_yield_ton_ha': 10.0, # Target Super Intensif (PTT+SRI)
            'pop_per_ha': 160000, # Rumpun (Jajar Legowo 2:1)
            'cycle_days': 105, # Varietas Unggul
            'price_per_kg': 6000, # GKP
            'phases': {
                'vegetative': (0, 40), 'flowering': (41, 65), 'fruiting': (66, 90), 'ripening': (91, 105)
            }
        }
    }

    # --- NUTRIENT & WORK DATABASES ---
    
    # 1. MELON (Data MHI yg sudah ada)
    MELON_DATA = {
        'Fase 1: Vegetatif (HST 0-25)': {
            'ec': 1.8, 'n': 180, 'p': 60, 'k': 200, 'ca': 150, 'water': 0.8,
            'focus': 'Akar & Batang Kokoh',
            'tasks': ['Pewiwilan tunas air', 'Lilit sulur', 'Pupuk N-Ca rutin']
        },
        'Fase 2: Bunga/Polinasi (HST 26-35)': {
            'ec': 2.0, 'n': 120, 'p': 80, 'k': 220, 'ca': 180, 'water': 1.0,
            'focus': 'Polinasi & Cegah Rontok',
            'tasks': ['Masukkan lebah/polinasi manual', 'Stop pestisida', 'Seleksi bunga']
        },
        'Fase 3: Pembesaran (HST 36-55)': {
            'ec': 2.2, 'n': 150, 'p': 70, 'k': 300, 'ca': 200, 'water': 1.5,
            'focus': 'Size Buah & Netting',
            'tasks': ['Topging (Seleksi 1 buah)', 'Gantung buah', 'Cek ulat/lalat buah']
        },
        'Fase 4: Pematangan (HST 56-Panen)': {
            'ec': 1.8, 'n': 80, 'p': 60, 'k': 350, 'ca': 150, 'water': 0.8,
            'focus': 'Kemanisan (Brix)',
            'tasks': ['Kurangi air (Dry down)', 'Stop N', 'Cek Brix']
        }
    }

    # 2. CABAI (Standard Intensif) - Enhanced
    CHILI_DATA = {
        'Fase 1: Vegetatif (HST 0-30)': {
            'ec': 1.5, 'n': 150, 'p': 80, 'k': 100, 'ca': 120, 'water': 0.3,
            'focus': 'Percabangan "Y" Kuat',
            'tasks': [
                'Rempel tunas air di bawah cabang Y', 
                'Pasang ajir/tali gawar awal', 
                'Aplikasi NPK 16-16-16 (200 kg/ha)',
                'Cek Kutu Kebul/Thrips (Vektor Virus)',
                'Mulsa plastik hitam-perak'
            ]
        },
        'Fase 2: Bunga & Buah Awal (HST 31-50)': {
            'ec': 2.0, 'n': 120, 'p': 100, 'k': 200, 'ca': 180, 'water': 0.5,
            'focus': 'Bunga Serempak & Anti-Rontok',
            'tasks': [
                'Spray Kalsium Boron (2-3x/minggu)', 
                'Pasang tali gawar vertikal', 
                'Monitor Lalat Buah (Trap metil eugenol)',
                'Aplikasi KNO3 (150 kg/ha)',
                'Cek pH tanah (target 6.0-6.5)'
            ]
        },
        'Fase 3: Pembesaran Buah (HST 51-80)': {
            'ec': 2.5, 'n': 140, 'p': 80, 'k': 280, 'ca': 200, 'water': 0.8,
            'focus': 'Bobot Buah & Ketebalan Dinding',
            'tasks': [
                'Pupuk K tinggi (KNO3 + KCL 250 kg/ha)', 
                'Pengendalian Patek (Fungisida rotasi FRAC)',
                'Sanitasi gulma & buah busuk',
                'Irigasi tetes 2x/hari (pagi-sore)',
                'Monitor EC larutan (2.0-2.5 mS/cm)'
            ]
        },
        'Fase 4: Panen Raya (HST 81-120)': {
            'ec': 2.0, 'n': 100, 'p': 60, 'k': 200, 'ca': 150, 'water': 0.6,
            'focus': 'Panen Kontinyu & Maintenance',
            'tasks': [
                'Panen interval 3-4 hari (merah 80%)', 
                'Sortasi buah busuk/cacat',
                'Rotasi pestisida (hindari resistensi)',
                'Pemupukan maintenance (NPK 15-15-15)',
                'Cek nematoda akar (gejala layu)'
            ]
        }
    }

    # 3. PADI (Target 10 Ton/Ha - Super Intensif)
    RICE_DATA = {
        'Fase 1: Vegetatif/Anakan Maksimal (HST 0-40)': {
            'ec': 0.0, 'n': 150, 'p': 90, 'k': 75, 'ca': 0, 'water': 5.0,
            'focus': 'Anakan Produktif 25-30 btg/rumpun',
            'tasks': [
                'Tanam sistem Jajar Legowo 2:1 (25x12.5 cm)',
                'Bibit muda (15-21 HSS), 1-2 btg/lubang',
                'Pupuk dasar: Urea 100 kg + SP-36 150 kg + KCl 100 kg/ha',
                'Pengairan macak-macak (0-10 HST) lalu genangan 2-3 cm',
                'Penyiangan I (15-20 HST) + Aplikasi herbisida selektif',
                'Pupuk susulan I (21 HST): Urea 100 kg + NPK Phonska 150 kg/ha',
                'Monitor hama keong mas & penggerek batang'
            ]
        },
        'Fase 2: Primordia/Bunting (HST 41-65)': {
            'ec': 0.0, 'n': 75, 'p': 60, 'k': 125, 'ca': 0, 'water': 10.0,
            'focus': 'Malai Panjang & Bulir Banyak',
            'tasks': [
                'Pupuk susulan II (42 HST): Urea 75 kg + KCl 75 kg/ha',
                'Jaga air tergenang 5-7 cm (fase kritis)',
                'Aplikasi ZPT (Giberelin) untuk perpanjangan malai',
                'Cek hama: Penggerek batang, Wereng, Putih Palsu',
                'Penyiangan II (40-45 HST)',
                'Spray MKP 0-52-34 (2 kg/ha) saat primordia',
                'Monitor kadar N daun (SPAD meter > 35)'
            ]
        },
        'Fase 3: Pengisian Bulir (HST 66-90)': {
            'ec': 0.0, 'n': 0, 'p': 30, 'k': 75, 'ca': 0, 'water': 5.0,
            'focus': 'Bobot 1000 Butir (>28 gram)',
            'tasks': [
                'Pupuk susulan III (70 HST): KCl 50 kg + MKP 2 kg/ha',
                'Spray pupuk daun (P-K tinggi) 2x seminggu',
                'Jaga daun bendera tetap hijau (fotosintesis maksimal)',
                'Pengairan intermiten (3 hari kering, 1 hari basah)',
                'Halau burung (pasang jaring/orang-orangan)',
                'Cek Walang Sangit & Kepinding Tanah',
                'Monitor kadar air gabah (panen 22-24%)'
            ]
        },
        'Fase 4: Pematangan & Panen (HST 91-105)': {
            'ec': 0.0, 'n': 0, 'p': 0, 'k': 0, 'ca': 0, 'water': 0.0,
            'focus': 'Kuning Jerami 90% & Panen Tepat Waktu',
            'tasks': [
                'Keringkan lahan total (10-14 hari sebelum panen)',
                'Cek kematangan: 90% bulir kuning, kadar air 22-24%',
                'Siapkan combine harvester / sabit bergerigi',
                'Panen pagi hari (hindari kehilangan hasil)',
                'Perontokan segera (max 24 jam pasca panen)',
                'Pengeringan GKP hingga 14% (jemur/dryer)',
                'Evaluasi: Hitung GKG, rendemen, losses'
            ]
        }
    }

    def get_crop_data(self, crop_name, hst):
        """Get nutrient/task data for specific crop and HST."""
        config = self.CROP_CONFIG.get(crop_name)
        schedule = {}
        
        if 'Melon' in crop_name: schedule = self.MELON_DATA
        elif 'Cabai' in crop_name: schedule = self.CHILI_DATA
        elif 'Padi' in crop_name: schedule = self.RICE_DATA
        
        # Determine Phase
        current_phase = "Unknown"
        phase_details = {}
        
        # Logic range checking
        # Simplification: iterate keys, parse range? 
        # Better: Use the 'phases' config to determine key
        
        for phase_key, (start, end) in config['phases'].items():
            if start <= hst <= end:
                # Find matching key in Schedule Dict (text based matching)
                # Map 'vegetative' -> 'Fase 1...'
                if phase_key == 'vegetative': prefix = 'Fase 1'
                elif phase_key == 'flowering' or phase_key == 'primordia': prefix = 'Fase 2'
                elif phase_key == 'fruiting' or phase_key == 'filling': prefix = 'Fase 3'
                else: prefix = 'Fase 4'
                
                for k, v in schedule.items():
                    if k.startswith(prefix):
                        current_phase = k
                        phase_details = v
                        break
                break
        
        # Fallback if hst out of range (e.g. > cycle)
        if not phase_details and hst > config['cycle_days']:
             current_phase = "Pasca Panen",
             phase_details = {'focus': 'Selesai', 'tasks': ['Evaluasi Hasil'], 'ec': 0, 'n':0, 'p':0,'k':0,'ca':0}

        return current_phase, phase_details

    def calculate_yield_potential(self, crop_name, ha_value):
        """Calculate estimates based on HA."""
        cfg = self.CROP_CONFIG.get(crop_name)
        target = cfg['target_yield_ton_ha']
        price = cfg['price_per_kg']
        
        total_ton = ha_value * target
        revenue = total_ton * 1000 * price
        
        return {
            'total_yield_ton': total_ton,
            'revenue': revenue,
            'target_per_ha': target
        }
