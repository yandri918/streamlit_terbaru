"""Database layer for AgriShop - Marketplace for agricultural products."""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import uuid


class AgriShopDatabase:
    """JSON-based database for AgriShop marketplace."""
    
    def __init__(self, data_dir='instance'):
        """Initialize database with data directory."""
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        self.products_file = os.path.join(data_dir, 'agrishop_products.json')
        self.preorders_file = os.path.join(data_dir, 'agrishop_preorders.json')
        
        # Initialize files if they don't exist
        self._init_file(self.products_file, [])
        self._init_file(self.preorders_file, [])
    
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
    
    # ========== PRODUCT OPERATIONS ==========
    
    def add_product(self, seller_name: str, seller_phone: str, commodity: str,
                   quantity_kg: float, price_per_kg: float, quality_grade: str,
                   harvest_date: str, latitude: float, longitude: float,
                   address: str = "", photo_url: str = "", description: str = "",
                   is_preorder: bool = False) -> Dict:
        """Add a new product listing."""
        products = self._read_json(self.products_file)
        
        product = {
            'id': str(uuid.uuid4()),
            'seller_name': seller_name,
            'seller_phone': seller_phone,
            'commodity': commodity,
            'quantity_kg': quantity_kg,
            'price_per_kg': price_per_kg,
            'total_price': quantity_kg * price_per_kg,
            'quality_grade': quality_grade,
            'harvest_date': harvest_date,
            'location': {
                'latitude': latitude,
                'longitude': longitude,
                'address': address
            },
            'photo_url': photo_url,
            'description': description,
            'is_preorder': is_preorder,
            'status': 'available',  # available, reserved, sold
            'views': 0,
            'interests': 0,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        products.append(product)
        self._write_json(self.products_file, products)
        return product
    
    def get_products(self, commodity: Optional[str] = None, 
                    quality_grade: Optional[str] = None,
                    status: Optional[str] = None,
                    is_preorder: Optional[bool] = None,
                    min_price: Optional[float] = None,
                    max_price: Optional[float] = None) -> List[Dict]:
        """Get products with optional filters."""
        products = self._read_json(self.products_file)
        
        # Apply filters
        if commodity:
            products = [p for p in products if p.get('commodity') == commodity]
        if quality_grade:
            products = [p for p in products if p.get('quality_grade') == quality_grade]
        if status:
            products = [p for p in products if p.get('status') == status]
        if is_preorder is not None:
            products = [p for p in products if p.get('is_preorder') == is_preorder]
        if min_price is not None:
            products = [p for p in products if p.get('price_per_kg', 0) >= min_price]
        if max_price is not None:
            products = [p for p in products if p.get('price_per_kg', 0) <= max_price]
        
        # Sort by created_at (newest first)
        products.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return products
    
    def get_product_by_id(self, product_id: str) -> Optional[Dict]:
        """Get product by ID."""
        products = self._read_json(self.products_file)
        for product in products:
            if product['id'] == product_id:
                return product
        return None
    
    def update_product(self, product_id: str, updates: Dict) -> bool:
        """Update product data."""
        products = self._read_json(self.products_file)
        for i, product in enumerate(products):
            if product['id'] == product_id:
                product.update(updates)
                product['updated_at'] = datetime.now().isoformat()
                
                # Recalculate total price if quantity or price changed
                if 'quantity_kg' in updates or 'price_per_kg' in updates:
                    product['total_price'] = product['quantity_kg'] * product['price_per_kg']
                
                products[i] = product
                return self._write_json(self.products_file, products)
        return False
    
    def delete_product(self, product_id: str) -> bool:
        """Delete product."""
        products = self._read_json(self.products_file)
        products = [p for p in products if p['id'] != product_id]
        return self._write_json(self.products_file, products)
    
    def increment_views(self, product_id: str) -> bool:
        """Increment product view count."""
        products = self._read_json(self.products_file)
        for i, product in enumerate(products):
            if product['id'] == product_id:
                product['views'] = product.get('views', 0) + 1
                products[i] = product
                return self._write_json(self.products_file, products)
        return False
    
    def increment_interests(self, product_id: str) -> bool:
        """Increment product interest count."""
        products = self._read_json(self.products_file)
        for i, product in enumerate(products):
            if product['id'] == product_id:
                product['interests'] = product.get('interests', 0) + 1
                products[i] = product
                return self._write_json(self.products_file, products)
        return False
    
    # ========== PRE-ORDER OPERATIONS ==========
    
    def add_preorder(self, product_id: str, buyer_name: str, buyer_phone: str,
                    quantity_kg: float, notes: str = "") -> Dict:
        """Add a pre-order for a product."""
        preorders = self._read_json(self.preorders_file)
        
        preorder = {
            'id': str(uuid.uuid4()),
            'product_id': product_id,
            'buyer_name': buyer_name,
            'buyer_phone': buyer_phone,
            'quantity_kg': quantity_kg,
            'notes': notes,
            'status': 'pending',  # pending, confirmed, completed, cancelled
            'created_at': datetime.now().isoformat()
        }
        
        preorders.append(preorder)
        self._write_json(self.preorders_file, preorders)
        return preorder
    
    def get_preorders(self, product_id: Optional[str] = None) -> List[Dict]:
        """Get pre-orders, optionally filtered by product_id."""
        preorders = self._read_json(self.preorders_file)
        if product_id:
            return [p for p in preorders if p.get('product_id') == product_id]
        return preorders
    
    def update_preorder_status(self, preorder_id: str, status: str) -> bool:
        """Update pre-order status."""
        preorders = self._read_json(self.preorders_file)
        for i, preorder in enumerate(preorders):
            if preorder['id'] == preorder_id:
                preorder['status'] = status
                preorders[i] = preorder
                return self._write_json(self.preorders_file, preorders)
        return False
    
    # ========== STATISTICS ==========
    
    def get_statistics(self) -> Dict:
        """Get marketplace statistics."""
        products = self._read_json(self.products_file)
        preorders = self._read_json(self.preorders_file)
        
        available_products = [p for p in products if p.get('status') == 'available']
        preorder_products = [p for p in products if p.get('is_preorder') == True]
        
        total_value = sum(p.get('total_price', 0) for p in available_products)
        total_quantity = sum(p.get('quantity_kg', 0) for p in available_products)
        
        return {
            'total_products': len(products),
            'available_products': len(available_products),
            'preorder_products': len(preorder_products),
            'total_preorders': len(preorders),
            'total_value': total_value,
            'total_quantity_kg': total_quantity,
            'commodities': self._count_by_field(products, 'commodity'),
            'quality_grades': self._count_by_field(products, 'quality_grade')
        }
    
    def _count_by_field(self, items: List[Dict], field: str) -> Dict:
        """Count items by field value."""
        counts = {}
        for item in items:
            value = item.get(field, 'unknown')
            counts[value] = counts.get(value, 0) + 1
        return counts
