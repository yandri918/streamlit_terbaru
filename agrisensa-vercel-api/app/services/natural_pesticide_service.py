"""Service for managing natural pesticide plant information."""
from app.data.natural_pesticide_db import NaturalPesticideDatabase


class NaturalPesticideService:
    """Service for natural pesticide plant knowledge."""
    
    @staticmethod
    def get_all_plants():
        """Get all natural pesticide plants."""
        return NaturalPesticideDatabase.get_all_plants()
    
    @staticmethod
    def get_plant_list():
        """Get simplified list of plants for browsing."""
        return NaturalPesticideDatabase.get_plant_list()
    
    @staticmethod
    def get_plant_by_id(plant_id):
        """Get specific plant details by ID."""
        return NaturalPesticideDatabase.get_plant_detail(plant_id)
    
    @staticmethod
    def search_plants(query):
        """Search plants by name, pest, or chemical compound."""
        if not query or len(query.strip()) == 0:
            return []
        return NaturalPesticideDatabase.search_plants(query)
    
    @staticmethod
    def get_by_pest(pest_name):
        """Find plants that control specific pest."""
        if not pest_name or len(pest_name.strip()) == 0:
            return []
        return NaturalPesticideDatabase.search_by_pest(pest_name)
    
    @staticmethod
    def get_formulations(plant_id):
        """Get all formulation methods for a plant."""
        plant = NaturalPesticideDatabase.get_plant_detail(plant_id)
        if not plant:
            return None
        return {
            "plant_name": plant["names"]["common"],
            "scientific_name": plant["taxonomy"]["jenis"],
            "formulations": plant["formulations"]
        }
    
    @staticmethod
    def get_by_plant_part(part):
        """Filter plants by plant part used."""
        if not part or len(part.strip()) == 0:
            return []
        return NaturalPesticideDatabase.get_by_plant_part(part)
    
    @staticmethod
    def get_all_pests():
        """Get list of all pests that can be controlled by natural pesticides."""
        all_plants = NaturalPesticideDatabase.get_all_plants()
        pests = set()
        
        for plant in all_plants.values():
            pests.update(plant["target_pests"])
        
        return sorted(list(pests))
    
    @staticmethod
    def get_all_plant_parts():
        """Get list of all plant parts used in natural pesticides."""
        all_plants = NaturalPesticideDatabase.get_all_plants()
        parts = set()
        
        for plant in all_plants.values():
            parts.update(plant["plant_parts_used"])
        
        return sorted(list(parts))
