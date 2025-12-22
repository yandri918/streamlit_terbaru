"""NPK Reading model for storing soil nutrient data."""
from datetime import datetime
from app import db


class NpkReading(db.Model):
    """NPK Reading model for soil analysis."""
    
    __tablename__ = 'npk_readings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # NPK values
    n_value = db.Column(db.Integer, nullable=False)
    p_value = db.Column(db.Integer, nullable=False)
    k_value = db.Column(db.Integer, nullable=False)
    
    # Additional soil parameters
    ph_value = db.Column(db.Float)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    
    # Location information
    location = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Analysis results
    analysis_result = db.Column(db.JSON)
    
    def to_dict(self):
        """Convert NPK reading to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'n_value': self.n_value,
            'p_value': self.p_value,
            'k_value': self.k_value,
            'ph_value': self.ph_value,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'analysis_result': self.analysis_result
        }
    
    def __repr__(self):
        return f'<NpkReading N:{self.n_value} P:{self.p_value} K:{self.k_value}>'
