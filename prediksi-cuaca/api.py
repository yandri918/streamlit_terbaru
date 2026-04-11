"""
Weather Prediction FastAPI Application
RESTful API for weather forecasting and predictions
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import sys
import os

# Add utils to path
sys.path.append(os.path.dirname(__file__))

from utils.weather_api import (
    get_current_weather,
    get_hourly_forecast,
    get_daily_forecast,
    get_weather_description
)

# Initialize FastAPI app
app = FastAPI(
    title="Weather Prediction API",
    description="Advanced weather forecasting and prediction API with ML capabilities",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class LocationRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude (-90 to 90)")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude (-180 to 180)")

class CurrentWeatherResponse(BaseModel):
    location: Dict[str, float]
    timestamp: str
    temperature: float
    feels_like: float
    humidity: int
    pressure: float
    wind_speed: float
    wind_direction: int
    cloud_cover: int
    weather_code: int
    description: str
    timezone: str

class HourlyForecastResponse(BaseModel):
    location: Dict[str, float]
    forecast: List[Dict[str, Any]]
    hours: int

class DailyForecastResponse(BaseModel):
    location: Dict[str, float]
    forecast: List[Dict[str, Any]]
    days: int

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Weather Prediction API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "current": "/api/v1/weather/current",
            "hourly": "/api/v1/weather/hourly",
            "daily": "/api/v1/weather/daily",
            "docs": "/docs"
        }
    }

# Health check endpoint
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

# Current weather endpoint
@app.get("/api/v1/weather/current", response_model=CurrentWeatherResponse, tags=["Weather"])
async def get_current(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude")
):
    """
    Get current weather conditions for a location
    
    Parameters:
    - latitude: Latitude coordinate (-90 to 90)
    - longitude: Longitude coordinate (-180 to 180)
    
    Returns:
    - Current weather data including temperature, humidity, wind, etc.
    """
    try:
        weather = get_current_weather(latitude, longitude)
        
        if not weather:
            raise HTTPException(status_code=404, detail="Weather data not found")
        
        return {
            "location": {"latitude": latitude, "longitude": longitude},
            "timestamp": weather.get('time', datetime.utcnow().isoformat()),
            "temperature": weather.get('temperature', 0),
            "feels_like": weather.get('feels_like', 0),
            "humidity": weather.get('humidity', 0),
            "pressure": weather.get('pressure', 0),
            "wind_speed": weather.get('wind_speed', 0),
            "wind_direction": weather.get('wind_direction', 0),
            "cloud_cover": weather.get('cloud_cover', 0),
            "weather_code": weather.get('weather_code', 0),
            "description": get_weather_description(weather.get('weather_code', 0)),
            "timezone": weather.get('timezone', 'UTC')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching weather data: {str(e)}")

# Hourly forecast endpoint
@app.get("/api/v1/weather/hourly", response_model=HourlyForecastResponse, tags=["Weather"])
async def get_hourly(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude"),
    hours: int = Query(24, ge=1, le=168, description="Number of hours (1-168)")
):
    """
    Get hourly weather forecast
    
    Parameters:
    - latitude: Latitude coordinate
    - longitude: Longitude coordinate
    - hours: Number of forecast hours (default: 24, max: 168)
    
    Returns:
    - Hourly forecast data
    """
    try:
        forecast = get_hourly_forecast(latitude, longitude, hours)
        
        if forecast is None or len(forecast) == 0:
            raise HTTPException(status_code=404, detail="Forecast data not found")
        
        # Convert DataFrame to list of dicts
        forecast_list = forecast.to_dict('records')
        
        return {
            "location": {"latitude": latitude, "longitude": longitude},
            "forecast": forecast_list,
            "hours": len(forecast_list)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching forecast: {str(e)}")

# Daily forecast endpoint
@app.get("/api/v1/weather/daily", response_model=DailyForecastResponse, tags=["Weather"])
async def get_daily(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude"),
    days: int = Query(7, ge=1, le=16, description="Number of days (1-16)")
):
    """
    Get daily weather forecast
    
    Parameters:
    - latitude: Latitude coordinate
    - longitude: Longitude coordinate
    - days: Number of forecast days (default: 7, max: 16)
    
    Returns:
    - Daily forecast data
    """
    try:
        forecast = get_daily_forecast(latitude, longitude, days)
        
        if forecast is None or len(forecast) == 0:
            raise HTTPException(status_code=404, detail="Forecast data not found")
        
        # Convert DataFrame to list of dicts
        forecast_list = forecast.to_dict('records')
        
        return {
            "location": {"latitude": latitude, "longitude": longitude},
            "forecast": forecast_list,
            "days": len(forecast_list)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching forecast: {str(e)}")

# Prediction endpoint (for future ML integration)
@app.post("/api/v1/predict/temperature", tags=["Prediction"])
async def predict_temperature(location: LocationRequest):
    """
    Predict temperature using ML models (placeholder for future implementation)
    
    Parameters:
    - location: Location coordinates
    
    Returns:
    - Temperature prediction
    """
    return {
        "message": "ML prediction endpoint - Coming soon!",
        "location": location.dict(),
        "note": "This endpoint will use ARIMA, Prophet, LSTM, and XGBoost models"
    }

# Weather statistics endpoint
@app.get("/api/v1/weather/statistics", tags=["Statistics"])
async def get_statistics(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    days: int = Query(30, ge=7, le=365)
):
    """
    Get weather statistics for a location
    
    Parameters:
    - latitude: Latitude coordinate
    - longitude: Longitude coordinate
    - days: Number of days for statistics (default: 30, max: 365)
    
    Returns:
    - Weather statistics including averages, extremes, etc.
    """
    try:
        # Get historical data
        forecast = get_daily_forecast(latitude, longitude, min(days, 16))
        
        if forecast is None or len(forecast) == 0:
            raise HTTPException(status_code=404, detail="Data not found")
        
        # Calculate statistics
        stats = {
            "location": {"latitude": latitude, "longitude": longitude},
            "period_days": len(forecast),
            "temperature": {
                "mean": float(forecast['temperature_2m_mean'].mean()) if 'temperature_2m_mean' in forecast.columns else None,
                "min": float(forecast['temperature_2m_min'].min()) if 'temperature_2m_min' in forecast.columns else None,
                "max": float(forecast['temperature_2m_max'].max()) if 'temperature_2m_max' in forecast.columns else None,
            },
            "precipitation": {
                "total": float(forecast['precipitation_sum'].sum()) if 'precipitation_sum' in forecast.columns else None,
                "days_with_rain": int((forecast['precipitation_sum'] > 0).sum()) if 'precipitation_sum' in forecast.columns else None,
            }
        }
        
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating statistics: {str(e)}")

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
