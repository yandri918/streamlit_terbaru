"""
IPM, Seed Network, and Landscape Planning Calculator
Integrated Pest Management 2.0, Seed Saving, and Farm Design
"""

class IPMSeedLandscapeCalculator:
    """Calculator for IPM, seed saving, and landscape planning"""
    
    # Common pests database (Matching Heatmap Risk Data)
    PEST_DATABASE = {
        # --- HORTIKULTURA ---
        'Thrips': {
            'scientific_name': 'Thrips parvispinus',
            'crops_affected': ['Cabai', 'Bawang', 'Bunga'],
            'damage_type': 'Penghisap cairan, vektor virus',
            'symptoms': 'Bercak perak pada daun bawah, daun mengeriting ke atas, bunga rontok',
            'organic_control': [
                'Perangkap likat biru (blue sticky trap)',
                'Predator: Orius bugs, Amblyseius',
                'Pestisida nabati: Tembakau, bawang putih',
                'Mulsa perak untuk memantulkan cahaya'
            ],
            'chemical_control': 'Spinosad, Abamectin (Gunakan rotasi bahan aktif)',
            'prevention': 'Sanitasi gulma, tumpang sari dengan bunga refugia'
        },
        'Kutu Kebul': {
            'scientific_name': 'Bemisia tabaci',
            'crops_affected': ['Cabai', 'Tomat', 'Terung'],
            'damage_type': 'Penghisap cairan, vektor virus Gemini (Kuning)',
            'symptoms': 'Daun menguning, kotoran embun madu (jelaga hitam)',
            'organic_control': [
                'Perangkap kuning (yellow sticky trap)',
                'Cendawan entomopatogen: Verticillium lecanii',
                'Minyak nimba (neem oil)',
                'Sabun kalium'
            ],
            'chemical_control': 'Imidakloprid, Asetamiprid (Sistemik)',
            'prevention': 'Barrier crop (jagung), varietas tahan virus'
        },
        'Tungau (Mites)': {
            'scientific_name': 'Polyphagotarsonemus latus / Tetranychus',
            'crops_affected': ['Cabai', 'Tomat', 'Jeruk'],
            'damage_type': 'Penghisap sel epidermis',
            'symptoms': 'Daun melengkung ke bawah (seperti sendok terbalik), permukaan bawah mengkilap tembaga',
            'organic_control': [
                'Predator: Phytoseiulus',
                'Belerang (Sulfur/Wettable Sulfur)',
                'Penyemprotan air bertekanan',
                'Minyak hortikultura'
            ],
            'chemical_control': 'Akarisida (Abamectin, Pyridaben)',
            'prevention': 'Hindari kekeringan ekstrem, irigasi sprinler'
        },
        'Ulat Grayak': {
            'scientific_name': 'Spodoptera litura',
            'crops_affected': ['Cabai', 'Bawang', 'Kedelai'],
            'damage_type': 'Defoliator (pemakan daun) & buah',
            'symptoms': 'Lubang pada daun, buah berlubang, kotoran hitam',
            'organic_control': [
                'Perangkap feromon seks (Exi)',
                'Bacillus thuringiensis (Bt)',
                'Virus NPV (Spodoptera litura NPV)',
                'Pengumpulan telur/larva manual'
            ],
            'chemical_control': 'Emamektin benzoat, Klorantraniliprol',
            'prevention': 'Rotasi tanaman, pasang lampu perangkap'
        },
        'Lalat Buah': {
            'scientific_name': 'Bactrocera spp.',
            'crops_affected': ['Cabai', 'Mangga', 'Jambu'],
            'damage_type': 'Larva memakan daging buah',
            'symptoms': 'Titik bekas tusukan pada buah, buah busuk basah dan rontok',
            'organic_control': [
                'Perangkap atraktan (Metil Eugenol)',
                'Pembungkusan buah',
                'Sanitasi buah jatuh (kubur dalam tanah)',
                'Ekstrak selasih'
            ],
            'chemical_control': 'Umpan protein beracun',
            'prevention': 'Kumpulkan dan musnahkan buah yang jatuh'
        },
        'Jamur (Fusarium)': {
            'scientific_name': 'Fusarium oxysporum',
            'crops_affected': ['Cabai', 'Tomat', 'Pisang'],
            'damage_type': 'Penyumbatan pembuluh xilem',
            'symptoms': 'Layu mendadak di siang hari, segar di pagi hari, akhirnya mati. Batang dipotong ada cincin coklat',
            'organic_control': [
                'Trichoderma spp. (aplikasi di tanah)',
                'PGPR (Plant Growth Promoting Rhizobacteria)',
                'Kompos matang',
                'Biofungisida Gliocladium'
            ],
            'chemical_control': 'Fungisida berbahan aktif Benomyl (Koret)',
            'prevention': 'Drainase baik, naikkan pH tanah, varietas tahan'
        },
        'Patek (Antraknosa)': {
            'scientific_name': 'Colletotrichum spp.',
            'crops_affected': ['Cabai', 'Mangga', 'Pepaya'],
            'damage_type': 'Infeksi buah dan daun',
            'symptoms': 'Bercak melingkar cekung warna oranye/hitam pada buah (patek)',
            'organic_control': [
                'Pangkas bagian sakit',
                'Ekstrak lengkuas/kunyit',
                'Agen hayati: yeast antagonis',
                'Pengurangan kelembaban'
            ],
            'chemical_control': 'Fungisida Azoxystrobin, Difenokonazol',
            'prevention': 'Jarak tanam lebar, pemakaian mulsa, kalsium cukup'
        },
        'Layu Bakteri': {
            'scientific_name': 'Ralstonia solanacearum',
            'crops_affected': ['Cabai', 'Tomat', 'Kentang'],
            'damage_type': 'Bakteri menyumbat vaskuler',
            'symptoms': 'Layu permanen cepat, jika batang dipotong dan dicelup air keluar ooze (cairan putih susu)',
            'organic_control': [
                'Bakterisida biologi (Streptomyces, Pseudomonas fluorescens)',
                'Grafting dengan batang bawah tahan (Terung pipit)',
                'Arang sekam',
                'Rotasi dengan jagung/padi'
            ],
            'chemical_control': 'Bakterisida tembaga (Coppercide), Antibiotik pertanian',
            'prevention': 'Hindari genangan air, sterilisasi alat tani'
        },
        
        # --- PADI ---
        'Wereng Coklat': {
            'scientific_name': 'Nilaparvata lugens',
            'crops_affected': ['Padi'],
            'damage_type': 'Penghisap cairan batang',
            'symptoms': 'Tanaman menguning dan kering (hopperburn), kerdil rumput/hampa',
            'organic_control': [
                'Musuh alami: Laba-laba, Paederus, Cyrtorhinus',
                'Jamur patogen: Beauveria bassiana, Metarhizium',
                'Tanam serempak',
                'Pengeringan lahan berkala (intermittent irrigation)'
            ],
            'chemical_control': 'Insektisida selektif (Pymetrozine, Buprofezin)',
            'prevention': 'Hindari pupuk N berlebih, varietas tahan (Inpari)'
        },
        'Blast (Padi)': {
            'scientific_name': 'Pyricularia oryzae',
            'crops_affected': ['Padi'],
            'damage_type': 'Jamur penyerang daun dan leher malai',
            'symptoms': 'Bercak belah ketupat pada daun, leher malai busuk (patah leher)',
            'organic_control': [
                'Corynebacterium',
                'Ekstrak daun sirih',
                'Pseudomonas fluorescens',
                'Silika (abu sekam)'
            ],
            'chemical_control': 'Fungisida Isoprotiolane, Tricyclazole',
            'prevention': 'Jangan tanam terlalu rapat, kurangi Urea'
        },
        'Hawar Daun (Kresek)': {
            'scientific_name': 'Xanthomonas oryzae',
            'crops_affected': ['Padi'],
            'damage_type': 'Bakteri daun',
            'symptoms': 'Garis basah pada tepi daun, daun mengering seperti terbakar',
            'organic_control': [
                'Paenibacillus polymyxa',
                'Ekstrak biji pinang',
                'Jarak tanam legowo',
                'Pupuk K cukup'
            ],
            'chemical_control': 'Bakterisida tembaga oksida',
            'prevention': 'Sanitasi jerami sakit, hindari pemotongan pucuk bibit'
        },
        'Keong Mas': {
            'scientific_name': 'Pomacea canaliculata',
            'crops_affected': ['Padi (fase muda)'],
            'damage_type': 'Pemakan rumpun muda',
            'symptoms': 'Rumpun padi hilang/terpotong, ada telur pink',
            'organic_control': [
                'Pungut manual telur dan keong',
                'Bebek/Itik gembala',
                'Umpan daun pepaya/talas',
                'Saringan pada saluran air masuk'
            ],
            'chemical_control': 'Moluskisida (Niklosamida)',
            'prevention': 'Tanam pindah (umur bibit >21 hari), parit keliling'
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
