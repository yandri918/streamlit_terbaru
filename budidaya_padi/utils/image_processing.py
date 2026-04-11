"""
🍃 Leaf Color Chart (BWD) Analyzer
Utility to analyze leaf color from image and map to BWD scale (2-5)
"""

from PIL import Image
import numpy as np

def analyze_leaf_color(image_file):
    """
    Analyze uploaded leaf image and determine BWD scale
    
    Returns:
        dict: {
            'bwd_score': float (2.0 - 5.0),
            'bwd_class': str (Sangat Rendah/Rendah/Sedang/Tinggi),
            'dominant_color_hex': str,
            'confidence': str
        }
    """
    try:
        # Open image
        img = Image.open(image_file)
        img = img.convert('RGB')
        
        # Resize for faster processing and noise reduction
        img = img.resize((100, 100))
        
        # Get center crop (to avoid background noise)
        width, height = img.size
        left = width * 0.25
        top = height * 0.25
        right = width * 0.75
        bottom = height * 0.75
        img_crop = img.crop((left, top, right, bottom))
        
        # Convert to numpy array
        np_img = np.array(img_crop)
        
        # Calculate mean color
        mean_color = np_img.mean(axis=(0, 1))
        r, g, b = mean_color
        
        # Calculate Greenness Index (simple approximation for BWD)
        # BWD correlates strongly with Green intensity relative to others
        # Higher G relative to R+B indicates higher chlorophyll
        
        # Dark Green (High N) -> Low R, Low B, Medium G (but perceived dark)
        # Yellowish Green (Low N) -> High R, High G, Low B
        
        # Using Excess Green Index (ExG) = 2*G - R - B commonly used in aggrotech
        exg = 2*g - r - b
        
        # Mapping ExG to BWD Scale (Calibration required, these are estimated thresholds)
        # Ranges based on empirical observation of leaf colors
        bwd_score = 0
        bwd_class = ""
        
        if exg < 20: 
            bwd_score = 2.0
            bwd_class = "Sangat Rendah (BWD < 3)"
        elif exg < 40:
            bwd_score = 3.0
            bwd_class = "Rendah (BWD 3)"
        elif exg < 70:
            bwd_score = 4.0
            bwd_class = "Sedang (BWD 4)"
        else:
            bwd_score = 5.0
            bwd_class = "Tinggi (BWD > 4)"
            
        return {
            'bwd_score': bwd_score,
            'bwd_class': bwd_class,
            'dominant_color_rgb': (int(r), int(g), int(b)),
            'exg_index': float(exg),
            'status': 'success'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }
