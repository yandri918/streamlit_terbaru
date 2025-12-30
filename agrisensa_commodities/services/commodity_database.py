"""
Indonesian Export Commodity Database for WAGRI Market Intelligence
Contains metadata for priority export commodities to Japan

Author: AgriSensa Team
Date: 2025-12-30
"""

from typing import Dict, List


class CommodityDatabase:
    """
    Database of Indonesian export commodities with metadata.
    Focus on high-priority items for Japan market.
    """
    
    # Indonesian Export Priority Commodities
    EXPORT_COMMODITIES = {
        "33100": {
            "name_en": "Asparagus",
            "name_id": "Asparagus",
            "name_jp": "アスパラガス",
            "category": "vegetable",
            "priority": 5,
            "indonesia_regions": ["Jawa Barat", "Jawa Tengah"],
            "typical_price_idr": 50000,  # per kg
            "export_ready": True,
            "certification_needed": ["GAP", "Phytosanitary"],
            "shelf_life_days": 7,
            "shipping_method": "Air Freight",
            "peak_season": "March-May",
            "quality_grade": "Grade A (straight, thick)",
            "packaging": "Plastic wrap, refrigerated box"
        },
        "31700": {
            "name_en": "Edamame",
            "name_id": "Kedelai Jepang (Edamame)",
            "name_jp": "枝豆",
            "category": "vegetable",
            "priority": 5,
            "indonesia_regions": ["Jawa Timur", "Jawa Tengah"],
            "typical_price_idr": 35000,
            "export_ready": True,
            "certification_needed": ["GAP", "Phytosanitary", "Organic (optional)"],
            "shelf_life_days": 5,
            "shipping_method": "Air Freight",
            "peak_season": "June-August",
            "quality_grade": "Fresh, green pods",
            "packaging": "Vacuum pack, frozen"
        },
        "46100": {
            "name_en": "Strawberry",
            "name_id": "Stroberi",
            "name_jp": "いちご",
            "category": "fruit",
            "priority": 5,
            "indonesia_regions": ["Bandung", "Malang", "Lembang"],
            "typical_price_idr": 80000,
            "export_ready": True,
            "certification_needed": ["GAP", "Phytosanitary", "HACCP"],
            "shelf_life_days": 3,
            "shipping_method": "Air Freight (Express)",
            "peak_season": "Year-round (highland)",
            "quality_grade": "Large, red, sweet (Brix >10)",
            "packaging": "Individual pack, temperature controlled"
        },
        "44100": {
            "name_en": "Mango",
            "name_id": "Mangga",
            "name_jp": "マンゴー",
            "category": "fruit",
            "priority": 4,
            "indonesia_regions": ["Indramayu", "Cirebon", "Probolinggo"],
            "typical_price_idr": 40000,
            "export_ready": True,
            "certification_needed": ["GAP", "Phytosanitary", "VHT (Vapor Heat Treatment)"],
            "shelf_life_days": 14,
            "shipping_method": "Air Freight",
            "peak_season": "September-December",
            "quality_grade": "Arumanis, Gedong Gincu (premium)",
            "packaging": "Individual wrap, carton box"
        },
        "44500": {
            "name_en": "Papaya",
            "name_id": "Pepaya",
            "name_jp": "パパイヤ",
            "category": "fruit",
            "priority": 4,
            "indonesia_regions": ["Jawa", "Sumatra", "Kalimantan"],
            "typical_price_idr": 15000,
            "export_ready": True,
            "certification_needed": ["GAP", "Phytosanitary"],
            "shelf_life_days": 10,
            "shipping_method": "Air/Sea Freight",
            "peak_season": "Year-round",
            "quality_grade": "California variety, medium size",
            "packaging": "Carton box with cushion"
        },
        "44800": {
            "name_en": "Dragon Fruit",
            "name_id": "Buah Naga",
            "name_jp": "ドラゴンフルーツ",
            "category": "fruit",
            "priority": 4,
            "indonesia_regions": ["Jawa", "Bali", "Lombok"],
            "typical_price_idr": 25000,
            "export_ready": True,
            "certification_needed": ["GAP", "Phytosanitary"],
            "shelf_life_days": 12,
            "shipping_method": "Air Freight",
            "peak_season": "Year-round",
            "quality_grade": "Red flesh, large (>350g)",
            "packaging": "Individual wrap, carton"
        },
        "42100": {
            "name_en": "Banana",
            "name_id": "Pisang",
            "name_jp": "バナナ",
            "category": "fruit",
            "priority": 3,
            "indonesia_regions": ["Lampung", "Jawa", "Sumatra"],
            "typical_price_idr": 12000,
            "export_ready": True,
            "certification_needed": ["GAP", "Phytosanitary"],
            "shelf_life_days": 14,
            "shipping_method": "Sea Freight (Reefer)",
            "peak_season": "Year-round",
            "quality_grade": "Cavendish, uniform size",
            "packaging": "Carton box, controlled atmosphere"
        },
        "42500": {
            "name_en": "Pineapple",
            "name_id": "Nanas",
            "name_jp": "パイナップル",
            "category": "fruit",
            "priority": 3,
            "indonesia_regions": ["Lampung", "Sumatra Utara"],
            "typical_price_idr": 18000,
            "export_ready": True,
            "certification_needed": ["GAP", "Phytosanitary"],
            "shelf_life_days": 21,
            "shipping_method": "Sea Freight",
            "peak_season": "Year-round",
            "quality_grade": "Sweet (Brix >14), golden color",
            "packaging": "Carton box"
        },
        "30500": {
            "name_en": "Sweet Potato",
            "name_id": "Ubi Jalar",
            "name_jp": "さつまいも",
            "category": "vegetable",
            "priority": 3,
            "indonesia_regions": ["Jawa", "Papua"],
            "typical_price_idr": 8000,
            "export_ready": True,
            "certification_needed": ["GAP", "Phytosanitary"],
            "shelf_life_days": 30,
            "shipping_method": "Sea Freight",
            "peak_season": "Year-round",
            "quality_grade": "Orange flesh, uniform size",
            "packaging": "Mesh bag, carton"
        },
        "34400": {
            "name_en": "Tomato",
            "name_id": "Tomat",
            "name_jp": "トマト",
            "category": "vegetable",
            "priority": 3,
            "indonesia_regions": ["Jawa Timur", "Jawa Barat"],
            "typical_price_idr": 20000,
            "export_ready": True,
            "certification_needed": ["GAP", "Phytosanitary"],
            "shelf_life_days": 10,
            "shipping_method": "Air Freight",
            "peak_season": "April-September",
            "quality_grade": "Cherry tomato, red, firm",
            "packaging": "Plastic container, refrigerated"
        },
        "32100": {
            "name_en": "Lettuce",
            "name_id": "Selada",
            "name_jp": "レタス",
            "category": "vegetable",
            "priority": 3,
            "indonesia_regions": ["Bandung", "Malang"],
            "typical_price_idr": 30000,
            "export_ready": True,
            "certification_needed": ["GAP", "Phytosanitary"],
            "shelf_life_days": 7,
            "shipping_method": "Air Freight",
            "peak_season": "Year-round (highland)",
            "quality_grade": "Crisp, green, hydroponic preferred",
            "packaging": "Plastic bag, refrigerated"
        },
        "34100": {
            "name_en": "Cucumber",
            "name_id": "Mentimun",
            "name_jp": "きゅうり",
            "category": "vegetable",
            "priority": 2,
            "indonesia_regions": ["Jawa", "Sumatra"],
            "typical_price_idr": 15000,
            "export_ready": True,
            "certification_needed": ["GAP", "Phytosanitary"],
            "shelf_life_days": 10,
            "shipping_method": "Air Freight",
            "peak_season": "Year-round",
            "quality_grade": "Japanese variety, straight, dark green",
            "packaging": "Plastic wrap, carton"
        },
        "31100": {
            "name_en": "Cabbage",
            "name_id": "Kubis",
            "name_jp": "キャベツ",
            "category": "vegetable",
            "priority": 2,
            "indonesia_regions": ["Jawa Barat", "Jawa Tengah"],
            "typical_price_idr": 10000,
            "export_ready": True,
            "certification_needed": ["GAP", "Phytosanitary"],
            "shelf_life_days": 21,
            "shipping_method": "Sea Freight",
            "peak_season": "Year-round (highland)",
            "quality_grade": "Tight head, fresh green",
            "packaging": "Carton box"
        },
        "30300": {
            "name_en": "Carrot",
            "name_id": "Wortel",
            "name_jp": "にんじん",
            "category": "vegetable",
            "priority": 2,
            "indonesia_regions": ["Jawa Barat", "Sumatra"],
            "typical_price_idr": 12000,
            "export_ready": True,
            "certification_needed": ["GAP", "Phytosanitary"],
            "shelf_life_days": 30,
            "shipping_method": "Sea Freight",
            "peak_season": "Year-round",
            "quality_grade": "Orange, uniform size, no cracks",
            "packaging": "Mesh bag, carton"
        },
        "45100": {
            "name_en": "Watermelon",
            "name_id": "Semangka",
            "name_jp": "すいか",
            "category": "fruit",
            "priority": 2,
            "indonesia_regions": ["Jawa", "Sumatra"],
            "typical_price_idr": 8000,
            "export_ready": True,
            "certification_needed": ["GAP", "Phytosanitary"],
            "shelf_life_days": 14,
            "shipping_method": "Sea Freight",
            "peak_season": "Year-round",
            "quality_grade": "Seedless, sweet (Brix >11)",
            "packaging": "Individual wrap, carton"
        }
    }
    
    @classmethod
    def get_commodity(cls, item_code: str) -> Dict:
        """Get commodity metadata by item code."""
        return cls.EXPORT_COMMODITIES.get(item_code, {})
    
    @classmethod
    def get_all_commodities(cls) -> Dict:
        """Get all export commodities."""
        return cls.EXPORT_COMMODITIES
    
    @classmethod
    def get_by_priority(cls, min_priority: int = 3) -> Dict:
        """
        Get commodities filtered by minimum priority level.
        
        Args:
            min_priority: Minimum priority (1-5)
        
        Returns:
            Dictionary of commodities meeting priority threshold
        """
        return {
            code: data
            for code, data in cls.EXPORT_COMMODITIES.items()
            if data.get("priority", 0) >= min_priority
        }
    
    @classmethod
    def get_by_category(cls, category: str) -> Dict:
        """
        Get commodities by category.
        
        Args:
            category: "vegetable" or "fruit"
        
        Returns:
            Dictionary of commodities in category
        """
        return {
            code: data
            for code, data in cls.EXPORT_COMMODITIES.items()
            if data.get("category") == category
        }
    
    @classmethod
    def get_export_ready(cls) -> Dict:
        """Get only export-ready commodities."""
        return {
            code: data
            for code, data in cls.EXPORT_COMMODITIES.items()
            if data.get("export_ready", False)
        }
    
    @classmethod
    def search_by_name(cls, search_term: str) -> Dict:
        """
        Search commodities by name (English, Indonesian, or Japanese).
        
        Args:
            search_term: Search string
        
        Returns:
            Dictionary of matching commodities
        """
        search_term = search_term.lower()
        results = {}
        
        for code, data in cls.EXPORT_COMMODITIES.items():
            if (search_term in data.get("name_en", "").lower() or
                search_term in data.get("name_id", "").lower() or
                search_term in data.get("name_jp", "").lower()):
                results[code] = data
        
        return results
    
    @classmethod
    def get_commodity_list(cls) -> List[Dict]:
        """
        Get list of all commodities with code and name.
        
        Returns:
            List of dictionaries with code and names
        """
        return [
            {
                "code": code,
                "name_en": data["name_en"],
                "name_id": data["name_id"],
                "name_jp": data["name_jp"],
                "priority": data["priority"],
                "category": data["category"]
            }
            for code, data in cls.EXPORT_COMMODITIES.items()
        ]
    
    @classmethod
    def get_priority_stars(cls, priority: int) -> str:
        """Convert priority number to star rating."""
        return "⭐" * priority
    
    @classmethod
    def get_typical_costs(cls, item_code: str) -> Dict:
        """
        Get typical export costs for a commodity.
        
        Args:
            item_code: Commodity code
        
        Returns:
            Dictionary with typical costs
        """
        commodity = cls.get_commodity(item_code)
        
        if not commodity:
            return {}
        
        # Default costs based on shipping method
        shipping_method = commodity.get("shipping_method", "Air Freight")
        
        if "Air" in shipping_method:
            if "Express" in shipping_method:
                air_freight = 120000  # Express air
            else:
                air_freight = 80000   # Regular air
        else:
            air_freight = 30000  # Sea freight
        
        return {
            "production": commodity.get("typical_price_idr", 20000),
            "packaging": 5000,
            "transport_to_port": 3000,
            "air_freight": air_freight,
            "customs_duty": 10000,
            "certification": 2000,
            "total_estimated": (
                commodity.get("typical_price_idr", 20000) +
                5000 + 3000 + air_freight + 10000 + 2000
            )
        }
