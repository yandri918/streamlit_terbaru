"""
Soil Adjustment Service
Provides functions to adjust fertilizer recommendations based on soil test results
"""

def adjust_npk_for_soil_test(base_n, base_p, base_k, soil_n=0, soil_p=0, soil_k=0):
    """
    Adjust NPK requirements based on soil test results.
    
    Parameters:
    - base_n, base_p, base_k: Base NPK requirements (kg)
    - soil_n, soil_p, soil_k: Current soil NPK levels (ppm)
    
    Returns:
    - adjusted_n, adjusted_p, adjusted_k: Adjusted NPK requirements (kg)
    - reduction_n, reduction_p, reduction_k: Reduction percentages
    """
    
    # Soil nutrient level categories (ppm)
    # Based on standard soil test interpretation
    NUTRIENT_LEVELS = {
        'N': {'very_low': 20, 'low': 40, 'medium': 60, 'high': 100, 'very_high': 150},
        'P': {'very_low': 10, 'low': 20, 'medium': 30, 'high': 50, 'very_high': 80},
        'K': {'very_low': 50, 'low': 100, 'medium': 150, 'high': 250, 'very_high': 400}
    }
    
    def get_reduction_factor(nutrient_level, nutrient_type):
        """Calculate reduction factor based on soil nutrient level"""
        levels = NUTRIENT_LEVELS[nutrient_type]
        
        if nutrient_level == 0:  # No data
            return 0.0  # No reduction
        elif nutrient_level < levels['very_low']:
            return 0.0  # Very low - no reduction
        elif nutrient_level < levels['low']:
            return 0.10  # Low - 10% reduction
        elif nutrient_level < levels['medium']:
            return 0.20  # Medium - 20% reduction
        elif nutrient_level < levels['high']:
            return 0.30  # High - 30% reduction
        elif nutrient_level < levels['very_high']:
            return 0.40  # Very high - 40% reduction
        else:
            return 0.50  # Excessive - 50% reduction
    
    # Calculate reduction factors
    reduction_n = get_reduction_factor(soil_n, 'N')
    reduction_p = get_reduction_factor(soil_p, 'P')
    reduction_k = get_reduction_factor(soil_k, 'K')
    
    # Apply reductions
    adjusted_n = base_n * (1 - reduction_n)
    adjusted_p = base_p * (1 - reduction_p)
    adjusted_k = base_k * (1 - reduction_k)
    
    return adjusted_n, adjusted_p, adjusted_k, reduction_n, reduction_p, reduction_k


def get_soil_status_message(soil_n, soil_p, soil_k, soil_ph):
    """Generate soil status message and recommendations"""
    messages = []
    
    # NPK Status
    if soil_n > 0 or soil_p > 0 or soil_k > 0:
        messages.append("**📊 Status Hara Tanah:**")
        
        if soil_n > 0:
            if soil_n < 40:
                messages.append(f"- N: {soil_n} ppm (Rendah) - Perlu pemupukan N penuh")
            elif soil_n < 100:
                messages.append(f"- N: {soil_n} ppm (Sedang) - Pemupukan N dikurangi 20-30%")
            else:
                messages.append(f"- N: {soil_n} ppm (Tinggi) - Pemupukan N dikurangi 40-50%")
        
        if soil_p > 0:
            if soil_p < 20:
                messages.append(f"- P: {soil_p} ppm (Rendah) - Perlu pemupukan P penuh")
            elif soil_p < 50:
                messages.append(f"- P: {soil_p} ppm (Sedang) - Pemupukan P dikurangi 20-30%")
            else:
                messages.append(f"- P: {soil_p} ppm (Tinggi) - Pemupukan P dikurangi 40-50%")
        
        if soil_k > 0:
            if soil_k < 100:
                messages.append(f"- K: {soil_k} ppm (Rendah) - Perlu pemupukan K penuh")
            elif soil_k < 250:
                messages.append(f"- K: {soil_k} ppm (Sedang) - Pemupukan K dikurangi 20-30%")
            else:
                messages.append(f"- K: {soil_k} ppm (Tinggi) - Pemupukan K dikurangi 40-50%")
    
    # pH Status
    if soil_ph > 0:
        messages.append("\n**🧪 Status pH Tanah:**")
        if soil_ph < 5.5:
            messages.append(f"- pH {soil_ph:.1f} (Sangat Masam) - Perlu pengapuran 1-2 ton/ha")
        elif soil_ph < 6.0:
            messages.append(f"- pH {soil_ph:.1f} (Masam) - Pertimbangkan pengapuran 0.5-1 ton/ha")
        elif soil_ph <= 7.0:
            messages.append(f"- pH {soil_ph:.1f} (Ideal) - Tidak perlu pengapuran")
        elif soil_ph <= 7.5:
            messages.append(f"- pH {soil_ph:.1f} (Sedikit Basa) - Monitor pH secara berkala")
        else:
            messages.append(f"- pH {soil_ph:.1f} (Basa) - Perlu penurunan pH dengan sulfur/pupuk asam")
    
    return "\n".join(messages) if messages else None


def get_nutrient_status(nutrient_value, nutrient_type):
    """
    Get status category for a nutrient
    
    Parameters:
    - nutrient_value: Nutrient level in ppm
    - nutrient_type: 'N', 'P', or 'K'
    
    Returns:
    - status: 'very_low', 'low', 'medium', 'high', 'very_high', or 'no_data'
    """
    NUTRIENT_LEVELS = {
        'N': {'very_low': 20, 'low': 40, 'medium': 60, 'high': 100, 'very_high': 150},
        'P': {'very_low': 10, 'low': 20, 'medium': 30, 'high': 50, 'very_high': 80},
        'K': {'very_low': 50, 'low': 100, 'medium': 150, 'high': 250, 'very_high': 400}
    }
    
    if nutrient_value == 0:
        return 'no_data'
    
    levels = NUTRIENT_LEVELS[nutrient_type]
    
    if nutrient_value < levels['very_low']:
        return 'very_low'
    elif nutrient_value < levels['low']:
        return 'low'
    elif nutrient_value < levels['medium']:
        return 'medium'
    elif nutrient_value < levels['high']:
        return 'high'
    elif nutrient_value < levels['very_high']:
        return 'very_high'
    else:
        return 'excessive'


def get_ph_status(ph_value):
    """
    Get pH status category
    
    Parameters:
    - ph_value: pH measurement
    
    Returns:
    - status: 'very_acidic', 'acidic', 'ideal', 'slightly_alkaline', 'alkaline', or 'no_data'
    """
    if ph_value == 0:
        return 'no_data'
    elif ph_value < 5.5:
        return 'very_acidic'
    elif ph_value < 6.0:
        return 'acidic'
    elif ph_value <= 7.0:
        return 'ideal'
    elif ph_value <= 7.5:
        return 'slightly_alkaline'
    else:
        return 'alkaline'
