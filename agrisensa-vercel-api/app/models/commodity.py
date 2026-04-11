"""Commodity model for dynamic data management."""
from datetime import datetime
from app import db


class Commodity(db.Model):
    """Model untuk menyimpan data komoditas pertanian."""
    
    __tablename__ = 'commodities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    name_local = db.Column(db.String(100))  # Nama lokal/daerah
    category = db.Column(db.String(50), nullable=False, index=True)  # sayuran, buah, pangan, rempah, dll
    subcategory = db.Column(db.String(50))  # daun, umbi, buah, dll
    
    # Unit & Measurement
    unit = db.Column(db.String(20), default='kg')  # kg, ikat, butir, ton
    
    # Cultivation Info
    optimal_ph_min = db.Column(db.Float)
    optimal_ph_max = db.Column(db.Float)
    optimal_temp_min = db.Column(db.Float)  # Celsius
    optimal_temp_max = db.Column(db.Float)
    optimal_altitude_min = db.Column(db.Integer)  # mdpl
    optimal_altitude_max = db.Column(db.Integer)
    water_need = db.Column(db.String(20))  # rendah, sedang, tinggi
    
    # Harvest Info
    days_to_harvest_min = db.Column(db.Integer)
    days_to_harvest_max = db.Column(db.Integer)
    yield_per_hectare_min = db.Column(db.Float)  # ton/ha
    yield_per_hectare_max = db.Column(db.Float)
    
    # Pricing Reference
    price_reference = db.Column(db.Float)  # Harga acuan per unit
    price_source = db.Column(db.String(50))  # bapanas, manual, crowdsource
    
    # Description & Guide
    description = db.Column(db.Text)
    cultivation_guide = db.Column(db.Text)
    
    # Metadata
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    image_url = db.Column(db.String(255))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    manual_prices = db.relationship('ManualPrice', backref='commodity', lazy='dynamic')
    
    def __repr__(self):
        return f'<Commodity {self.name}>'
    
    def to_dict(self):
        """Convert model to dictionary for API response."""
        return {
            'id': self.id,
            'name': self.name,
            'name_local': self.name_local,
            'category': self.category,
            'subcategory': self.subcategory,
            'unit': self.unit,
            'optimal_conditions': {
                'ph': {'min': self.optimal_ph_min, 'max': self.optimal_ph_max},
                'temperature': {'min': self.optimal_temp_min, 'max': self.optimal_temp_max},
                'altitude': {'min': self.optimal_altitude_min, 'max': self.optimal_altitude_max},
                'water_need': self.water_need
            },
            'harvest_info': {
                'days_to_harvest': {'min': self.days_to_harvest_min, 'max': self.days_to_harvest_max},
                'yield_per_hectare': {'min': self.yield_per_hectare_min, 'max': self.yield_per_hectare_max}
            },
            'price_reference': self.price_reference,
            'price_source': self.price_source,
            'description': self.description,
            'cultivation_guide': self.cultivation_guide,
            'is_active': self.is_active,
            'is_featured': self.is_featured,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_categories(cls):
        """Get distinct categories."""
        return db.session.query(cls.category).distinct().all()
    
    @classmethod
    def search(cls, query, category=None, active_only=True):
        """Search commodities by name or category."""
        filters = []
        if active_only:
            filters.append(cls.is_active == True)
        if category:
            filters.append(cls.category == category)
        if query:
            filters.append(
                db.or_(
                    cls.name.ilike(f'%{query}%'),
                    cls.name_local.ilike(f'%{query}%'),
                    cls.description.ilike(f'%{query}%')
                )
            )
        return cls.query.filter(*filters).order_by(cls.name).all()
