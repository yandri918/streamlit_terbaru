"""
Circular Economy Calculator
Agricultural waste valorization and biogas calculations
"""

class CircularEconomyCalculator:
    """Calculate waste valorization potential and biogas production"""
    
    # Agricultural waste valorization options
    WASTE_VALORIZATION = {
        'Jerami Padi': {
            'biochar': {'yield_pct': 30, 'value_per_kg': 2000},
            'kompos': {'yield_pct': 80, 'value_per_kg': 500},
            'pakan_ternak': {'yield_pct': 90, 'value_per_kg': 800},
            'briket': {'yield_pct': 40, 'value_per_kg': 1500}
        },
        'Tongkol Jagung': {
            'biochar': {'yield_pct': 35, 'value_per_kg': 2000},
            'briket': {'yield_pct': 45, 'value_per_kg': 1500},
            'xylitol': {'yield_pct': 10, 'value_per_kg': 50000},
            'pakan_ternak': {'yield_pct': 85, 'value_per_kg': 600}
        },
        'Kulit Kopi': {
            'cascara_tea': {'yield_pct': 90, 'value_per_kg': 15000},
            'kompos': {'yield_pct': 80, 'value_per_kg': 800},
            'pakan_ternak': {'yield_pct': 85, 'value_per_kg': 1000}
        },
        'Limbah Sawit': {
            'biogas': {'yield_m3_per_kg': 0.3, 'value_per_m3': 3000},
            'kompos': {'yield_pct': 70, 'value_per_kg': 600},
            'pupuk_organik': {'yield_pct': 75, 'value_per_kg': 800}
        },
        'Kotoran Ternak': {
            'biogas': {'yield_m3_per_kg': 0.25, 'value_per_m3': 3000},
            'kompos': {'yield_pct': 60, 'value_per_kg': 700},
            'pupuk_organik_cair': {'yield_pct': 40, 'value_per_kg': 1200}
        }
    }
    
    # Biogas potential (m³/kg organic matter)
    BIOGAS_POTENTIAL = {
        'Kotoran Sapi': 0.25,
        'Kotoran Ayam': 0.35,
        'Kotoran Babi': 0.40,
        'Limbah Sawit': 0.30,
        'Jerami Padi': 0.20,
        'Sampah Organik': 0.30
    }
    
    def calculate_waste_valorization(self, waste_type, waste_amount_kg, valorization_method):
        """Calculate value from waste valorization"""
        
        waste_options = self.WASTE_VALORIZATION.get(waste_type, {})
        method_data = waste_options.get(valorization_method, {})
        
        if not method_data:
            return {'error': 'Invalid waste type or method'}
        
        # Calculate output
        if 'yield_pct' in method_data:
            output_kg = waste_amount_kg * (method_data['yield_pct'] / 100)
            value = output_kg * method_data['value_per_kg']
            
            return {
                'waste_type': waste_type,
                'waste_amount_kg': waste_amount_kg,
                'method': valorization_method,
                'output_kg': round(output_kg, 2),
                'value': round(value, 0),
                'value_per_kg_waste': round(value / waste_amount_kg, 0) if waste_amount_kg > 0 else 0
            }
        elif 'yield_m3_per_kg' in method_data:
            # For biogas
            output_m3 = waste_amount_kg * method_data['yield_m3_per_kg']
            value = output_m3 * method_data['value_per_m3']
            
            return {
                'waste_type': waste_type,
                'waste_amount_kg': waste_amount_kg,
                'method': valorization_method,
                'output_m3': round(output_m3, 2),
                'value': round(value, 0),
                'kwh_equivalent': round(output_m3 * 2.5, 2)  # 1 m³ biogas ≈ 2.5 kWh
            }
    
    def calculate_biogas_potential(self, feedstock_type, daily_input_kg, digester_efficiency=0.7):
        """Calculate biogas production potential"""
        
        biogas_yield = self.BIOGAS_POTENTIAL.get(feedstock_type, 0.25)
        
        # Daily production
        daily_biogas_m3 = daily_input_kg * biogas_yield * digester_efficiency
        
        # Monthly and annual
        monthly_biogas_m3 = daily_biogas_m3 * 30
        annual_biogas_m3 = daily_biogas_m3 * 365
        
        # Energy equivalent (1 m³ biogas ≈ 2.5 kWh)
        daily_kwh = daily_biogas_m3 * 2.5
        monthly_kwh = monthly_biogas_m3 * 2.5
        annual_kwh = annual_biogas_m3 * 2.5
        
        # Economic value (Rp 1,500/kWh)
        kwh_price = 1500
        daily_value = daily_kwh * kwh_price
        monthly_value = monthly_kwh * kwh_price
        annual_value = annual_kwh * kwh_price
        
        # CO₂ reduction (1 m³ biogas replaces 0.6 kg LPG = 1.8 kg CO₂)
        annual_co2_reduction = annual_biogas_m3 * 1.8
        
        return {
            'feedstock': feedstock_type,
            'daily_input_kg': daily_input_kg,
            'daily_biogas_m3': round(daily_biogas_m3, 2),
            'monthly_biogas_m3': round(monthly_biogas_m3, 2),
            'annual_biogas_m3': round(annual_biogas_m3, 2),
            'daily_kwh': round(daily_kwh, 2),
            'monthly_kwh': round(monthly_kwh, 2),
            'annual_kwh': round(annual_kwh, 2),
            'monthly_value': round(monthly_value, 0),
            'annual_value': round(annual_value, 0),
            'co2_reduction_kg': round(annual_co2_reduction, 2)
        }
    
    def calculate_biogas_digester_roi(self, digester_size_m3, installation_cost, annual_biogas_value):
        """Calculate ROI for biogas digester investment"""
        
        # Operating costs (maintenance, labor)
        annual_operating_cost = installation_cost * 0.05  # 5% of CAPEX
        
        # Net annual benefit
        net_annual_benefit = annual_biogas_value - annual_operating_cost
        
        # Payback period
        if net_annual_benefit > 0:
            payback_years = installation_cost / net_annual_benefit
        else:
            payback_years = 999
        
        # NPV (10 year horizon, 10% discount rate)
        discount_rate = 0.10
        npv = -installation_cost
        for year in range(1, 11):
            npv += net_annual_benefit / ((1 + discount_rate) ** year)
        
        # IRR approximation
        if payback_years < 10:
            irr_pct = (net_annual_benefit / installation_cost) * 100
        else:
            irr_pct = 0
        
        return {
            'digester_size_m3': digester_size_m3,
            'installation_cost': round(installation_cost, 0),
            'annual_biogas_value': round(annual_biogas_value, 0),
            'annual_operating_cost': round(annual_operating_cost, 0),
            'net_annual_benefit': round(net_annual_benefit, 0),
            'payback_years': round(payback_years, 1),
            'npv_10_years': round(npv, 0),
            'irr_pct': round(irr_pct, 1)
        }
    
    def calculate_composting_time(self, material_type, c_n_ratio, moisture_pct, turning_frequency):
        """Estimate composting time"""
        
        # Base composting time (days)
        base_time = 60
        
        # C:N ratio adjustment (optimal: 25-30)
        if 25 <= c_n_ratio <= 30:
            cn_factor = 1.0
        elif c_n_ratio < 25:
            cn_factor = 1.2  # Too much N, slower
        else:
            cn_factor = 1.3  # Too much C, slower
        
        # Moisture adjustment (optimal: 50-60%)
        if 50 <= moisture_pct <= 60:
            moisture_factor = 1.0
        elif moisture_pct < 50:
            moisture_factor = 1.3  # Too dry
        else:
            moisture_factor = 1.2  # Too wet
        
        # Turning frequency adjustment
        turning_factors = {
            'daily': 0.7,
            'every_2_days': 0.8,
            'weekly': 1.0,
            'biweekly': 1.2,
            'monthly': 1.5
        }
        turning_factor = turning_factors.get(turning_frequency, 1.0)
        
        # Calculate total time
        total_time = base_time * cn_factor * moisture_factor * turning_factor
        
        return {
            'estimated_days': round(total_time, 0),
            'estimated_weeks': round(total_time / 7, 1),
            'optimal_cn_ratio': '25-30:1',
            'optimal_moisture': '50-60%',
            'recommendations': self._get_composting_recommendations(c_n_ratio, moisture_pct)
        }
    
    def _get_composting_recommendations(self, c_n_ratio, moisture_pct):
        """Get composting recommendations"""
        recs = []
        
        if c_n_ratio < 25:
            recs.append("C:N ratio terlalu rendah. Tambahkan bahan coklat (jerami, daun kering)")
        elif c_n_ratio > 30:
            recs.append("C:N ratio terlalu tinggi. Tambahkan bahan hijau (rumput, kotoran)")
        
        if moisture_pct < 50:
            recs.append("Terlalu kering. Tambahkan air atau bahan basah")
        elif moisture_pct > 60:
            recs.append("Terlalu basah. Tambahkan bahan kering atau aerasi lebih baik")
        
        return recs if recs else ["Kondisi optimal untuk composting!"]
