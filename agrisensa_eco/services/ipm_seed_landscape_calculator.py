"""
IPM, Seed Network, and Landscape Planning Calculator
Integrated Pest Management 2.0, Seed Saving, and Farm Design
"""

class IPMSeedLandscapeCalculator:
    """Calculator for IPM, seed saving, and landscape planning"""
    
    # Common pests database (for AI identification simulation)
    PEST_DATABASE = {
        'Wereng Coklat': {
            'scientific_name': 'Nilaparvata lugens',
            'crops_affected': ['Padi'],
            'damage_type': 'Penghisap cairan tanaman',
            'symptoms': 'Daun menguning, tanaman kerdil, hopperburn',
            'organic_control': [
                'Predator alami: Laba-laba, kepik',
                'Varietas tahan wereng',
                'Pengaturan jarak tanam',
                'Hindari pemupukan N berlebihan'
            ],
            'chemical_control': 'Imidakloprid, Buprofezin (last resort)',
            'prevention': 'Rotasi varietas, sanitasi lahan'
        },
        'Ulat Grayak': {
            'scientific_name': 'Spodoptera litura',
            'crops_affected': ['Cabai', 'Tomat', 'Kedelai'],
            'damage_type': 'Pemakan daun',
            'symptoms': 'Lubang pada daun, kotoran hitam',
            'organic_control': [
                'Bacillus thuringiensis (Bt)',
                'Predator: Trichogramma wasps',
                'Pestisida nabati: ekstrak nimba',
                'Hand picking larva'
            ],
            'chemical_control': 'Klorpirifos, Profenofos (last resort)',
            'prevention': 'Perangkap feromon, crop rotation'
        },
        'Kutu Daun': {
            'scientific_name': 'Aphis spp.',
            'crops_affected': ['Cabai', 'Tomat', 'Sayuran'],
            'damage_type': 'Penghisap cairan, vektor virus',
            'symptoms': 'Daun keriting, embun madu, semut',
            'organic_control': [
                'Predator: Ladybug, lacewing',
                'Semprotan air kuat',
                'Sabun insektisida',
                'Minyak nimba'
            ],
            'chemical_control': 'Imidakloprid (last resort)',
            'prevention': 'Tanaman refugia, mulsa reflektif'
        },
        'Penggerek Batang': {
            'scientific_name': 'Ostrinia furnacalis',
            'crops_affected': ['Jagung'],
            'damage_type': 'Penggerek batang dan tongkol',
            'symptoms': 'Lubang pada batang, patah batang, tongkol rusak',
            'organic_control': [
                'Trichogramma parasitoid',
                'Bacillus thuringiensis (Bt)',
                'Potong dan musnahkan tanaman terserang',
                'Tanam varietas tahan'
            ],
            'chemical_control': 'Karbofuran granul (last resort)',
            'prevention': 'Sanitasi, tanam serempak, rotasi tanaman'
        },
        'Trips': {
            'scientific_name': 'Thrips spp.',
            'crops_affected': ['Cabai', 'Bawang', 'Bunga'],
            'damage_type': 'Penghisap cairan, vektor virus',
            'symptoms': 'Bercak perak pada daun, daun menggulung',
            'organic_control': [
                'Perangkap biru lengket',
                'Predator: Orius bugs',
                'Minyak nimba',
                'Mulsa reflektif'
            ],
            'chemical_control': 'Spinosad, Abamectin',
            'prevention': 'Sanitasi gulma, tanaman perangkap'
        }
    }
    
    # Seed saving network - heirloom varieties
    SEED_VARIETIES = {
        'Padi Lokal': {
            'Padi Gogo Merah': {
                'origin': 'Jawa Barat',
                'characteristics': 'Tahan kering, warna merah, aromatik',
                'days_to_harvest': 120,
                'yield_potential': '3-4 ton/ha',
                'conservation_status': 'Endangered'
            },
            'Padi Hitam': {
                'origin': 'Toraja',
                'characteristics': 'Antosianin tinggi, nilai gizi tinggi',
                'days_to_harvest': 150,
                'yield_potential': '2-3 ton/ha',
                'conservation_status': 'Rare'
            }
        },
        'Jagung Lokal': {
            'Jagung Pulut': {
                'origin': 'Jawa Timur',
                'characteristics': 'Sticky, manis, untuk kue tradisional',
                'days_to_harvest': 90,
                'yield_potential': '4-5 ton/ha',
                'conservation_status': 'Vulnerable'
            }
        },
        'Cabai Lokal': {
            'Cabai Gendot': {
                'origin': 'Jawa Tengah',
                'characteristics': 'Besar, daging tebal, tidak terlalu pedas',
                'days_to_harvest': 90,
                'yield_potential': '15-20 ton/ha',
                'conservation_status': 'Common'
            }
        }
    }
    
    def identify_pest(self, pest_name):
        """Simulate AI pest identification"""
        pest_data = self.PEST_DATABASE.get(pest_name)
        
        if pest_data:
            return {
                'identified': True,
                'pest_name': pest_name,
                'confidence': 92.5,  # Simulated AI confidence
                'data': pest_data
            }
        else:
            return {
                'identified': False,
                'message': 'Hama tidak ditemukan dalam database'
            }
    
    def calculate_ipm_cost_benefit(self, area_ha, conventional_cost_per_ha, 
                                   ipm_cost_per_ha, yield_increase_pct):
        """Calculate cost-benefit of IPM vs conventional"""
        
        # Conventional approach
        conventional_total_cost = area_ha * conventional_cost_per_ha
        
        # IPM approach
        ipm_total_cost = area_ha * ipm_cost_per_ha
        
        # Cost savings
        cost_savings = conventional_total_cost - ipm_total_cost
        
        # Yield benefit (assuming base yield)
        base_yield_value = area_ha * 50000000  # Rp 50 juta/ha (example)
        yield_increase_value = base_yield_value * (yield_increase_pct / 100)
        
        # Total benefit
        total_benefit = cost_savings + yield_increase_value
        
        return {
            'conventional_cost': conventional_total_cost,
            'ipm_cost': ipm_total_cost,
            'cost_savings': cost_savings,
            'yield_increase_value': yield_increase_value,
            'total_benefit': total_benefit,
            'roi_pct': (total_benefit / ipm_total_cost * 100) if ipm_total_cost > 0 else 0
        }
    
    def calculate_landscape_zones(self, total_area_ha, production_pct, 
                                  conservation_pct, infrastructure_pct):
        """Calculate optimal landscape zones"""
        
        production_area = total_area_ha * (production_pct / 100)
        conservation_area = total_area_ha * (conservation_pct / 100)
        infrastructure_area = total_area_ha * (infrastructure_pct / 100)
        
        # Recommendations based on ratios
        recommendations = []
        
        if conservation_pct < 10:
            recommendations.append("⚠️ Zona konservasi terlalu kecil. Minimal 10-15% untuk biodiversitas")
        
        if production_pct > 80:
            recommendations.append("⚠️ Zona produksi terlalu dominan. Pertimbangkan diversifikasi")
        
        if infrastructure_pct < 5:
            recommendations.append("💡 Pertimbangkan infrastruktur lebih baik (jalan, irigasi, storage)")
        
        return {
            'production_area_ha': production_area,
            'conservation_area_ha': conservation_area,
            'infrastructure_area_ha': infrastructure_area,
            'total_allocated': production_area + conservation_area + infrastructure_area,
            'recommendations': recommendations
        }
