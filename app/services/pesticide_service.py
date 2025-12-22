from app.data.pesticide_db import PesticideDatabase

class PesticideService:
    """Service for managing pesticide information."""
    
    @staticmethod
    def get_all_pesticides():
        """Get all pesticide active ingredients."""
        return PesticideDatabase.get_all_pesticides()
    
    @staticmethod
    def get_pesticide_by_id(pesticide_id):
        """Get specific pesticide details by ID."""
        pesticides = PesticideDatabase.get_all_pesticides()
        return pesticides.get(pesticide_id)
    
    @staticmethod
    def search_pesticides(query):
        """Search pesticides by name, target, or type."""
        query = query.lower()
        all_pesticides = PesticideDatabase.get_all_pesticides()
        results = []
        
        for p in all_pesticides.values():
            # Search in name, type, group, or targets
            if (query in p['name'].lower() or 
                query in p['type'].lower() or 
                query in p['group'].lower() or 
                any(query in t.lower() for t in p['targets'])):
                results.append(p)
                
        return results
