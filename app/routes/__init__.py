"""API routes/blueprints for AgriSensa API."""
from app.routes.main import main_bp
from app.routes.analysis import analysis_bp
from app.routes.recommendation import recommendation_bp
from app.routes.knowledge import knowledge_bp
from app.routes.market import market_bp
from app.routes.ml import ml_bp
from app.routes.auth import auth_bp
from app.routes.legacy import legacy_bp
from app.routes.diagnostik import diagnostic_bp
from app.routes.catalog import catalog_bp
from app.routes.pesticide import pesticide_bp
from app.routes.natural_pesticide import natural_pesticide_bp
from app.routes.soil_map import soil_map_bp
from app.routes.agrishop import agrishop_bp
from app.routes.harvest_routes import harvest_bp
from app.routes.admin import admin_bp

__all__ = [
    'main_bp',
    'analysis_bp',
    'recommendation_bp',
    'knowledge_bp',
    'market_bp',
    'ml_bp',
    'auth_bp',
    'legacy_bp',
    'diagnostic_bp',
    'catalog_bp',
    'pesticide_bp',
    'natural_pesticide_bp',
    'soil_map_bp',
    'agrishop_bp',
    'harvest_bp',
    'admin_bp'
]

