"""Crop model for storing crop information and history."""
from datetime import datetime
from app import db


class Crop(db.Model):
    """Crop model for tracking crop cultivation."""
    
    __tablename__ = 'crops'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Crop information
    crop_name = db.Column(db.String(100), nullable=False)
    crop_variety = db.Column(db.String(100))
    crop_type = db.Column(db.String(50))  # vegetable, fruit, grain, etc.
    
    # Cultivation details
    planting_date = db.Column(db.Date)
    expected_harvest_date = db.Column(db.Date)
    actual_harvest_date = db.Column(db.Date)
    
    # Area information
    area_size = db.Column(db.Float)  # in hectares or square meters
    location = db.Column(db.String(100))
    
    # Yield information
    expected_yield = db.Column(db.Float)
    actual_yield = db.Column(db.Float)
    yield_unit = db.Column(db.String(20), default='kg')
    
    # Status
    status = db.Column(db.String(20), default='planning')  # planning, growing, harvested, failed
    
    # Additional data
    notes = db.Column(db.Text)
    extra_data = db.Column(db.JSON)  # Changed from 'metadata' to avoid SQLAlchemy conflict
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert crop to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'crop_name': self.crop_name,
            'crop_variety': self.crop_variety,
            'crop_type': self.crop_type,
            'planting_date': self.planting_date.isoformat() if self.planting_date else None,
            'expected_harvest_date': self.expected_harvest_date.isoformat() if self.expected_harvest_date else None,
            'actual_harvest_date': self.actual_harvest_date.isoformat() if self.actual_harvest_date else None,
            'area_size': self.area_size,
            'location': self.location,
            'expected_yield': self.expected_yield,
            'actual_yield': self.actual_yield,
            'yield_unit': self.yield_unit,
            'status': self.status,
            'notes': self.notes,
            'extra_data': self.extra_data,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Crop {self.crop_name} - {self.status}>'
