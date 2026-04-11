"""Database layer for Harvest Storage - Record keeping for farmers."""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import uuid


class HarvestStorageDatabase:
    """JSON-based database for harvest records."""
    
    def __init__(self, data_dir='instance'):
        """Initialize database with data directory."""
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        self.records_file = os.path.join(data_dir, 'harvest_records.json')
        
        # Initialize file if it doesn't exist
        self._init_file(self.records_file, [])
    
    def _init_file(self, filepath, default_data):
        """Initialize JSON file if it doesn't exist."""
        if not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(default_data, f, ensure_ascii=False, indent=2)
    
    def _read_json(self, filepath):
        """Read JSON file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return []
    
    def _write_json(self, filepath, data):
        """Write JSON file."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error writing {filepath}: {e}")
            return False
    
    # ========== HARVEST RECORD OPERATIONS ==========
    
    def add_record(self, farmer_name: str, farmer_phone: str, commodity: str,
                   location: str, harvest_date: str, criteria: List[Dict],
                   costs: Optional[Dict] = None, notes: str = '',
                   weather: str = '', harvest_sequence: int = 1) -> Dict:
        """Add a new harvest record with multiple criteria, costs, and profitability."""
        records = self._read_json(self.records_file)
        
        # Calculate totals from criteria
        total_quantity = sum(c.get('quantity_kg', 0) for c in criteria)
        total_value = sum(c.get('total', 0) for c in criteria)
        
        # Calculate costs and profitability
        costs = costs or {}
        total_cost = sum(costs.values())
        profit = total_value - total_cost
        profit_margin = (profit / total_value * 100) if total_value > 0 else 0
        roi = (profit / total_cost * 100) if total_cost > 0 else 0
        cost_per_kg = total_cost / total_quantity if total_quantity > 0 else 0
        revenue_per_kg = total_value / total_quantity if total_quantity > 0 else 0
        
        record = {
            'id': str(uuid.uuid4()),
            'farmer_name': farmer_name,
            'farmer_phone': farmer_phone,
            'commodity': commodity,
            'location': location,
            'harvest_date': harvest_date,
            'harvest_sequence': harvest_sequence,
            'criteria': criteria,
            'total_quantity': total_quantity,
            'total_value': total_value,
            # Cost tracking
            'costs': costs,
            'total_cost': total_cost,
            # Profitability
            'profit': profit,
            'profit_margin': round(profit_margin, 2),
            'roi': round(roi, 2),
            'cost_per_kg': cost_per_kg,
            'revenue_per_kg': revenue_per_kg,
            # Quick wins
            'notes': notes,
            'weather': weather,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        records.append(record)
        self._write_json(self.records_file, records)
        return record
    
    def get_records(self, farmer_phone: Optional[str] = None,
                   commodity: Optional[str] = None,
                   start_date: Optional[str] = None,
                   end_date: Optional[str] = None) -> List[Dict]:
        """Get harvest records with optional filters."""
        records = self._read_json(self.records_file)
        
        # Apply filters
        if farmer_phone:
            records = [r for r in records if r.get('farmer_phone') == farmer_phone]
        if commodity:
            records = [r for r in records if r.get('commodity') == commodity]
        if start_date:
            records = [r for r in records if r.get('harvest_date', '') >= start_date]
        if end_date:
            records = [r for r in records if r.get('harvest_date', '') <= end_date]
        
        # Sort by harvest_date (newest first)
        records.sort(key=lambda x: x.get('harvest_date', ''), reverse=True)
        
        return records
    
    def get_record_by_id(self, record_id: str) -> Optional[Dict]:
        """Get harvest record by ID."""
        records = self._read_json(self.records_file)
        for record in records:
            if record['id'] == record_id:
                return record
        return None
    
    def update_record(self, record_id: str, updates: Dict) -> bool:
        """Update harvest record."""
        records = self._read_json(self.records_file)
        for i, record in enumerate(records):
            if record['id'] == record_id:
                record.update(updates)
                record['updated_at'] = datetime.now().isoformat()
                
                # Recalculate totals if criteria changed
                if 'criteria' in updates:
                    criteria = record['criteria']
                    record['total_quantity'] = sum(c.get('quantity_kg', 0) for c in criteria)
                    record['total_value'] = sum(c.get('total', 0) for c in criteria)
                
                # Recalculate profitability if costs or criteria changed
                if 'costs' in updates or 'criteria' in updates:
                    total_quantity = record.get('total_quantity', 0)
                    total_value = record.get('total_value', 0)
                    costs = record.get('costs', {})
                    total_cost = sum(costs.values())
                    profit = total_value - total_cost
                    
                    record['total_cost'] = total_cost
                    record['profit'] = profit
                    record['profit_margin'] = round((profit / total_value * 100) if total_value > 0 else 0, 2)
                    record['roi'] = round((profit / total_cost * 100) if total_cost > 0 else 0, 2)
                    record['cost_per_kg'] = total_cost / total_quantity if total_quantity > 0 else 0
                    record['revenue_per_kg'] = total_value / total_quantity if total_quantity > 0 else 0
                
                records[i] = record
                return self._write_json(self.records_file, records)
        return False
    
    def delete_record(self, record_id: str) -> bool:
        """Delete harvest record."""
        records = self._read_json(self.records_file)
        records = [r for r in records if r['id'] != record_id]
        return self._write_json(self.records_file, records)
    
    # ========== STATISTICS ==========
    
    def get_statistics(self, farmer_phone: Optional[str] = None) -> Dict:
        """Get harvest statistics."""
        records = self.get_records(farmer_phone=farmer_phone)
        
        if not records:
            return {
                'total_records': 0,
                'total_quantity_kg': 0,
                'total_value': 0,
                'avg_price_per_kg': 0,
                'commodities': {},
                'by_size': {},
                'by_month': {}
            }
        
        total_quantity = sum(r.get('total_quantity', 0) for r in records)
        total_value = sum(r.get('total_value', 0) for r in records)
        
        # Count by commodity
        commodities = {}
        for record in records:
            commodity = record.get('commodity', 'unknown')
            if commodity not in commodities:
                commodities[commodity] = {
                    'count': 0,
                    'quantity': 0,
                    'value': 0
                }
            commodities[commodity]['count'] += 1
            commodities[commodity]['quantity'] += record.get('total_quantity', 0)
            commodities[commodity]['value'] += record.get('total_value', 0)
        
        # Count by size/grade
        by_size = {}
        for record in records:
            for criterion in record.get('criteria', []):
                size = criterion.get('size', 'unknown')
                if size not in by_size:
                    by_size[size] = {
                        'quantity': 0,
                        'value': 0,
                        'avg_price': 0
                    }
                by_size[size]['quantity'] += criterion.get('quantity_kg', 0)
                by_size[size]['value'] += criterion.get('total', 0)
        
        # Calculate average prices for each size
        for size in by_size:
            if by_size[size]['quantity'] > 0:
                by_size[size]['avg_price'] = by_size[size]['value'] / by_size[size]['quantity']
        
        # Count by month
        by_month = {}
        for record in records:
            harvest_date = record.get('harvest_date', '')
            if harvest_date:
                month = harvest_date[:7]  # YYYY-MM
                if month not in by_month:
                    by_month[month] = {
                        'count': 0,
                        'quantity': 0,
                        'value': 0
                    }
                by_month[month]['count'] += 1
                by_month[month]['quantity'] += record.get('total_quantity', 0)
                by_month[month]['value'] += record.get('total_value', 0)
        
        return {
            'total_records': len(records),
            'total_quantity_kg': total_quantity,
            'total_value': total_value,
            'avg_price_per_kg': total_value / total_quantity if total_quantity > 0 else 0,
            'commodities': commodities,
            'by_size': by_size,
            'by_month': by_month
        }
    
    def get_chart_data(self, farmer_phone: Optional[str] = None) -> Dict:
        """Get data formatted for charts."""
        stats = self.get_statistics(farmer_phone)
        
        # Pie chart data - commodities
        commodity_labels = list(stats['commodities'].keys())
        commodity_values = [stats['commodities'][c]['quantity'] for c in commodity_labels]
        
        # Bar chart data - by size
        size_labels = list(stats['by_size'].keys())
        size_quantities = [stats['by_size'][s]['quantity'] for s in size_labels]
        size_prices = [stats['by_size'][s]['avg_price'] for s in size_labels]
        
        # Line chart data - by month
        month_labels = sorted(stats['by_month'].keys())
        month_quantities = [stats['by_month'][m]['quantity'] for m in month_labels]
        month_values = [stats['by_month'][m]['value'] for m in month_labels]
        
        return {
            'commodity_distribution': {
                'labels': commodity_labels,
                'data': commodity_values
            },
            'size_distribution': {
                'labels': size_labels,
                'quantities': size_quantities,
                'prices': size_prices
            },
            'monthly_trend': {
                'labels': month_labels,
                'quantities': month_quantities,
                'values': month_values
            }
        }
