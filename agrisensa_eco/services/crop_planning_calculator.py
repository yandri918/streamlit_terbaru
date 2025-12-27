"""
Crop Planning Optimizer Service
Calculates optimal vegetable proportions based on farming system and goals (Personal vs Market).
"""

class CropPlanningCalculator:
    """
    Kalkulator Perencanaan Tanam Sayuran
    """
    
    # Database Tanaman (Yield & Market Data)
    VEGETABLE_DB = {
        # --- SAYURAN DAUN (LEAFY GREENS) ---
        'Selada (Lettuce)': {
            'type': 'leaf',
            'system_pref': ['hydroponic', 'mixed'],
            'harvest_days': 40,
            'yield_hydro_g_per_hole': 150, # gram
            'yield_soil_kg_m2': 1.5,
            'market_value': 'high', # Rp 20-30k/kg
            'personal_value': 'medium', # Salad
            'spacing_cm': 20
        },
        'Pakcoy': {
            'type': 'leaf',
            'system_pref': ['hydroponic', 'soil', 'mixed'],
            'harvest_days': 30,
            'yield_hydro_g_per_hole': 120,
            'yield_soil_kg_m2': 1.8,
            'market_value': 'medium', # Rp 10-15k/kg
            'personal_value': 'high', # Daily vegetable
            'spacing_cm': 15
        },
        'Bayam (Spinach)': {
            'type': 'leaf',
            'system_pref': ['soil', 'hydroponic', 'mixed'],
            'harvest_days': 25,
            'yield_hydro_g_per_hole': 100,
            'yield_soil_kg_m2': 1.2,
            'market_value': 'medium',
            'personal_value': 'high', # Iron source
            'spacing_cm': 10
        },
        'Kangkung': {
            'type': 'leaf',
            'system_pref': ['soil', 'hydroponic', 'mixed'],
            'harvest_days': 21, # Very fast
            'yield_hydro_g_per_hole': 100,
            'yield_soil_kg_m2': 2.0, # Can be harvested multiple times
            'market_value': 'low', # Volume game
            'personal_value': 'high',
            'spacing_cm': 10
        },
        'Kale': {
            'type': 'leaf',
            'system_pref': ['hydroponic', 'soil'],
            'harvest_days': 50,
            'yield_hydro_g_per_hole': 200,
            'yield_soil_kg_m2': 2.5,
            'market_value': 'premium', # Superfood price
            'personal_value': 'premium',
            'spacing_cm': 30
        },
        
        # --- SAYURAN BUAH (FRUITING VEG) ---
        'Cabai Rawit': {
            'type': 'fruit',
            'system_pref': ['soil', 'mixed', 'drip_hydro'],
            'harvest_days': 90,
            'yield_hydro_g_per_hole': 500, # Per cycle/plant
            'yield_soil_kg_m2': 0.8, # Planting density lower
            'market_value': 'volatile', # High risk high reward
            'personal_value': 'high', # Essential spice
            'spacing_cm': 50
        },
        'Tomat Cherry': {
            'type': 'fruit',
            'system_pref': ['hydroponic', 'greenhouse'],
            'harvest_days': 70,
            'yield_hydro_g_per_hole': 1000,
            'yield_soil_kg_m2': 3.0,
            'market_value': 'high',
            'personal_value': 'medium',
            'spacing_cm': 40
        },
        'Terung': {
            'type': 'fruit',
            'system_pref': ['soil'],
            'harvest_days': 60,
            'yield_hydro_g_per_hole': 800,
            'yield_soil_kg_m2': 2.5,
            'market_value': 'medium',
            'personal_value': 'medium',
            'spacing_cm': 60
        },
        'Timun': {
            'type': 'fruit',
            'system_pref': ['soil', 'drip_hydro'],
            'harvest_days': 40,
            'yield_hydro_g_per_hole': 1500,
            'yield_soil_kg_m2': 4.0,
            'market_value': 'medium',
            'personal_value': 'medium',
            'spacing_cm': 40
        }
    }

    def calculate_plan(self, inputs):
        """
        Generate planting plan.
        inputs = {
            'area_m2': 100,
            'system': 'soil' | 'hydroponic' | 'mixed',
            'goal': 'personal' | 'market',
            'selected_crops': ['Pakcoy', 'Selada', 'Cabai Rawit']
        }
        """
        area = inputs['area_m2'] or 1 # Avoid zero div
        system = inputs['system']
        goal = inputs['goal']
        selected = inputs.get('selected_crops', [])
        
        # If no crops selected, suggest default based on goal
        if not selected:
            if goal == 'personal':
                selected = ['Pakcoy', 'Kangkung', 'Cabai Rawit', 'Tomat Cherry']
            else:
                selected = ['Selada', 'Pakcoy', 'Kale'] # Commercial favorites
        
        # Determine Allocation Weights
        allocation = {}
        
        if goal == 'personal':
            # Balance: 50% Daily Greens, 30% Fruit/Spice, 20% Fancy/Salad
            for crop in selected:
                c_data = self.VEGETABLE_DB.get(crop, {})
                weight = 1
                if c_data.get('type') == 'leaf':
                    weight = 2 # Prioritize daily greens
                if c_data.get('personal_value') == 'high':
                    weight += 1
                allocation[crop] = weight
                
        elif goal == 'market':
            # Profit focus: 70% Fast Turnover/High Value, 30% Filler
            for crop in selected:
                c_data = self.VEGETABLE_DB.get(crop, {})
                weight = 1
                if c_data.get('market_value') in ['high', 'premium']:
                    weight = 3
                if c_data.get('harvest_days') < 40: # Fast turnover
                    weight += 1
                allocation[crop] = weight

        # Normalize Allocation to Percentage
        total_weight = sum(allocation.values())
        final_plan = {}
        
        for crop, weight in allocation.items():
            pct = (weight / total_weight) * 100
            
            c_data = self.VEGETABLE_DB.get(crop, {})
            harvest_days = c_data.get('harvest_days', 30)
            
            # Calculate Physical Capacity
            plant_count = 0
            yield_est_kg = 0
            space_alloc = 0
            
            if system == 'hydroponic':
                # Assume density based on spacing or fixed holes per meter pipe
                # Simple approximation: Hydro holes density ~ 20-30 holes/m2 for leafy
                # Fruit veg needs more space
                density = 25 if c_data.get('type') == 'leaf' else 4
                space_alloc = (area * (pct/100)) # m2 allocated
                plant_count = int(space_alloc * density)
                yield_est_kg = (plant_count * c_data.get('yield_hydro_g_per_hole', 100)) / 1000
                
            else: # soil / mixed
                space_alloc = (area * (pct/100))
                # Soil yield directly from kg/m2
                yield_est_kg = space_alloc * c_data.get('yield_soil_kg_m2', 1.0)
                # Plant count estimate based on spacing
                spacing_m = c_data.get('spacing_cm', 30) / 100
                plant_count = int(space_alloc / (spacing_m * spacing_m))

            final_plan[crop] = {
                'allocation_pct': round(pct, 1),
                'area_alloc_m2': round(space_alloc, 1),
                'plant_count': plant_count,
                'yield_est_kg': round(yield_est_kg, 1),
                'harvest_days': harvest_days,
                'type': c_data.get('type')
            }
            
        return {
            'system': system,
            'goal': goal,
            'total_area': area,
            'plan': final_plan,
            'total_yield_kg': sum(d['yield_est_kg'] for d in final_plan.values())
        }
