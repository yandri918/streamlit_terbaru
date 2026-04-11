"""Soil Test model for storing soil analysis data with location."""
from app import db
from datetime import datetime
import json


class SoilTest(db.Model):
    """Model for soil test results with geolocation."""
    
    __tablename__ = 'soil_tests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Location data
    location_name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    # Land area data (from polygon drawing)
    polygon_coordinates = db.Column(db.Text, nullable=True)  # JSON string
    area_sqm = db.Column(db.Float, nullable=True)  # Area in square meters
    area_ha = db.Column(db.Float, nullable=True)   # Area in hectares
    
    # Soil test data
    n_value = db.Column(db.Float, nullable=True)  # Nitrogen
    p_value = db.Column(db.Float, nullable=True)  # Phosphorus
    k_value = db.Column(db.Float, nullable=True)  # Potassium
    ph = db.Column(db.Float, nullable=True)
    
    # Environmental data
    temperature = db.Column(db.Float, nullable=True)
    humidity = db.Column(db.Float, nullable=True)
    moisture = db.Column(db.Float, nullable=True)  # Soil moisture
    
    # Additional info
    soil_type = db.Column(db.String(100), nullable=True)
    test_date = db.Column(db.Date, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='soil_tests', lazy=True)
    
    def get_polygon_coords(self):
        """Get polygon coordinates as Python object."""
        if self.polygon_coordinates:
            return json.loads(self.polygon_coordinates)
        return None
    
    def set_polygon_coords(self, coords):
        """Set polygon coordinates from Python object."""
        if coords:
            self.polygon_coordinates = json.dumps(coords)
        else:
            self.polygon_coordinates = None
    
    def to_dict(self):
        """Convert to dictionary for JSON response."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'location_name': self.location_name,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'polygon_coordinates': self.get_polygon_coords(),
            'area_sqm': self.area_sqm,
            'area_ha': self.area_ha,
            'n_value': self.n_value,
            'p_value': self.p_value,
            'k_value': self.k_value,
            'ph': self.ph,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'moisture': self.moisture,
            'soil_type': self.soil_type,
            'test_date': self.test_date.isoformat() if self.test_date else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<SoilTest {self.location_name} at ({self.latitude}, {self.longitude})>'
