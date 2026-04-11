"""Manual Price model for commodity prices not covered by Bapanas API."""
from datetime import datetime, date
from app import db


class ManualPrice(db.Model):
    """Model untuk menyimpan harga manual komoditas."""
    
    __tablename__ = 'manual_prices'
    
    id = db.Column(db.Integer, primary_key=True)
    commodity_id = db.Column(db.Integer, db.ForeignKey('commodities.id'), nullable=False, index=True)
    
    # Location
    province_id = db.Column(db.Integer, index=True)  # Mengikuti mapping dari bapanas_constants
    province_name = db.Column(db.String(100))
    city_name = db.Column(db.String(100))  # Opsional, lebih spesifik
    
    # Price Data
    price = db.Column(db.Numeric(15, 2), nullable=False)
    price_type = db.Column(db.String(20), default='retail')  # retail, wholesale, farm_gate
    unit = db.Column(db.String(20), default='kg')
    
    # Date & Source
    price_date = db.Column(db.Date, nullable=False, default=date.today, index=True)
    source = db.Column(db.String(50), default='manual')  # manual, crowdsource, survey
    notes = db.Column(db.Text)
    
    # Reporter Info
    reported_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    reporter_name = db.Column(db.String(100))  # Untuk anonymous/crowdsource
    
    # Verification
    is_verified = db.Column(db.Boolean, default=False)
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    verified_at = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ManualPrice {self.commodity_id} @ {self.province_name}: {self.price}>'
    
    def to_dict(self):
        """Convert model to dictionary for API response."""
        return {
            'id': self.id,
            'commodity_id': self.commodity_id,
            'commodity_name': self.commodity.name if self.commodity else None,
            'location': {
                'province_id': self.province_id,
                'province_name': self.province_name,
                'city_name': self.city_name
            },
            'price': float(self.price) if self.price else None,
            'price_type': self.price_type,
            'unit': self.unit,
            'price_date': self.price_date.isoformat() if self.price_date else None,
            'source': self.source,
            'notes': self.notes,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def get_latest_price(cls, commodity_id, province_id=None):
        """Get the latest price for a commodity."""
        query = cls.query.filter(cls.commodity_id == commodity_id)
        if province_id:
            query = query.filter(cls.province_id == province_id)
        return query.order_by(cls.price_date.desc()).first()
    
    @classmethod
    def get_price_history(cls, commodity_id, province_id=None, days=30):
        """Get price history for a commodity."""
        from datetime import timedelta
        start_date = date.today() - timedelta(days=days)
        
        query = cls.query.filter(
            cls.commodity_id == commodity_id,
            cls.price_date >= start_date
        )
        if province_id:
            query = query.filter(cls.province_id == province_id)
            
        return query.order_by(cls.price_date.asc()).all()
    
    @classmethod
    def bulk_import(cls, data_list, user_id=None):
        """Bulk import prices from list of dictionaries."""
        prices = []
        for data in data_list:
            price = cls(
                commodity_id=data.get('commodity_id'),
                province_id=data.get('province_id'),
                province_name=data.get('province_name'),
                city_name=data.get('city_name'),
                price=data.get('price'),
                price_type=data.get('price_type', 'retail'),
                unit=data.get('unit', 'kg'),
                price_date=data.get('price_date', date.today()),
                source=data.get('source', 'bulk_import'),
                notes=data.get('notes'),
                reported_by=user_id
            )
            prices.append(price)
        
        db.session.bulk_save_objects(prices)
        db.session.commit()
        return len(prices)
