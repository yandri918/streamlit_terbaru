"""Database models for AgriSensa Vercel API - Auth only."""
from app.models.user import User
from app.models.user_activity import UserActivity

__all__ = ['User', 'UserActivity']
