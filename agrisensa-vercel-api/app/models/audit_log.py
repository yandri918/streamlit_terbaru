"""Admin Audit Log model for tracking all admin actions."""
from datetime import datetime
from app import db


class AdminAuditLog(db.Model):
    """Model untuk mencatat semua aksi admin (audit trail)."""
    
    __tablename__ = 'admin_audit_log'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # User Info
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    username = db.Column(db.String(100))  # Denormalized for quick lookup
    
    # Action Details
    action = db.Column(db.String(50), nullable=False, index=True)  # CREATE, UPDATE, DELETE, LOGIN, EXPORT
    table_name = db.Column(db.String(100), index=True)  # commodities, manual_prices, users
    record_id = db.Column(db.Integer)  # ID of affected record
    
    # Change Data (stored as JSON)
    old_values = db.Column(db.JSON)  # Previous values (for UPDATE/DELETE)
    new_values = db.Column(db.JSON)  # New values (for CREATE/UPDATE)
    
    # Request Context
    ip_address = db.Column(db.String(45))  # IPv4 or IPv6
    user_agent = db.Column(db.String(255))
    endpoint = db.Column(db.String(255))  # API endpoint called
    
    # Additional Info
    notes = db.Column(db.Text)  # Optional description
    status = db.Column(db.String(20), default='success')  # success, failed, pending
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationship
    user = db.relationship('User', backref='audit_logs')
    
    def __repr__(self):
        return f'<AuditLog {self.action} on {self.table_name} by {self.username}>'
    
    def to_dict(self):
        """Convert model to dictionary for API response."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'action': self.action,
            'table_name': self.table_name,
            'record_id': self.record_id,
            'old_values': self.old_values,
            'new_values': self.new_values,
            'ip_address': self.ip_address,
            'endpoint': self.endpoint,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def log_action(cls, user_id, username, action, table_name=None, record_id=None,
                   old_values=None, new_values=None, ip_address=None, 
                   user_agent=None, endpoint=None, notes=None, status='success'):
        """Create a new audit log entry."""
        log = cls(
            user_id=user_id,
            username=username,
            action=action,
            table_name=table_name,
            record_id=record_id,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent,
            endpoint=endpoint,
            notes=notes,
            status=status
        )
        db.session.add(log)
        db.session.commit()
        return log
    
    @classmethod
    def get_user_activity(cls, user_id, limit=50):
        """Get recent activity for a specific user."""
        return cls.query.filter(cls.user_id == user_id)\
                       .order_by(cls.created_at.desc())\
                       .limit(limit).all()
    
    @classmethod
    def get_table_history(cls, table_name, record_id=None, limit=50):
        """Get audit history for a specific table or record."""
        query = cls.query.filter(cls.table_name == table_name)
        if record_id:
            query = query.filter(cls.record_id == record_id)
        return query.order_by(cls.created_at.desc()).limit(limit).all()
    
    @classmethod
    def get_recent_activity(cls, limit=100):
        """Get most recent admin activity."""
        return cls.query.order_by(cls.created_at.desc()).limit(limit).all()
    
    @classmethod
    def get_activity_summary(cls, days=7):
        """Get activity summary for dashboard."""
        from datetime import timedelta
        from sqlalchemy import func
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        results = db.session.query(
            cls.action,
            func.count(cls.id).label('count')
        ).filter(
            cls.created_at >= start_date
        ).group_by(cls.action).all()
        
        return {action: count for action, count in results}
