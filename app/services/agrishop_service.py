"""Service layer for AgriShop - Business logic and integrations."""
from app.data.agrishop_db import AgriShopDatabase
from app.services.market_service import MarketService
from typing import Dict, List, Optional
import math


class AgriShopService:
    """Business logic for AgriShop marketplace."""
    
    def __init__(self):
        self.db = AgriShopDatabase()
        self.market_service = MarketService()
    
    # ========== SMART PRICING ==========
    
    def get_price_recommendation(self, commodity: str, quality_grade: str,
                                 location_lat: float, location_lon: float) -> Dict:
        """Get smart price recommendation based on market data."""
        try:
            # Get current market price
            market_data = self.market_service.get_latest_price(commodity)
            
            if not market_data or not market_data.get('success'):
                return {
                    'success': False,
                    'message': 'Data harga pasar tidak tersedia'
                }
            
            base_price = market_data.get('price', 0)
            
            # Quality adjustment
            quality_multiplier = {
                'A': 1.15,  # +15% for Grade A
                'B': 1.0,   # Base price for Grade B
                'C': 0.85   # -15% for Grade C
            }
            
            adjusted_price = base_price * quality_multiplier.get(quality_grade, 1.0)
            
            # Calculate price range (±10%)
            min_price = adjusted_price * 0.9
            max_price = adjusted_price * 1.1
            
            return {
                'success': True,
                'commodity': commodity,
                'quality_grade': quality_grade,
                'market_price': base_price,
                'recommended_price': round(adjusted_price, -2),  # Round to nearest 100
                'min_price': round(min_price, -2),
                'max_price': round(max_price, -2),
                'quality_adjustment': f"{((quality_multiplier.get(quality_grade, 1.0) - 1) * 100):+.0f}%",
                'market_trend': market_data.get('trend', 'stable'),
                'last_updated': market_data.get('date', '')
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }
    
    # ========== QUALITY VERIFICATION ==========
    
    def verify_quality_from_agrimap(self, seller_phone: str, commodity: str) -> Dict:
        """Verify product quality based on AgriMap NPK data."""
        try:
            # This would integrate with AgriMap to get NPK data
            # For now, return placeholder
            return {
                'verified': False,
                'message': 'Integrasi dengan AgriMap akan datang',
                'badges': []
            }
        except Exception as e:
            return {
                'verified': False,
                'message': f'Error: {str(e)}',
                'badges': []
            }
    
    def get_quality_badges(self, product: Dict) -> List[str]:
        """Get quality badges for a product."""
        badges = []
        
        # Quality grade badge
        if product.get('quality_grade') == 'A':
            badges.append('Premium Quality')
        
        # Pre-order badge
        if product.get('is_preorder'):
            badges.append('Pre-Order Available')
        
        # Fresh harvest badge (within 7 days)
        # This would check harvest_date
        
        # Verified seller badge
        # This would check seller history
        
        return badges
    
    # ========== DISTANCE CALCULATION ==========
    
    def calculate_distance(self, lat1: float, lon1: float, 
                          lat2: float, lon2: float) -> float:
        """Calculate distance between two coordinates in km (Haversine formula)."""
        R = 6371  # Earth radius in km
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = R * c
        return round(distance, 2)
    
    def get_products_with_distance(self, user_lat: float, user_lon: float,
                                   max_distance_km: Optional[float] = None,
                                   **filters) -> List[Dict]:
        """Get products with calculated distance from user location."""
        products = self.db.get_products(**filters)
        
        # Add distance to each product
        for product in products:
            location = product.get('location', {})
            product_lat = location.get('latitude', 0)
            product_lon = location.get('longitude', 0)
            
            if product_lat and product_lon:
                distance = self.calculate_distance(
                    user_lat, user_lon, product_lat, product_lon
                )
                product['distance_km'] = distance
            else:
                product['distance_km'] = None
        
        # Filter by max distance if specified
        if max_distance_km:
            products = [p for p in products 
                       if p.get('distance_km') is not None 
                       and p['distance_km'] <= max_distance_km]
        
        # Sort by distance (nearest first)
        products.sort(key=lambda x: x.get('distance_km') or float('inf'))
        
        return products
    
    # ========== PRODUCT VALIDATION ==========
    
    def validate_product_data(self, data: Dict) -> Dict:
        """Validate product data before saving."""
        errors = []
        
        # Required fields
        required = ['seller_name', 'seller_phone', 'commodity', 
                   'quantity_kg', 'price_per_kg', 'quality_grade']
        
        for field in required:
            if not data.get(field):
                errors.append(f'{field} is required')
        
        # Validate quantity
        if data.get('quantity_kg', 0) <= 0:
            errors.append('Quantity must be greater than 0')
        
        # Validate price
        if data.get('price_per_kg', 0) <= 0:
            errors.append('Price must be greater than 0')
        
        # Validate quality grade
        if data.get('quality_grade') not in ['A', 'B', 'C']:
            errors.append('Quality grade must be A, B, or C')
        
        # Validate phone number (basic)
        phone = data.get('seller_phone', '')
        if phone and not phone.startswith('08') and not phone.startswith('+62'):
            errors.append('Invalid phone number format')
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    # ========== PRE-ORDER LOGIC ==========
    
    def calculate_preorder_total(self, product_id: str, quantity_kg: float) -> Dict:
        """Calculate total for a pre-order."""
        product = self.db.get_product_by_id(product_id)
        
        if not product:
            return {
                'success': False,
                'message': 'Product not found'
            }
        
        if quantity_kg > product.get('quantity_kg', 0):
            return {
                'success': False,
                'message': 'Requested quantity exceeds available stock'
            }
        
        price_per_kg = product.get('price_per_kg', 0)
        total = quantity_kg * price_per_kg
        
        # Pre-order discount (5% for pre-orders)
        if product.get('is_preorder'):
            discount = total * 0.05
            final_total = total - discount
        else:
            discount = 0
            final_total = total
        
        return {
            'success': True,
            'quantity_kg': quantity_kg,
            'price_per_kg': price_per_kg,
            'subtotal': total,
            'discount': discount,
            'total': final_total,
            'discount_percentage': 5 if product.get('is_preorder') else 0
        }
    
    # ========== STATISTICS & ANALYTICS ==========
    
    def get_seller_statistics(self, seller_phone: str) -> Dict:
        """Get statistics for a specific seller."""
        all_products = self.db.get_products()
        seller_products = [p for p in all_products 
                          if p.get('seller_phone') == seller_phone]
        
        total_value = sum(p.get('total_price', 0) for p in seller_products)
        total_views = sum(p.get('views', 0) for p in seller_products)
        total_interests = sum(p.get('interests', 0) for p in seller_products)
        
        available = [p for p in seller_products if p.get('status') == 'available']
        sold = [p for p in seller_products if p.get('status') == 'sold']
        
        return {
            'total_products': len(seller_products),
            'available_products': len(available),
            'sold_products': len(sold),
            'total_value': total_value,
            'total_views': total_views,
            'total_interests': total_interests,
            'avg_price_per_kg': total_value / sum(p.get('quantity_kg', 1) 
                                                  for p in seller_products) if seller_products else 0
        }
