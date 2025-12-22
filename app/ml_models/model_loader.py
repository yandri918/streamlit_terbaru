"""ML Model loader with lazy loading and caching."""
import os
import joblib
import threading
from flask import current_app


class ModelLoader:
    """Singleton class for loading and caching ML models."""
    
    _instance = None
    _lock = threading.Lock()
    _model_cache = {}
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def get_model(cls, model_name):
        """
        Get ML model with lazy loading and caching.
        
        Args:
            model_name: Name of the model to load
            
        Returns:
            Loaded model or None if not found
        """
        with cls._lock:
            # Return cached model if available
            if model_name in cls._model_cache:
                return cls._model_cache[model_name]
            
            # Get model path from config
            try:
                model_paths = current_app.config['MODEL_PATHS']
                ml_models_path = current_app.config['ML_MODELS_PATH']
            except:
                # Fallback if not in app context
                model_paths = {
                    'bwd': 'bwd_model.pkl',
                    'recommendation': 'recommendation_model.pkl',
                    'crop_recommendation': 'crop_recommendation_model.pkl',
                    'yield_prediction': 'yield_prediction_model.pkl',
                    'advanced_yield': 'advanced_yield_model.pkl',
                    'shap_explainer': 'shap_explainer.pkl'
                }
                ml_models_path = '.'
            
            if model_name not in model_paths:
                current_app.logger.warning(f"Model '{model_name}' not found in MODEL_PATHS")
                cls._model_cache[model_name] = None
                return None
            
            # Construct full path
            model_file = model_paths[model_name]
            full_path = os.path.join(ml_models_path, model_file)
            
            # Load model
            if os.path.exists(full_path):
                try:
                    cls._model_cache[model_name] = joblib.load(full_path)
                    current_app.logger.info(f"Model '{model_name}' loaded successfully")
                except Exception as e:
                    current_app.logger.error(f"Failed to load model '{model_name}': {e}")
                    cls._model_cache[model_name] = None
            else:
                current_app.logger.warning(f"Model file not found: {full_path}")
                cls._model_cache[model_name] = None
            
            return cls._model_cache[model_name]
    
    @classmethod
    def clear_cache(cls):
        """Clear all cached models."""
        with cls._lock:
            cls._model_cache.clear()
            current_app.logger.info("Model cache cleared")
