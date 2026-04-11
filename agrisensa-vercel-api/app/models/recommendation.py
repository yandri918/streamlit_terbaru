"""Recommendation model for storing fertilizer and crop recommendations."""
from datetime import datetime
from app import db


class Recommendation(db.Model):
    """Recommendation model for fertilizer and crop advice."""
    
    __tablename__ = 'recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Recommendation type
    recommendation_type = db.Column(db.String(50))  # fertilizer, crop, pest_control, etc.
    
    # Input parameters
    input_data = db.Column(db.JSON)
    
    # Recommendation results
    recommendation_data = db.Column(db.JSON)
    
    # Crop information
    crop_type = db.Column(db.String(50))
    crop_stage = db.Column(db.String(50))
    
    # Location
    location = db.Column(db.String(100))
    
    # Status
    status = db.Column(db.String(20), default='active')  # active, archived, implemented
    
    # User feedback
    rating = db.Column(db.Integer)  # 1-5 stars
    feedback = db.Column(db.Text)
    
    def to_dict(self):
        """Convert recommendation to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'recommendation_type': self.recommendation_type,
            'input_data': self.input_data,
            'recommendation_data': self.recommendation_data,
            'crop_type': self.crop_type,
            'crop_stage': self.crop_stage,
            'location': self.location,
            'status': self.status,
            'rating': self.rating,
            'feedback': self.feedback
        }
    
    def __repr__(self):
        return f'<Recommendation {self.recommendation_type} for {self.crop_type}>'
