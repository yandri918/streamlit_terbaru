class FertilizerCatalogDB:
    """Database for fertilizer catalog and prices."""
    
    @staticmethod
    def get_catalog():
        """Get the full fertilizer catalog."""
        return [
            {
                "category": "Pupuk Majemuk (NPK)",
                "products": [
                    {
                        "name": "NPK 16-16-16 Pak Tani",
                        "manufacturer": "Saprotan Utama",
                        "description": "Pupuk NPK seimbang (Nitrogen 16%, Phosphate 16%, Kalium 16%) yang mudah larut dalam air. Cocok untuk fase vegetatif dan generatif awal.",
                        "price_range": "Rp 20.000 - Rp 25.000 / kg",
                        "image_url": "https://saprotan-utama.com/wp-content/uploads/2018/03/NPK-16-16-16.png",
                        "link": "https://saprotan-utama.com/product/npk-16-16-16-pak-tani/"
                    },
                    {
                        "name": "NPK Mutiara 16-16-16",
                        "manufacturer": "Meroke Tetap Jaya",
                        "description": "Pupuk NPK granular biru yang sangat populer. Mengandung hara makro dan mikro yang seimbang.",
                        "price_range": "Rp 18.000 - Rp 22.000 / kg",
                        "image_url": "https://down-id.img.susercontent.com/file/id-11134207-7r98o-lsmk0z4z5z4z56", # Example image
                        "link": ""
                    },
                    {
                        "name": "NPK Phonska Plus 15-15-15",
                        "manufacturer": "Petrokimia Gresik",
                        "description": "Pupuk NPK non-subsidi dengan tambahan Zinc (Zn) dan Sulfur (S).",
                        "price_range": "Rp 15.000 - Rp 18.000 / kg",
                        "image_url": "https://petrokimia-gresik.com/images/product/pupuk-npk-phonska-plus.png",
                        "link": "https://petrokimia-gresik.com/product/pupuk-npk-phonska-plus"
                    }
                ]
            },
            {
                "category": "Pupuk Fosfat (P)",
                "products": [
                    {
                        "name": "Fertiphos Pak Tani",
                        "manufacturer": "Saprotan Utama",
                        "description": "Pupuk Fosfat (P2O5 20%) yang diperkaya dengan Magnesium, Kalsium, Sulfur, dan Boron. Alternatif SP-36.",
                        "price_range": "Rp 16.000 - Rp 20.000 / kg",
                        "image_url": "https://saprotan-utama.com/wp-content/uploads/2020/10/Fertiphos.png",
                        "link": "https://saprotan-utama.com/product/fertiphos/"
                    },
                    {
                        "name": "MKP Pak Tani",
                        "manufacturer": "Saprotan Utama",
                        "description": "Mono Kalium Phosphate (P2O5 52%, K2O 34%). Bebas Nitrogen, cocok untuk pembuahan dan pembungaan.",
                        "price_range": "Rp 65.000 - Rp 75.000 / kg",
                        "image_url": "https://saprotan-utama.com/wp-content/uploads/2018/03/MKP.png",
                        "link": "https://saprotan-utama.com/product/mkp-pak-tani/"
                    },
                    {
                        "name": "SP-36 Non Subsidi",
                        "manufacturer": "Petrokimia Gresik",
                        "description": "Pupuk Fosfat tunggal dengan kandungan P2O5 36%.",
                        "price_range": "Rp 15.000 - Rp 18.000 / kg",
                        "image_url": "https://petrokimia-gresik.com/images/product/pupuk-sp-36.png",
                        "link": "https://petrokimia-gresik.com/product/pupuk-sp-36"
                    }
                ]
            },
            {
                "category": "Pupuk Kalium (K)",
                "products": [
                    {
                        "name": "KCL Mahkota",
                        "manufacturer": "Pupuk Kaltim",
                        "description": "Pupuk Kalium Klorida (60% K2O). Meningkatkan kualitas buah dan ketahanan tanaman.",
                        "price_range": "Rp 18.000 - Rp 22.000 / kg",
                        "image_url": "https://www.pupukkaltim.com/assets/images/product/kcl.png", # Placeholder
                        "link": ""
                    },
                    {
                        "name": "ZK (Kalium Sulfat)",
                        "manufacturer": "Petrokimia Gresik",
                        "description": "Pupuk Kalium bebas Klorin. Cocok untuk tanaman sensitif klorin seperti tembakau dan kentang.",
                        "price_range": "Rp 25.000 - Rp 30.000 / kg",
                        "image_url": "https://petrokimia-gresik.com/images/product/pupuk-zk.png",
                        "link": "https://petrokimia-gresik.com/product/pupuk-zk"
                    }
                ]
            },
            {
                "category": "Pupuk Nitrogen (N)",
                "products": [
                    {
                        "name": "Urea Non Subsidi",
                        "manufacturer": "Pusri / Pupuk Kujang",
                        "description": "Pupuk Nitrogen (46% N) higroskopis. Memacu pertumbuhan vegetatif.",
                        "price_range": "Rp 10.000 - Rp 12.000 / kg",
                        "image_url": "https://petrokimia-gresik.com/images/product/pupuk-urea.png",
                        "link": ""
                    },
                    {
                        "name": "ZN Urecote",
                        "manufacturer": "Saprotan Utama",
                        "description": "Urea coated dengan tambahan Zinc. Lebih efisien dan tidak mudah menguap.",
                        "price_range": "Rp 15.000 - Rp 18.000 / kg",
                        "image_url": "https://saprotan-utama.com/wp-content/uploads/2018/03/Urecote.png",
                        "link": "https://saprotan-utama.com/product/urecote/"
                    }
                ]
            },
             {
                "category": "Pupuk Mikro & Lainnya",
                "products": [
                    {
                        "name": "Kalsium Super Cap Tawon",
                        "manufacturer": "Kertopaten",
                        "description": "Pupuk Kalsium (CaCO3) untuk mencegah rontok bunga/buah dan menetralkan pH tanah.",
                        "price_range": "Rp 5.000 - Rp 8.000 / kg",
                        "image_url": "",
                        "link": ""
                    },
                    {
                         "name": "Borate 48",
                         "manufacturer": "Import",
                         "description": "Pupuk mikro Boron (B2O3 48%). Mencegah gejala kekurangan boron seperti daun keriting.",
                         "price_range": "Rp 35.000 - Rp 45.000 / kg",
                         "image_url": "",
                         "link": ""
                    }
                ]
            }
        ]
