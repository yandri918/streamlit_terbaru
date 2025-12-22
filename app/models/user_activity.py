"""User Activity Log model for tracking user actions."""
from datetime import datetime
from app import db


class UserActivity(db.Model):
    """Model for logging user activities across all sessions."""
    
    __tablename__ = 'user_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    username = db.Column(db.String(80), nullable=False, index=True)
    action = db.Column(db.String(50), nullable=False, index=True)  # LOGIN, LOGOUT, LOGIN_FAILED, REGISTER
    details = db.Column(db.String(255))
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'action': self.action,
            'details': self.details,
            'ip_address': self.ip_address,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
    
    @classmethod
    def log_activity(cls, username, action, details=None, user_id=None, ip_address=None, user_agent=None):
        """Log a user activity."""
        activity = cls(
            username=username,
            action=action,
            details=details,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.session.add(activity)
        db.session.commit()
        return activity
    
    @classmethod
    def get_recent_activities(cls, limit=100):
        """Get recent activities."""
        return cls.query.order_by(cls.timestamp.desc()).limit(limit).all()
    
    @classmethod
    def get_user_activities(cls, username, limit=50):
        """Get activities for a specific user."""
        return cls.query.filter_by(username=username).order_by(cls.timestamp.desc()).limit(limit).all()
    
    def __repr__(self):
        return f'<UserActivity {self.username}:{self.action}>'
