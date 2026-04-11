"""
Moon phase calculation utilities
"""
import math
from datetime import datetime

def calculate_moon_phase(date=None):
    """
    Calculate moon phase for a given date
    
    Args:
        date: datetime object (default: current date)
    
    Returns:
        Dictionary with moon phase information
    """
    if date is None:
        date = datetime.now()
    
    # Calculate days since known new moon (January 6, 2000)
    known_new_moon = datetime(2000, 1, 6, 18, 14)
    days_diff = (date - known_new_moon).total_seconds() / 86400
    
    # Lunar cycle is approximately 29.53 days
    lunar_cycle = 29.53058867
    
    # Calculate phase
    phase = (days_diff % lunar_cycle) / lunar_cycle
    
    # Determine phase name and emoji
    if phase < 0.0625:
        phase_name = "New Moon"
        emoji = "🌑"
        illumination = 0
    elif phase < 0.1875:
        phase_name = "Waxing Crescent"
        emoji = "🌒"
        illumination = 25
    elif phase < 0.3125:
        phase_name = "First Quarter"
        emoji = "🌓"
        illumination = 50
    elif phase < 0.4375:
        phase_name = "Waxing Gibbous"
        emoji = "🌔"
        illumination = 75
    elif phase < 0.5625:
        phase_name = "Full Moon"
        emoji = "🌕"
        illumination = 100
    elif phase < 0.6875:
        phase_name = "Waning Gibbous"
        emoji = "🌖"
        illumination = 75
    elif phase < 0.8125:
        phase_name = "Last Quarter"
        emoji = "🌗"
        illumination = 50
    elif phase < 0.9375:
        phase_name = "Waning Crescent"
        emoji = "🌘"
        illumination = 25
    else:
        phase_name = "New Moon"
        emoji = "🌑"
        illumination = 0
    
    return {
        "phase_name": phase_name,
        "emoji": emoji,
        "illumination": illumination,
        "phase_percentage": phase * 100,
        "age_days": days_diff % lunar_cycle
    }
