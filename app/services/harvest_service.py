"""Service layer for Harvest Storage - Business logic."""
from app.data.harvest_storage_db import HarvestStorageDatabase
from typing import Dict, List, Optional


class HarvestService:
    """Business logic for harvest storage."""
    
    def __init__(self):
        self.db = HarvestStorageDatabase()
    
    def validate_record_data(self, data: Dict) -> Dict:
        """Validate harvest record data."""
        errors = []
        
        # Required fields
        required = ['farmer_name', 'farmer_phone', 'commodity', 'location', 'harvest_date', 'criteria']
        
        for field in required:
            if not data.get(field):
                errors.append(f'{field} is required')
        
        # Validate criteria
        criteria = data.get('criteria', [])
        if not criteria or len(criteria) == 0:
            errors.append('At least one criterion is required')
        else:
            for i, criterion in enumerate(criteria):
                if not criterion.get('size'):
                    errors.append(f'Criterion {i+1}: size is required')
                if not criterion.get('quantity_kg') or criterion.get('quantity_kg') <= 0:
                    errors.append(f'Criterion {i+1}: quantity must be greater than 0')
                if not criterion.get('price_per_kg') or criterion.get('price_per_kg') <= 0:
                    errors.append(f'Criterion {i+1}: price must be greater than 0')
        
        # Validate phone number
        phone = data.get('farmer_phone', '')
        if phone and not phone.startswith('08') and not phone.startswith('+62'):
            errors.append('Invalid phone number format')
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def calculate_criterion_total(self, quantity_kg: float, price_per_kg: float) -> float:
        """Calculate total for a criterion."""
        return quantity_kg * price_per_kg
    
    def prepare_criteria(self, criteria: List[Dict]) -> List[Dict]:
        """Prepare criteria with calculated totals."""
        prepared = []
        for criterion in criteria:
            quantity = float(criterion.get('quantity_kg', 0))
            price = float(criterion.get('price_per_kg', 0))
            
            prepared.append({
                'size': criterion.get('size'),
                'quantity_kg': quantity,
                'price_per_kg': price,
                'total': self.calculate_criterion_total(quantity, price)
            })
        
        return prepared
    
    def get_farmer_summary(self, farmer_phone: str) -> Dict:
        """Get summary statistics for a specific farmer."""
        stats = self.db.get_statistics(farmer_phone=farmer_phone)
        records = self.db.get_records(farmer_phone=farmer_phone)
        
        # Get recent harvests
        recent_harvests = records[:5] if len(records) > 5 else records
        
        # Get top commodities
        commodities = stats.get('commodities', {})
        top_commodities = sorted(
            commodities.items(),
            key=lambda x: x[1]['quantity'],
            reverse=True
        )[:3]
        
        return {
            'total_records': stats['total_records'],
            'total_quantity_kg': stats['total_quantity_kg'],
            'total_value': stats['total_value'],
            'avg_price_per_kg': stats['avg_price_per_kg'],
            'recent_harvests': recent_harvests,
            'top_commodities': [
                {
                    'commodity': c[0],
                    'quantity': c[1]['quantity'],
                    'value': c[1]['value']
                }
                for c in top_commodities
            ]
        }
