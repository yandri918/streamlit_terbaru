import numpy as np
from sklearn.ensemble import RandomForestRegressor
import streamlit as st

# ==========================================
# 🧠 AI ENGINE & LOGIC LAYER
# ==========================================

@st.cache_resource
def get_ai_model():
    """Train/Load the AI Model (Shared)."""
    np.random.seed(42)
    n_samples = 3000
    
    # Feature Engineering: 
    # 0: N, 1: P, 2: K, 3: pH, 4: Rain, 5: Temp, 
    # 6: Organic_Matter_Input (ton/ha), 7: Soil_Texture_Index (0-1), 8: Water_Access
    X = np.random.rand(n_samples, 9)
    
    # Scale to realistic agronomic ranges
    X[:, 0] = X[:, 0] * 350 + 20     # N: 20-370 kg/ha
    X[:, 1] = X[:, 1] * 120 + 10     # P: 10-130 kg/ha
    X[:, 2] = X[:, 2] * 250 + 20     # K: 20-270 kg/ha
    X[:, 3] = X[:, 3] * 4.5 + 4.0   # pH: 4.0-8.5
    X[:, 4] = X[:, 4] * 3500 + 500  # Rain: 500-4000 mm
    X[:, 5] = X[:, 5] * 20 + 15     # Temp: 15-35 C
    X[:, 6] = X[:, 6] * 20          # Organic Fert: 0-20 ton/ha
    X[:, 7] = X[:, 7]               # Soil Texture: 0-1
    X[:, 8] = X[:, 8]               # Water Access: 0-1

    # Complex Biological Yield Function
    def biological_yield_curve(n, p, k, ph, rain, temp, org, texture, water):
        # Optimal points (General baseline)
        opt_n, opt_p, opt_k = 200, 70, 150
        opt_ph, opt_rain, opt_temp = 6.5, 1800, 27
        
        # Stress factors
        stress_n = 1 - np.exp(-0.012 * n)
        stress_p = 1 - np.exp(-0.04 * p)
        stress_k = 1 - np.exp(-0.015 * k)
        
        # Bell curves
        stress_ph = np.exp(-0.5 * ((ph - opt_ph)/1.2)**2)
        stress_temp = np.exp(-0.5 * ((temp - opt_temp)/5.0)**2)
        
        # Water & Soil Interaction
        effective_water_retention = 0.5 + (0.5 * texture) 
        total_water = (rain * 0.4) + (water * 1000) 
        water_available = total_water * effective_water_retention
        stress_water = 1 - np.exp(-0.0015 * (water_available - 300))
        stress_water = np.clip(stress_water, 0, 1)

        # Organic Fertilizer Bonus
        som_bonus = 1 + (org * 0.015) 
        
        # Base Yield (kg/ha)
        base_yield = 12000 
        
        # Combined yield
        algo_yield = base_yield * (stress_n * stress_p * stress_k * stress_ph * stress_temp * stress_water) * som_bonus
        
        # Add random biological variability
        algo_yield += np.random.normal(0, 500, len(n) if isinstance(n, np.ndarray) else 1)
        
        return np.maximum(algo_yield, 0)

    y = biological_yield_curve(X[:,0], X[:,1], X[:,2], X[:,3], X[:,4], X[:,5], X[:,6], X[:,7], X[:,8])

    model = RandomForestRegressor(n_estimators=150, max_depth=14, random_state=42)
    model.fit(X, y)
    return model

def optimize_solution(model, target_yield, optimization_mode="Yield", fixed_params={}, price_per_kg=6000):
    """
    Finds the optimal agronomic inputs (SOP) to achieve target yield or max profit.
    Fixed params allow constraining weather/soil.
    """
    
    # Cost Assumptions (Global Standard)
    COST_N = 15000 
    COST_P = 20000 
    COST_K = 18000
    COST_ORG = 1000 # Rp 1000/kg
    
    # Pest Cost Logic
    p_strat = fixed_params.get('pest_strategy', "IPM (Terpadu)")
    
    # --- HARDCODED KNOWLEDGE BASE: PEST STRATEGIES ---
    PEST_STRATEGIES = {
        "Organic (Nabati)": {"cost_factor": 1.0, "risk_reduction": 0.3},
        "IPM (Terpadu)": {"cost_factor": 1.5, "risk_reduction": 0.6},
        "Konvensional": {"cost_factor": 2.5, "risk_reduction": 0.8},
        "Agresif (Intensif)": {"cost_factor": 4.0, "risk_reduction": 0.95}
    }
    
    pest_cost_base = 2000000 
    pest_cost_total = pest_cost_base * PEST_STRATEGIES.get(p_strat, {}).get('cost_factor', 1.5)

    best_conditions = None
    best_score = -float('inf')
    
    # Starting point based on weather input or default
    start_rain = fixed_params.get('rain', 2000.0)
    start_temp = fixed_params.get('temp', 27.0)
    
    current_cond = np.array([
        200.0, 60.0, 120.0, 6.5, start_rain, start_temp, 
        fixed_params.get('org_start', 2.0), 
        fixed_params.get('texture', 0.7), 
        0.8 
    ])
    
    iterations = 5   # We will do 5 steps of hill climbing
    batch_size = 50  # 50 mutations per step (total 250 evaluations)

    for i in range(iterations):
        # Generate batch_size mutations at once
        test_conds = np.tile(current_cond, (batch_size, 1))
        mutations = np.random.normal(0, [25, 10, 15, 0.1, 0, 0, 1.0, 0, 0], (batch_size, 9))
        test_conds += mutations
        
        # Clip values to realistic ranges
        test_conds = np.clip(test_conds, 
                             [0, 0, 0, 4, 500, 15, 0, 0, 0], 
                             [400, 150, 300, 8, 4000, 35, 20, 1, 1])
        
        # Enforce fixed constraints across the batch
        test_conds[:, 4] = start_rain
        test_conds[:, 5] = start_temp
        if 'fixed_org' in fixed_params:
             test_conds[:, 6] = fixed_params['fixed_org']
        test_conds[:, 7] = fixed_params.get('texture', 0.7)

        # Predict all yields for the batch at once (Extremely fast compared to single predictions)
        pred_yields = model.predict(test_conds)
        
        # Economic Calculation Vectorized
        revenues = pred_yields * price_per_kg
        chem_costs = (test_conds[:, 0] * COST_N) + (test_conds[:, 1] * COST_P) + (test_conds[:, 2] * COST_K)
        org_costs = (test_conds[:, 6] * 1000 * COST_ORG)
        total_variable_costs = chem_costs + org_costs + pest_cost_total
        
        profits = revenues - total_variable_costs
        
        if optimization_mode == "Profit":
            scores = profits
        else:
            diffs = np.abs(pred_yields - target_yield)
            scores = -diffs 
            
        best_idx = np.argmax(scores)
        if scores[best_idx] > best_score:
            best_score = scores[best_idx]
            best_conditions = test_conds[best_idx].copy()
            current_cond = test_conds[best_idx].copy() 
            
    final_yield = model.predict(best_conditions.reshape(1,-1))[0]
    
    # Return Dictionary for easier consumption
    return {
        "n_kg": best_conditions[0],
        "p_kg": best_conditions[1],
        "k_kg": best_conditions[2],
        "organic_ton": best_conditions[6],
        "predicted_yield": final_yield,
        "pest_cost": pest_cost_total
    }
