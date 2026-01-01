"""
Microbe & Biofertilizer Production Service
Handles calculations for production cost, CFU counting, ROI analysis, and application rates
"""

class MicrobeProductionService:
    """Service for microbe production calculations and data"""
    
    # Production cost database (per liter/kg)
    COST_DATABASE = {
        'ROTAN_Bioactivator': {
            'raw_materials': {
                'Cairan Rumen Sapi': {'qty': 2, 'unit': 'L', 'price': 5000},
                'Molase': {'qty': 2, 'unit': 'L', 'price': 15000},
                'Dedak': {'qty': 1, 'unit': 'kg', 'price': 3000},
                'Urine Ternak': {'qty': 4, 'unit': 'L', 'price': 2000},
                'Ragi Tape': {'qty': 3, 'unit': 'butir', 'price': 1000},
                'Terasi': {'qty': 0.1, 'unit': 'kg', 'price': 30000},
                'Nanas': {'qty': 1, 'unit': 'buah', 'price': 10000}
            },
            'output_volume': 12,  # Liter
            'fermentation_days': 14
        },
        'POC_ROTAN_Premium': {
            'raw_materials': {
                'Pisang': {'qty': 5, 'unit': 'buah', 'price': 3000},
                'Pepaya': {'qty': 1, 'unit': 'buah', 'price': 10000},
                'Nanas': {'qty': 1, 'unit': 'buah', 'price': 10000},
                'Mangga': {'qty': 2, 'unit': 'buah', 'price': 5000},
                'Melon': {'qty': 1, 'unit': 'buah', 'price': 15000},
                'Kangkung': {'qty': 3, 'unit': 'ikat', 'price': 2000},
                'Kacang Panjang': {'qty': 3, 'unit': 'ikat', 'price': 3000},
                'Jagung Muda': {'qty': 2, 'unit': 'buah', 'price': 5000},
                'Air Kelapa': {'qty': 5, 'unit': 'L', 'price': 5000},
                'Gula Kelapa': {'qty': 1, 'unit': 'kg', 'price': 20000},
                'Usus Ikan': {'qty': 0.2, 'unit': 'kg', 'price': 15000}
            },
            'output_volume': 15,  # Liter
            'fermentation_days': 12
        },
        'POC_Rumen_Kambing': {
            'raw_materials': {
                'Air Bersih': {'qty': 5, 'unit': 'L', 'price': 0},
                'Gula Kelapa': {'qty': 1, 'unit': 'kg', 'price': 20000},
                'Kecambah (Tauge)': {'qty': 1, 'unit': 'kg', 'price': 8000},
                'Dedak': {'qty': 2, 'unit': 'kg', 'price': 3000},
                'Susu Murni': {'qty': 1, 'unit': 'L', 'price': 15000},
                'Rumen Kambing': {'qty': 0.3, 'unit': 'kg', 'price': 5000}
            },
            'output_volume': 7,
            'fermentation_days': 5
        },
        'POC_Urine_Kelinci': {
            'raw_materials': {
                'Urine Kelinci': {'qty': 10, 'unit': 'L', 'price': 3000},
                'EM4/MOL': {'qty': 0.2, 'unit': 'L', 'price': 25000},
                'Molase': {'qty': 0.2, 'unit': 'L', 'price': 15000},
                'Air Kelapa': {'qty': 1, 'unit': 'L', 'price': 5000}
            },
            'output_volume': 11,
            'fermentation_days': 10
        },
        'MOL_Sayuran': {
            'raw_materials': {
                'Sayuran Beragam': {'qty': 3, 'unit': 'kg', 'price': 5000},
                'Gula Merah': {'qty': 0.5, 'unit': 'kg', 'price': 15000},
                'Garam': {'qty': 0.15, 'unit': 'kg', 'price': 5000},
                'Air Leri': {'qty': 3, 'unit': 'L', 'price': 0},
                'Air Kelapa': {'qty': 2, 'unit': 'L', 'price': 5000}
            },
            'output_volume': 5,
            'fermentation_days': 14
        },
        'MOL_Buah': {
            'raw_materials': {
                'Buah Matang': {'qty': 2, 'unit': 'kg', 'price': 8000},
                'Gula Merah': {'qty': 0.5, 'unit': 'kg', 'price': 15000},
                'Air Kelapa': {'qty': 5, 'unit': 'L', 'price': 5000}
            },
            'output_volume': 6,
            'fermentation_days': 14
        },
        'MOL_Rebung_Bambu': {
            'raw_materials': {
                'Rebung Bambu': {'qty': 1, 'unit': 'kg', 'price': 10000},
                'Air Leri': {'qty': 5, 'unit': 'L', 'price': 0},
                'Gula Merah': {'qty': 0.5, 'unit': 'kg', 'price': 15000}
            },
            'output_volume': 5,
            'fermentation_days': 15
        },
        'MOL_Bonggol_Pisang': {
            'raw_materials': {
                'Bonggol Pisang': {'qty': 1, 'unit': 'kg', 'price': 2000},
                'Gula Merah': {'qty': 0.05, 'unit': 'kg', 'price': 15000},
                'Air Leri': {'qty': 5, 'unit': 'L', 'price': 0}
            },
            'output_volume': 5,
            'fermentation_days': 14
        },
        'MOL_Keong_Mas': {
            'raw_materials': {
                'Keong Mas Hidup': {'qty': 1, 'unit': 'kg', 'price': 5000},
                'Buah Maja': {'qty': 0.5, 'unit': 'buah', 'price': 10000},
                'Air Kelapa': {'qty': 5, 'unit': 'L', 'price': 5000}
            },
            'output_volume': 5,
            'fermentation_days': 15
        },
        'Trichoderma': {
            'raw_materials': {
                'Rice Bran (Dedak)': {'qty': 1.4, 'unit': 'kg', 'price': 3000},
                'Corn Meal': {'qty': 0.4, 'unit': 'kg', 'price': 5000},
                'Sawdust': {'qty': 0.2, 'unit': 'kg', 'price': 1000},
                'Starter Culture': {'qty': 0.1, 'unit': 'L', 'price': 50000}
            },
            'output_volume': 2,  # kg (solid)
            'fermentation_days': 10
        },
        'Beauveria_bassiana': {
            'raw_materials': {
                'Beras Putih': {'qty': 1, 'unit': 'kg', 'price': 12000},
                'Air': {'qty': 1.2, 'unit': 'L', 'price': 0},
                'Starter Culture': {'qty': 0.05, 'unit': 'L', 'price': 75000}
            },
            'output_volume': 1.5,  # kg
            'fermentation_days': 18
        },
        'Metarhizium_anisopliae': {
            'raw_materials': {
                'Beras/Jagung': {'qty': 1, 'unit': 'kg', 'price': 12000},
                'Air': {'qty': 1.2, 'unit': 'L', 'price': 0},
                'Starter Culture': {'qty': 0.05, 'unit': 'L', 'price': 75000}
            },
            'output_volume': 1.5,  # kg
            'fermentation_days': 20
        },
        'PGPR_Liquid': {
            'raw_materials': {
                'Nutrient Broth': {'qty': 0.5, 'unit': 'kg', 'price': 100000},
                'Yeast Extract': {'qty': 0.1, 'unit': 'kg', 'price': 150000},
                'Starter Culture': {'qty': 0.1, 'unit': 'L', 'price': 75000}
            },
            'output_volume': 5,  # L (liquid)
            'fermentation_days': 3
        },
        'PGPR_Carrier': {
            'raw_materials': {
                'Nutrient Broth': {'qty': 0.5, 'unit': 'kg', 'price': 100000},
                'Carrier (Peat/Biochar)': {'qty': 1, 'unit': 'kg', 'price': 10000},
                'Starter Culture': {'qty': 0.1, 'unit': 'L', 'price': 75000}
            },
            'output_volume': 2,  # kg
            'fermentation_days': 7
        },
        'Azotobacter': {
            'raw_materials': {
                'Ashby Medium': {'qty': 0.3, 'unit': 'kg', 'price': 120000},
                'Molase': {'qty': 0.5, 'unit': 'L', 'price': 15000},
                'Carrier (Peat)': {'qty': 1, 'unit': 'kg', 'price': 10000},
                'Starter Culture': {'qty': 0.1, 'unit': 'L', 'price': 60000}
            },
            'output_volume': 2,  # kg
            'fermentation_days': 5
        },
        # Amino Acid Products
        'Fish_Amino_Acid': {
            'raw_materials': {
                'Ikan Segar/Sisa Ikan': {'qty': 1, 'unit': 'kg', 'price': 10000},
                'Gula Merah/Molase': {'qty': 1, 'unit': 'kg', 'price': 15000},
                'Nanas (opsional)': {'qty': 0.5, 'unit': 'buah', 'price': 10000},
                'EM4': {'qty': 0.05, 'unit': 'L', 'price': 25000}
            },
            'output_volume': 1.5,  # L (setelah disaring)
            'fermentation_days': 14
        },
        'Keong_Mas_Amino': {
            'raw_materials': {
                'Keong Mas Hidup': {'qty': 1, 'unit': 'kg', 'price': 5000},
                'Gula Merah': {'qty': 0.5, 'unit': 'kg', 'price': 15000},
                'Air Kelapa': {'qty': 2, 'unit': 'L', 'price': 5000},
                'Buah Maja': {'qty': 0.5, 'unit': 'buah', 'price': 10000}
            },
            'output_volume': 2,  # L
            'fermentation_days': 15
        },
        'Plant_Amino_Soybean': {
            'raw_materials': {
                'Kedelai/Kacang Hijau': {'qty': 2, 'unit': 'kg', 'price': 12000},
                'Gula Merah': {'qty': 1, 'unit': 'kg', 'price': 15000},
                'Air Leri': {'qty': 5, 'unit': 'L', 'price': 0},
                'Ragi Tempe': {'qty': 2, 'unit': 'bungkus', 'price': 2000},
                'EM4': {'qty': 0.1, 'unit': 'L', 'price': 25000}
            },
            'output_volume': 5,  # L
            'fermentation_days': 14
        },
        # Growth Booster Products
        'Seaweed_Extract': {
            'raw_materials': {
                'Rumput Laut Segar': {'qty': 2, 'unit': 'kg', 'price': 8000},
                'Molase': {'qty': 0.5, 'unit': 'kg', 'price': 15000},
                'EM4': {'qty': 0.1, 'unit': 'L', 'price': 25000}
            },
            'output_volume': 8,  # L (setelah disaring)
            'fermentation_days': 14
        },
        'Humic_Acid_Extract': {
            'raw_materials': {
                'Kascing/Vermicompost': {'qty': 5, 'unit': 'kg', 'price': 5000},
                'KOH/NaOH': {'qty': 0.05, 'unit': 'kg', 'price': 20000},
                'Air Bersih': {'qty': 20, 'unit': 'L', 'price': 0}
            },
            'output_volume': 15,  # L (ekstrak)
            'fermentation_days': 2
        },
        'Moringa_Extract': {
            'raw_materials': {
                'Daun Kelor Segar': {'qty': 1, 'unit': 'kg', 'price': 5000},
                'Air Bersih': {'qty': 5, 'unit': 'L', 'price': 0},
                'Molase (opsional)': {'qty': 0.1, 'unit': 'kg', 'price': 15000},
                'EM4 (opsional)': {'qty': 0.05, 'unit': 'L', 'price': 25000}
            },
            'output_volume': 4,  # L
            'fermentation_days': 7
        },
        'Chitosan_Solution': {
            'raw_materials': {
                'Cangkang Udang/Kepiting': {'qty': 1, 'unit': 'kg', 'price': 5000},
                'HCl 5%': {'qty': 2, 'unit': 'L', 'price': 15000},
                'NaOH 40%': {'qty': 2, 'unit': 'L', 'price': 20000},
                'Asam Asetat 1%': {'qty': 1, 'unit': 'L', 'price': 5000}
            },
            'output_volume': 1,  # L (solution 0.1%)
            'fermentation_days': 3
        }
    }
    
    # Equipment investment by scale
    EQUIPMENT_COST = {
        'Small': {
            'Fermentor': 5000000,
            'Incubator': 3000000,
            'Autoclave': 10000000,
            'Microscope': 5000000,
            'Lab Equipment': 7000000,
            'Total': 30000000
        },
        'Medium': {
            'Fermentor': 25000000,
            'Incubator': 15000000,
            'Autoclave': 30000000,
            'Microscope': 15000000,
            'Lab Equipment': 20000000,
            'Total': 105000000
        },
        'Large': {
            'Fermentor': 150000000,
            'Incubator': 50000000,
            'Autoclave': 100000000,
            'Microscope': 50000000,
            'Lab Equipment': 50000000,
            'Total': 400000000
        }
    }
    
    # Application rates (per crop type)
    APPLICATION_RATES = {
        'Rice': {
            'ROTAN': '250 ml/14L',
            'MOL': '250 ml/14L',
            'PGPR': '500 ml/ha',
            'Trichoderma': '20 g/plant',
            'Beauveria': '2 ml/L',
            'Azotobacter': '1 L/ha'
        },
        'Vegetables': {
            'ROTAN': '100 ml/14L',
            'MOL': '100 ml/14L',
            'PGPR': '1 L/ha',
            'Trichoderma': '50 g/plant',
            'Beauveria': '2 ml/L',
            'Azotobacter': '2 L/ha'
        },
        'Fruits': {
            'ROTAN': '200 ml/14L',
            'MOL': '200 ml/14L',
            'PGPR': '2 L/ha',
            'Trichoderma': '100 g/tree',
            'Beauveria': '3 ml/L',
            'Azotobacter': '1 L/ha'
        },
        'Chili': {
            'ROTAN': '100 ml/14L',
            'MOL': '100 ml/14L',
            'PGPR': '1 L/ha',
            'Trichoderma': '50 g/plant',
            'Beauveria': '2 ml/L',
            'Azotobacter': '2 L/ha'
        },
        'Melon': {
            'ROTAN': '150 ml/14L',
            'MOL': '150 ml/14L',
            'PGPR': '1.5 L/ha',
            'Trichoderma': '30 g/plant',
            'Beauveria': '2 ml/L',
            'Azotobacter': '1.5 L/ha'
        }
    }
    
    def calculate_production_cost(self, product_type, volume_liters):
        """Calculate total production cost"""
        if product_type not in self.COST_DATABASE:
            return None
        
        product = self.COST_DATABASE[product_type]
        batch_output = product['output_volume']
        num_batches = volume_liters / batch_output
        
        # Calculate raw material cost per batch
        raw_material_cost = 0
        for material, data in product['raw_materials'].items():
            raw_material_cost += data['qty'] * data['price']
        
        # Total cost
        total_raw_material = raw_material_cost * num_batches
        labor_cost = num_batches * 50000  # Rp 50k per batch
        utilities = num_batches * 25000  # Electricity, water
        packaging = volume_liters * 2000  # Rp 2k per liter
        
        total_cost = total_raw_material + labor_cost + utilities + packaging
        cost_per_liter = total_cost / volume_liters
        
        return {
            'total_cost': total_cost,
            'cost_per_liter': cost_per_liter,
            'raw_material_cost': total_raw_material,
            'labor_cost': labor_cost,
            'utilities': utilities,
            'packaging': packaging,
            'num_batches': num_batches
        }
    
    def calculate_cfu(self, dilution_factor, colony_count, plating_volume_ml=0.1):
        """Calculate CFU/ml"""
        cfu_per_ml = (colony_count / plating_volume_ml) * dilution_factor
        return cfu_per_ml
    
    def calculate_roi(self, investment, monthly_production_liters, price_per_liter, 
                     cost_per_liter, months=12):
        """Calculate ROI and break-even"""
        monthly_revenue = monthly_production_liters * price_per_liter
        monthly_cost = monthly_production_liters * cost_per_liter
        monthly_profit = monthly_revenue - monthly_cost
        
        annual_profit = monthly_profit * months
        roi_percent = (annual_profit / investment) * 100
        
        # Break-even calculation
        if monthly_profit > 0:
            break_even_months = investment / monthly_profit
        else:
            break_even_months = float('inf')
        
        return {
            'monthly_revenue': monthly_revenue,
            'monthly_cost': monthly_cost,
            'monthly_profit': monthly_profit,
            'annual_profit': annual_profit,
            'roi_percent': roi_percent,
            'break_even_months': break_even_months,
            'payback_period_years': break_even_months / 12
        }
    
    def get_application_rate(self, microbe_type, crop_type):
        """Get recommended application rate"""
        if crop_type in self.APPLICATION_RATES:
            return self.APPLICATION_RATES[crop_type].get(microbe_type, 'N/A')
        return 'N/A'
    
    def calculate_mass_multiplication(self, biang_volume_liters, target_volume_liters):
        """Calculate ingredients for ROTAN mass multiplication"""
        ratio = target_volume_liters / biang_volume_liters
        
        # Standard formula for 100L from 1L biang
        base_ratio = 100  # 100L from 1L
        scale_factor = target_volume_liters / base_ratio
        
        ingredients = {
            'Air Jernih': target_volume_liters,
            'Dedak': 10 * scale_factor,  # kg
            'Gula Kelapa': 5 * scale_factor,  # kg
            'Air Kelapa': 10 * scale_factor,  # L
            'Biang ROTAN': biang_volume_liters
        }
        
        # Cost estimation
        cost = (
            ingredients['Dedak'] * 3000 +
            ingredients['Gula Kelapa'] * 20000 +
            ingredients['Air Kelapa'] * 5000 +
            biang_volume_liters * 40000  # Assuming biang cost
        )
        
        return {
            'ingredients': ingredients,
            'estimated_cost': cost,
            'cost_per_liter': cost / target_volume_liters,
            'fermentation_days': 7
        }
