"""
Greenhouse Biosecurity Service
Calculates material needs, costs, and generates SOPs for Greenhouse Biosecurity (Ante-room, Double Door, IPM).
"""

class GreenhouseBiosecurityService:
    """
    Service untuk perencanaan infrastruktur Biosecurity Greenhouse.
    Mengacu pada standar SOP Melon GH MHI.
    """
    
    # Material Costs (Estimates in IDR)
    COST_DB = {
        'insect_net_mesh_50': 25000, # per m2 (Mesh 50 for Thrips/Whitefly)
        'polycarbonate_sheet': 150000, # per m2 (Walls/Roof)
        'aluminium_frame': 75000, # per m (Structure)
        'sticky_trap_yellow': 5000, # per sheet (A4)
        'sticky_trap_blue': 5000, # per sheet
        'disinfectant_footbath': 150000, # per unit (Tray + Mat)
        'hand_wash_sink': 750000, # per unit (Basic sink + tap)
        'apd_set': 350000, # Coverall, Boots, Mask, Gloves
        'door_unit': 1500000 # Standard alumunium/glass door
    }
    
    def calculate_anteroom_cost(self, width_m, length_m, height_m, n_doors=2):
        """
        Hitung biaya pembuatan Anteroom (Ruang Antara) Double Door.
        """
        # Surface Areas
        wall_area = 2 * (width_m + length_m) * height_m
        roof_area = width_m * length_m
        floor_area = width_m * length_m
        
        # Structure Frame (Simple estimation: perimeter top/bottom + corners + door frames)
        frame_len = (2 * (width_m + length_m) * 2) + (4 * height_m)
        
        # Bill of Materials
        bom = {
            'polycarbonate_or_plastic': {
                'qty': wall_area + roof_area,
                'unit': 'm²',
                'cost': (wall_area + roof_area) * self.COST_DB['polycarbonate_sheet']
            },
            'frame_structure': {
                'qty': frame_len,
                'unit': 'm',
                'cost': frame_len * self.COST_DB['aluminium_frame']
            },
            'doors': {
                'qty': n_doors,
                'unit': 'unit',
                'cost': n_doors * self.COST_DB['door_unit']
            },
            'infrastructure_total': 0
        }
        
        infra_total = bom['polycarbonate_or_plastic']['cost'] + bom['frame_structure']['cost'] + bom['doors']['cost']
        bom['infrastructure_total'] = infra_total
        
        return bom
    
    def calculate_ipm_needs(self, gh_area_m2, crop_type='Melon'):
        """
        Hitung kebutuhan Sticky Trap dan Insect Net.
        Trap density: 1 per 20-50m2 (High risk) or 1 per 100m2 (Monitoring).
        SOP MHI: 1 trap per X m2 monitoring.
        """
        # Monitoring Density (Standard)
        monitoring_traps = max(2, int(gh_area_m2 / 50)) # Min 2 traps per GH
        
        # Mass Trapping Density (Outbreak)
        mass_traps = int(gh_area_m2 / 10) 
        
        return {
            'monitoring_yellow_traps': monitoring_traps,
            'mass_trapping_yellow_traps': mass_traps,
            'cost_monitoring': monitoring_traps * self.COST_DB['sticky_trap_yellow'],
            'cost_mass_trapping': mass_traps * self.COST_DB['sticky_trap_yellow']
        }

    def generate_sop_checklist(self, gh_name="GH-1", manager_name="Manager"):
        """
        Generate SOP text based on MHI Biosecurity standards.
        """
        sop_text = f"""
# SOP BIOSECURITY & ALUR MASUK GREENHOUSE (SOP-{gh_name})
**Penanggung Jawab:** {manager_name}
**Revisi:** 1.0 (Standard Export)

---

## A. ZONA LUAR (PRE-ENTRY)
1. [ ] **Parkir & Alas Kaki Luar**: Lepas alas kaki luar (sepatu/sandal rumah) di batas zona kotor.
2. [ ] **Kebersihan Diri**: Tangan tidak memegang benda kotor/rokok sebelum masuk.

## B. ANTEROOM (ZONA TRANSISI / HYGIENE LOCK)
**Pintu Luar harus ditutup sebelum melakukan aktivitas di sini!**

3. [ ] **Cuci Tangan (Hand Wash)**:
   - Gunakan sabun cair.
   - Gosok punggung tangan, sela jari, dan kuku minimal 20 detik.
   - Bilas & keringkan.
   
4. [ ] **Pakai APD (Alat Pelindung Diri)**:
   - Pakai **Coverall/Jas Lab** khusus GH (jangan dibawa keluar).
   - Pakai **Masker** (cegah droplet/kontaminasi napas).
   - Pakai **Sarung Tangan** (Latex/Nitrile) jika menangani tanaman sensitif virus.
   
5. [ ] **Ganti Alas Kaki**:
   - Pakai Sepatu Boots khusus GH yang sudah tersedia di rak.
   
6. [ ] **Footbath (Desinfeksi Kaki)**:
   - Celupkan boots ke bak desinfektan (Chlorine/BKC) selama 5 detik.
   - Keset kaki hingga tidak menetes.

## C. ZONA PRODUKSI (GREENHOUSE)
**Buka Pintu Dalam HANYA jika Pintu Luar sudah tertutup rapat.**

7. [ ] **Cek Sticky Trap Pintu**:
   - Pastikan trap kuning di area pintu masih lengket & tidak penuh.
   - Catat jumlah serangga yang terperangkap (jika jadwal scouting).
   
8. [ ] **Aktivitas Kerja**:
   - Bergerak dari Blok Tanaman Sehat -> ke Blok Sakit (JANGAN TERBALIK).
   - Dilarang merokok/makan di dalam GH.

## D. ALUR KELUAR
9. [ ] Buang sampah APD disposable (masker/gloves) ke tempat sampah tertutup di Anteroom.
10. [ ] Gantung kembali Coverall di Rak APD (Sisi Bersih).
11. [ ] Celup kembali boots sebelum dilepas.
12. [ ] Cuci tangan sebelum meninggalkan area.

---
**PENTING:** Kunci keberhasilan Biosecurity adalah KEDISIPLINAN, bukan sekadar fasilitas.
        """
        return sop_text
