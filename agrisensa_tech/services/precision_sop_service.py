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
            'target_yield_ton_ha': 9.0, # Target PTT/IP400
            'pop_per_ha': 160000, # Rumpun (Tajarwo)
            'cycle_days': 100, # Genjah
            'price_per_kg': 6000, # GKP
            'phases': {
                'vegetative': (0, 40), 'flowering': (41, 65), 'fruiting': (66, 85), 'ripening': (86, 100)
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

    # 2. CABAI (Standard Intensif)
    CHILI_DATA = {
        'Fase 1: Vegetatif (HST 0-30)': {
            'ec': 1.5, 'n': 150, 'p': 80, 'k': 100, 'ca': 100, 'water': 0.3,
            'focus': 'Percabangan "Y"',
            'tasks': ['Rempel tunas air di bawah cabang Y', 'Pasang ajir', 'Cek Kutu Kebul/Thrips (Virus)']
        },
        'Fase 2: Bunga & Buah Awal (HST 31-50)': {
            'ec': 2.0, 'n': 120, 'p': 100, 'k': 200, 'ca': 150, 'water': 0.5,
            'focus': 'Bunga Serempak & Kalsium',
            'tasks': ['Spray Kalsium (Cegah rontok)', 'Pasang tali gawar', 'Monitor Lalat Buah (Trap)']
        },
        'Fase 3: Pembesaran Buah (HST 51-80)': {
            'ec': 2.5, 'n': 140, 'p': 80, 'k': 250, 'ca': 180, 'water': 0.8,
            'focus': 'Bobot Buah & Dinding Tebal',
            'tasks': ['Pupuk K tinggi (KNO3)', 'Pengendalian Patek (Antraknosa) saat hujan', 'Sanitasi gulma']
        },
        'Fase 4: Panen Raya (HST 81-120)': {
            'ec': 2.0, 'n': 100, 'p': 60, 'k': 200, 'ca': 150, 'water': 0.6,
            'focus': 'Panen & Maintenance',
            'tasks': ['Panen interval 3-4 hari', 'Sortasi buah busuk', 'Rotasi pestisida']
        }
    }

    # 3. PADI (Standard PTT/Modern)
    # Note: Padi pakai istilah Kg/Ha pupuk tabur biasanya, dikonversi ke saran umum.
    RICE_DATA = {
        'Fase 1: Vegetatif/Anakan (HST 0-40)': {
            'ec': 0.0, 'n': 120, 'p': 60, 'k': 60, 'ca': 0, 'water': 5.0, # Intermittent
            'focus': 'Anakan Maksimal',
            'tasks': ['Tanam sistem Jajar Legowo', 'Pupuk Urea & SP-36', 'Pengairan Macak-macak (0-10 HST)', 'Siangi gulma']
        },
        'Fase 2: Primordia/Bunting (HST 41-65)': {
            'ec': 0.0, 'n': 60, 'p': 40, 'k': 100, 'ca': 0, 'water': 10.0, # Genang
            'focus': 'Malai Panjang & Bernas',
            'tasks': ['Pupuk KCL/NPK', 'Cek Hama Putih Palsu & Penggerek Batang', 'Jaga air tergenang 3cm']
        },
        'Fase 3: Pengisian Bulir (HST 66-85)': {
            'ec': 0.0, 'n': 0, 'p': 20, 'k': 60, 'ca': 0, 'water': 5.0,
            'focus': 'Bobot Gabah (1000 butir)',
            'tasks': ['Spray MKP (Daun Bendera Hijau)', 'Halau Burung', 'Cek Walang Sangit']
        },
        'Fase 4: Pematangan (HST 86-100)': {
            'ec': 0.0, 'n': 0, 'p': 0, 'k': 0, 'ca': 0, 'water': 0.0, # Keringkan
            'focus': 'Kuning Jerami & Panen',
            'tasks': ['Keringkan lahan (10 hari sebelum panen)', 'Siapkan alat panen']
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
