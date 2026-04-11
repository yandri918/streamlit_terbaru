"""Database of natural pesticide plants.
Source: BALITSA (Balai Penelitian Tanaman Sayuran) 2008
Publication: Tumbuhan Bahan Pestisida Nabati dan Cara Pembuatannya
Authors: Wiwin Setiawati, Rini Murtiningsih, Neni Gunaeni, dan Tati Rubiati
"""

class NaturalPesticideDatabase:
    """Static database for natural pesticide plants."""
    
    @staticmethod
    def get_all_plants():
        """Return dictionary of natural pesticide plants."""
        return {
            "ajeran": {
                "id": "ajeran",
                "taxonomy": {
                    "divisi": "Spermatophyta",
                    "sub_divisi": "Angiospermae",
                    "kelas": "Dicotyledonae",
                    "bangsa": "Asterales",
                    "suku": "Asteraceae",
                    "warga": "Bidens",
                    "jenis": "Bidens pilosa L.",
                    "sinonim": ["Bidens sundaica Blume", "Bidens leucorrhiza (Lour.) DC."]
                },
                "names": {
                    "common": "Ajeran",
                    "regional": {
                        "sunda": "Hareuga",
                        "jawa": "Jaringan, Ketut"
                    },
                    "english": "Spanish needle"
                },
                "description": {
                    "overview": "Termasuk tumbuhan liar dan banyak ditemui di pinggir jalan. Kadang-kadang ditanam di halaman sebagai tanaman hias.",
                    "characteristics": "Tumbuhan ini tingginya dapat mencapai 150 cm. Batang berbentuk segi empat, warna hijau. Daun bertiga-tiga, masing-masing berbentuk bulat telur, pinggir bergerigi. Bunga bertangkai panjang, mahkota bunga berwarna putih dengan putik berwarna kuning.",
                    "distribution": "Tumbuhan ini berasal dari Amerika Selatan menyebar ke Afrika dan Asia.",
                    "habitat": "Ajeran merupakan tanaman liar, dan sering dianggap sebagai gulma pada ladang sayuran."
                },
                "plant_parts_used": [
                    "Biji (Seeds)",
                    "Seluruh bagian tanaman di atas tanah (Herba)"
                ],
                "chemical_compounds": [
                    "Flavonoid",
                    "Terpen",
                    "Fenilpropanoid",
                    "Lemak",
                    "Benzenoid"
                ],
                "mode_of_action": "Bersifat sebagai insektisida",
                "target_pests": [
                    "Kutu Daun (Aphids)",
                    "Ulat Tanah",
                    "Tungau (Mites)"
                ],
                "formulations": [
                    {
                        "id": "ajeran_ekstrak_biji",
                        "name": "Ekstrak Biji Ajeran",
                        "materials": {
                            "main": [
                                {"item": "Biji ajeran", "amount": "1 gelas"},
                                {"item": "Air", "amount": "1 liter"}
                            ],
                            "additives": [
                                {"item": "Sabun/deterjen", "amount": "secukupnya"}
                            ],
                            "tools": [
                                "Panci",
                                "Ember",
                                "Alat penyaring"
                            ]
                        },
                        "preparation_steps": [
                            "Masukkan biji ajeran ke dalam panci",
                            "Tambahkan air",
                            "Didihkan selama 5 menit",
                            "Saring",
                            "Tambahkan larutan dengan 1 liter air",
                            "Tambahkan sabun",
                            "Aduk hingga rata"
                        ],
                        "application_method": "Semprotkan ke seluruh bagian tanaman atau siram ke tanah di sekitar tanaman",
                        "target_pests": [
                            "Kutu Daun",
                            "Ulat Tanah",
                            "Tungau"
                        ]
                    },
                    {
                        "id": "ajeran_ekstrak_tanaman",
                        "name": "Ekstrak Tanaman Ajeran",
                        "materials": {
                            "main": [
                                {"item": "Tanaman ajeran utuh", "amount": "1 tanaman"},
                                {"item": "Air", "amount": "2 liter"}
                            ],
                            "additives": [
                                {"item": "Sabun/deterjen", "amount": "secukupnya"}
                            ],
                            "tools": [
                                "Pisau/alat pemotong",
                                "Ember",
                                "Alat penyaring"
                            ]
                        },
                        "preparation_steps": [
                            "Rajang tanaman ajeran",
                            "Rendam dalam air selama 24 jam",
                            "Saring sampai getahnya keluar",
                            "Tambahkan sabun/deterjen",
                            "Aduk hingga rata"
                        ],
                        "application_method": "Semprotkan ke seluruh bagian tanaman atau siram ke tanah di sekitar tanaman",
                        "target_pests": [
                            "Kutu Daun",
                            "Ulat Tanah",
                            "Tungau"
                        ]
                    }
                ],
                "safety": {
                    "effect_on_beneficial_organisms": "Aman",
                    "toxicity_level": "Rendah",
                    "precautions": [
                        "Gunakan sarung tangan saat menyiapkan",
                        "Hindari kontak langsung dengan mata",
                        "Simpan di tempat yang aman dari jangkauan anak-anak"
                    ]
                },
                "other_benefits": [
                    "Obat demam",
                    "Membantu pencernaan yang tidak baik",
                    "Mengatasi rematik (nyeri persendian)",
                    "Obat selesma",
                    "Membantu mengatasi usus buntu",
                    "Obat wasir"
                ],
                "source": {
                    "publication": "Tumbuhan Bahan Pestisida Nabati dan Cara Pembuatannya",
                    "publisher": "Balai Penelitian Tanaman Sayuran (BALITSA)",
                    "year": 2008,
                    "page_reference": "10-12"
                }
            }
            # Additional plants can be added here following the same structure
        }
    
    @staticmethod
    def get_plant_list():
        """Get simplified list of all plants for browsing."""
        all_plants = NaturalPesticideDatabase.get_all_plants()
        return [
            {
                "id": plant["id"],
                "name": plant["names"]["common"],
                "scientific_name": plant["taxonomy"]["jenis"],
                "english_name": plant["names"]["english"],
                "target_pests": plant["target_pests"],
                "parts_used": plant["plant_parts_used"],
                "formulation_count": len(plant["formulations"])
            }
            for plant in all_plants.values()
        ]
    
    @staticmethod
    def get_plant_detail(plant_id):
        """Get detailed information for specific plant."""
        all_plants = NaturalPesticideDatabase.get_all_plants()
        return all_plants.get(plant_id)
    
    @staticmethod
    def search_by_pest(pest_name):
        """Find plants that control specific pest."""
        pest_lower = pest_name.lower()
        all_plants = NaturalPesticideDatabase.get_all_plants()
        results = []
        
        for plant in all_plants.values():
            # Check if pest is in target_pests
            if any(pest_lower in pest.lower() for pest in plant["target_pests"]):
                results.append({
                    "id": plant["id"],
                    "name": plant["names"]["common"],
                    "scientific_name": plant["taxonomy"]["jenis"],
                    "target_pests": plant["target_pests"],
                    "formulations": plant["formulations"]
                })
        
        return results
    
    @staticmethod
    def search_plants(query):
        """Search plants by name, pest, or chemical compound."""
        query_lower = query.lower()
        all_plants = NaturalPesticideDatabase.get_all_plants()
        results = []
        
        for plant in all_plants.values():
            # Search in common name
            if query_lower in plant["names"]["common"].lower():
                results.append(plant)
                continue
            
            # Search in scientific name
            if query_lower in plant["taxonomy"]["jenis"].lower():
                results.append(plant)
                continue
            
            # Search in target pests
            if any(query_lower in pest.lower() for pest in plant["target_pests"]):
                results.append(plant)
                continue
            
            # Search in chemical compounds
            if any(query_lower in compound.lower() for compound in plant["chemical_compounds"]):
                results.append(plant)
                continue
            
            # Search in regional names
            for regional_name in plant["names"]["regional"].values():
                if query_lower in regional_name.lower():
                    results.append(plant)
                    break
        
        return results
    
    @staticmethod
    def get_by_plant_part(part):
        """Filter plants by plant part used."""
        part_lower = part.lower()
        all_plants = NaturalPesticideDatabase.get_all_plants()
        results = []
        
        for plant in all_plants.values():
            if any(part_lower in plant_part.lower() for plant_part in plant["plant_parts_used"]):
                results.append(plant)
        
        return results
