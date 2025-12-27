"""
Integrated Farming System (IFS) Calculator
Simulates the flow of resources between Agriculture, Livestock, Fisheries, and Waste Management.
"""

class IntegratedFarmingCalculator:
    """
    Kalkulator Sistem Pertanian Terpadu (Zero Waste)
    Basis ilmiah untuk konversi limbah ke pakan/pupuk.
    """
    
    # --- CONSTANTS & SCIENTIFIC COEFFICIENTS ---
    
    # 1. Livestock Waste Production (kg/head/day)
    # Source: Balitnak, FAO
    LIVESTOCK_WASTE = {
        'sapi': {'feces': 15.0, 'urine': 10.0, 'biogas_potential': 0.04}, # m3 biogas/kg feces
        'kambing': {'feces': 1.5, 'urine': 1.0, 'biogas_potential': 0.05},
        'ayam_petelur': {'feces': 0.12, 'urine': 0.0, 'biogas_potential': 0.06},
        'ayam_pedaging': {'feces': 0.08, 'urine': 0.0, 'biogas_potential': 0.06},
        'bebek': {'feces': 0.15, 'urine': 0.0, 'biogas_potential': 0.05}
    }
    
    # 2. Crop Residue Production (kg biomass/ha/harvest) - Approx
    CROP_RESIDUE = {
        'padi': 5000, # Jerami
        'jagung': 8000, # Brangkasan
        'sayuran': 2000, # Sisa sayur
        'sawit': 12000 # Pelepah (per year)
    }
    
    # 3. Bioconversion Ratios
    # Source: Research journals on BSF & Vermicomposting
    CONVERSION_RATES = {
        'maggot_bsf': {
            'waste_reduction': 0.60, # 60% waste reduced
            'biomass_conversion': 0.15, # 100kg waste -> 15kg maggot
            'residue_conversion': 0.30, # 100kg waste -> 30kg kasgot
            'protein_content': 0.42 # 42% Protein
        },
        'vermicompost': {
            'waste_reduction': 0.50,
            'biomass_conversion': 0.05, # 100kg waste -> 5kg cacing biomass
            'residue_conversion': 0.60, # 100kg waste -> 60kg kascing
            'time_days': 30
        },
        'compost': {
            'mass_yield': 0.65, # 100kg wet waste -> 65kg compost
            'cn_ratio_target': 30
        }
    }
    
    # 4. Feed Requirements (kg/day)
    FEED_NEEDS = {
        'lele': 0.03, # 3% body weight
        'nila': 0.03,
        'ayam_kampung': 0.08,
        'bebek': 0.15
    }

    def calculate_flow(self, inputs):
        """
        Main calculation function based on user inputs.
        
        inputs = {
            'livestock': {'sapi': 2, 'ayam_petelur': 50},
            'land': {'padi': 1.0 (ha)},
            'fisheries': {'lele': 1000}
        }
        """
        results = {
            'daily_waste_kg': 0,
            'daily_urine_liter': 0,
            'crop_residue_kg_season': 0,
            'potential_maggot_kg': 0,
            'potential_kasgot_kg': 0,
            'potential_kascing_kg': 0,
            'potential_compost_kg': 0,
            'potential_biogas_m3': 0,
            'fish_feed_demand_kg': 0,
            'feed_substitution_value': 0,
            'fertilizer_substitution_value': 0
        }
        
        # 1. Calculate Livestock Waste Output
        livestock = inputs.get('livestock', {})
        for animal, count in livestock.items():
            if animal in self.LIVESTOCK_WASTE:
                data = self.LIVESTOCK_WASTE[animal]
                results['daily_waste_kg'] += count * data['feces']
                results['daily_urine_liter'] += count * data['urine']
                results['potential_biogas_m3'] += (count * data['feces']) * data['biogas_potential']

        # 2. Calculate Agriculture Residue
        land = inputs.get('land', {})
        for crop, ha in land.items():
            if crop in self.CROP_RESIDUE:
                results['crop_residue_kg_season'] += ha * self.CROP_RESIDUE[crop]

        # 3. Calculate Fisheries Demand
        fisheries = inputs.get('fisheries', {})
        for fish, count in fisheries.items():
            avg_weight = 0.1 # assumption 100g/fish average
            if fish in self.FEED_NEEDS:
                # Total biomass = count * weight
                # Feed = biomass * rate
                results['fish_feed_demand_kg'] += (count * avg_weight) * self.FEED_NEEDS[fish]

        # 4. Waste Allocation Simulation (User Strategy)
        # Assume generic strategy if not specified: 
        # 40% to Maggot, 30% to Vermicompost, 30% to Regular Compost
        
        total_organic_waste = results['daily_waste_kg']
        # Note: Crop residue usually goes to composting or cattle feed, not maggot immediately
        
        # Scenario: Maggot (BSF)
        maggot_input = total_organic_waste * 0.4
        results['potential_maggot_kg'] = maggot_input * self.CONVERSION_RATES['maggot_bsf']['biomass_conversion']
        results['potential_kasgot_kg'] = maggot_input * self.CONVERSION_RATES['maggot_bsf']['residue_conversion']
        
        # Scenario: Vermicompost (Cacing)
        vermi_input = total_organic_waste * 0.3
        results['potential_kascing_kg'] = vermi_input * self.CONVERSION_RATES['vermicompost']['residue_conversion']
        
        # Scenario: Regular Compost
        compost_input = total_organic_waste * 0.3
        results['potential_compost_kg'] = compost_input * self.CONVERSION_RATES['compost']['mass_yield']
        
        # 5. Integration / Substitution Value
        # Maggot replaces fish feed
        maggot_feed_value = 8000 # Rp/kg commercial pellet saved
        results['feed_substitution_value'] = results['potential_maggot_kg'] * maggot_feed_value
        
        # Organic Fertilizer value
        fertilizer_value = 2000 # Rp/kg organic fertilizer
        total_fertilizer = results['potential_kasgot_kg'] + results['potential_kascing_kg'] + results['potential_compost_kg']
        results['fertilizer_substitution_value'] = total_fertilizer * fertilizer_value
        
        return results

    def get_sankey_data(self, results):
        """
        Generate nodes and links for Sankey Diagram.
        """
        # Node indices:
        # 0: Livestock, 1: Agriculture, 2: Waste Pool
        # 3: Maggot BSF, 4: Vermicompost, 5: Biogas/Compost
        # 6: Fish Feed, 7: Fertilizer/Soil, 8: Energy
        
        waste = int(results['daily_waste_kg'])
        maggot_in = int(waste * 0.4)
        vermi_in = int(waste * 0.3)
        compost_in = int(waste * 0.3)
        
        maggot_out = int(results['potential_maggot_kg'])
        kasgot_out = int(results['potential_kasgot_kg'])
        kascing_out = int(results['potential_kascing_kg'])
        compost_out = int(results['potential_compost_kg'])
        
        return {
            'label': [
                "Ternak (Sumber Limbah)", "Sisa Tanaman", "Bank Limbah Organik", # Inputs
                "Biokonversi Maggot BSF", "Vermicomposting (Cacing)", "Kompos Konvensional", # Processes
                "Pakan Protein (Ikan/Unggas)", "Pupuk Organik Padat", "Media Tanam" # Outputs
            ],
            'source': [0, 1, 2, 2, 2, 3, 3, 4, 5],
            'target': [2, 2, 3, 4, 5, 6, 7, 7, 7],
            'value':  [
                waste, 10, # Inputs to Waste Pool (10 dummy for plants if 0)
                maggot_in, vermi_in, compost_in, # Pool to Processes
                maggot_out, kasgot_out, # Maggot outputs
                kascing_out, # Vermi output
                compost_out # Compost output
            ]
        }
