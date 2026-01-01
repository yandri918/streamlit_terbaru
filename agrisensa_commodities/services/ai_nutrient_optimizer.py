"""
AI Nutrient Optimizer Service
Sistem Optimasi Nutrisi Hidroponik berbasis AI

Fitur:
- Rekomendasi nutrisi otomatis berdasarkan tanaman & fase pertumbuhan
- Optimasi EC & pH
- Perhitungan formula nutrisi detail
- Analisis defisiensi & toxicity
- Rekomendasi penyesuaian
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

class AInutrientOptimizer:
    """Service untuk optimasi nutrisi hidroponik dengan AI"""
    
    # Database nutrisi optimal per tanaman & fase
    OPTIMAL_PARAMETERS = {
        'Selada': {
            'Seedling': {'ec': 0.8, 'ph': 6.0, 'n': 150, 'p': 50, 'k': 200},
            'Vegetatif': {'ec': 1.2, 'ph': 5.8, 'n': 200, 'p': 60, 'k': 250},
            'Panen': {'ec': 1.0, 'ph': 6.0, 'n': 180, 'p': 55, 'k': 220}
        },
        'Tomat': {
            'Seedling': {'ec': 1.0, 'ph': 6.0, 'n': 180, 'p': 60, 'k': 220},
            'Vegetatif': {'ec': 1.8, 'ph': 5.8, 'n': 220, 'p': 80, 'k': 280},
            'Berbunga': {'ec': 2.2, 'ph': 5.8, 'n': 200, 'p': 100, 'k': 320},
            'Berbuah': {'ec': 2.5, 'ph': 6.0, 'n': 180, 'p': 120, 'k': 350}
        },
        'Cabai': {
            'Seedling': {'ec': 1.0, 'ph': 6.0, 'n': 180, 'p': 60, 'k': 220},
            'Vegetatif': {'ec': 1.8, 'ph': 5.8, 'n': 220, 'p': 80, 'k': 280},
            'Berbunga': {'ec': 2.0, 'ph': 5.8, 'n': 200, 'p': 100, 'k': 320},
            'Berbuah': {'ec': 2.3, 'ph': 6.0, 'n': 180, 'p': 120, 'k': 350}
        },
        'Strawberry': {
            'Seedling': {'ec': 0.8, 'ph': 6.0, 'n': 150, 'p': 50, 'k': 180},
            'Vegetatif': {'ec': 1.2, 'ph': 5.8, 'n': 180, 'p': 60, 'k': 220},
            'Berbunga': {'ec': 1.5, 'ph': 5.8, 'n': 160, 'p': 80, 'k': 250},
            'Berbuah': {'ec': 1.8, 'ph': 6.0, 'n': 140, 'p': 100, 'k': 280}
        },
        'Timun': {
            'Seedling': {'ec': 1.0, 'ph': 6.0, 'n': 180, 'p': 60, 'k': 220},
            'Vegetatif': {'ec': 1.7, 'ph': 5.8, 'n': 220, 'p': 80, 'k': 280},
            'Berbunga': {'ec': 2.0, 'ph': 5.8, 'n': 200, 'p': 90, 'k': 300},
            'Berbuah': {'ec': 2.2, 'ph': 6.0, 'n': 180, 'p': 100, 'k': 320}
        },
        'Kangkung': {
            'Seedling': {'ec': 0.8, 'ph': 6.0, 'n': 150, 'p': 50, 'k': 180},
            'Vegetatif': {'ec': 1.2, 'ph': 5.8, 'n': 200, 'p': 60, 'k': 220},
            'Panen': {'ec': 1.0, 'ph': 6.0, 'n': 180, 'p': 55, 'k': 200}
        },
        'Pakcoy': {
            'Seedling': {'ec': 0.8, 'ph': 6.0, 'n': 150, 'p': 50, 'k': 180},
            'Vegetatif': {'ec': 1.2, 'ph': 5.8, 'n': 200, 'p': 60, 'k': 220},
            'Panen': {'ec': 1.0, 'ph': 6.0, 'n': 180, 'p': 55, 'k': 200}
        }
    }
    
    # Formula nutrisi AB Mix (gram per 100 liter)
    NUTRIENT_FORMULAS = {
        'Standard': {
            'Calcium Nitrate': 100,
            'Potassium Nitrate': 50,
            'Monopotassium Phosphate (MKP)': 40,
            'Magnesium Sulfate': 75,
            'Iron Chelate (Fe-EDTA)': 5,
            'Manganese Sulfate': 2,
            'Boric Acid': 0.3,
            'Zinc Sulfate': 0.2,
            'Copper Sulfate': 0.05,
            'Sodium Molybdate': 0.02
        },
        'Tinggi_N': {
            'Calcium Nitrate': 120,
            'Potassium Nitrate': 60,
            'Monopotassium Phosphate (MKP)': 35,
            'Magnesium Sulfate': 75,
            'Iron Chelate (Fe-EDTA)': 5,
            'Manganese Sulfate': 2,
            'Boric Acid': 0.3,
            'Zinc Sulfate': 0.2,
            'Copper Sulfate': 0.05,
            'Sodium Molybdate': 0.02
        },
        'Tinggi_K': {
            'Calcium Nitrate': 100,
            'Potassium Nitrate': 70,
            'Monopotassium Phosphate (MKP)': 50,
            'Magnesium Sulfate': 75,
            'Iron Chelate (Fe-EDTA)': 5,
            'Manganese Sulfate': 2,
            'Boric Acid': 0.3,
            'Zinc Sulfate': 0.2,
            'Copper Sulfate': 0.05,
            'Sodium Molybdate': 0.02
        },
        'Tinggi_P': {
            'Calcium Nitrate': 100,
            'Potassium Nitrate': 50,
            'Monopotassium Phosphate (MKP)': 60,
            'Magnesium Sulfate': 75,
            'Iron Chelate (Fe-EDTA)': 5,
            'Manganese Sulfate': 2,
            'Boric Acid': 0.3,
            'Zinc Sulfate': 0.2,
            'Copper Sulfate': 0.05,
            'Sodium Molybdate': 0.02
        }
    }
    
    # Harga nutrisi (Rp per kg)
    NUTRIENT_PRICES = {
        'Calcium Nitrate': 15000,
        'Potassium Nitrate': 25000,
        'Monopotassium Phosphate (MKP)': 35000,
        'Magnesium Sulfate': 12000,
        'Iron Chelate (Fe-EDTA)': 150000,
        'Manganese Sulfate': 80000,
        'Boric Acid': 100000,
        'Zinc Sulfate': 90000,
        'Copper Sulfate': 95000,
        'Sodium Molybdate': 200000
    }
    
    def get_optimal_parameters(self, tanaman: str, fase: str) -> Dict:
        """
        Mendapatkan parameter optimal untuk tanaman & fase tertentu
        
        Args:
            tanaman: Nama tanaman (Selada, Tomat, dll)
            fase: Fase pertumbuhan (Seedling, Vegetatif, dll)
            
        Returns:
            Dict dengan EC, pH, dan NPK optimal
        """
        if tanaman in self.OPTIMAL_PARAMETERS:
            if fase in self.OPTIMAL_PARAMETERS[tanaman]:
                return self.OPTIMAL_PARAMETERS[tanaman][fase]
        
        # Default jika tidak ada data
        return {'ec': 1.5, 'ph': 6.0, 'n': 180, 'p': 60, 'k': 220}
    
    def recommend_formula(self, tanaman: str, fase: str, target_hasil: str = 'Standard') -> Dict:
        """
        Merekomendasikan formula nutrisi berdasarkan AI
        
        Args:
            tanaman: Nama tanaman
            fase: Fase pertumbuhan
            target_hasil: Standard, Tinggi, Maksimal
            
        Returns:
            Dict dengan formula nutrisi lengkap
        """
        # Dapatkan parameter optimal
        optimal = self.get_optimal_parameters(tanaman, fase)
        
        # Pilih formula base
        if fase in ['Vegetatif', 'Seedling']:
            formula_type = 'Tinggi_N'
        elif fase in ['Berbunga']:
            formula_type = 'Tinggi_P'
        elif fase in ['Berbuah', 'Panen']:
            formula_type = 'Tinggi_K'
        else:
            formula_type = 'Standard'
        
        # Adjust berdasarkan target hasil
        formula = self.NUTRIENT_FORMULAS[formula_type].copy()
        
        if target_hasil == 'Tinggi':
            # Naikkan 10%
            formula = {k: v * 1.1 for k, v in formula.items()}
        elif target_hasil == 'Maksimal':
            # Naikkan 20%
            formula = {k: v * 1.2 for k, v in formula.items()}
        
        return {
            'formula': formula,
            'optimal_ec': optimal['ec'],
            'optimal_ph': optimal['ph'],
            'formula_type': formula_type
        }
    
    def calculate_cost(self, formula: Dict, volume: int = 100) -> Dict:
        """
        Menghitung biaya nutrisi
        
        Args:
            formula: Dict formula nutrisi (gram per 100L)
            volume: Volume larutan (liter)
            
        Returns:
            Dict dengan breakdown biaya
        """
        total_cost = 0
        breakdown = {}
        
        for nutrient, amount_per_100l in formula.items():
            # Hitung jumlah untuk volume yang diminta
            amount_needed = (amount_per_100l / 100) * volume  # gram
            
            # Hitung biaya
            price_per_kg = self.NUTRIENT_PRICES.get(nutrient, 0)
            cost = (amount_needed / 1000) * price_per_kg
            
            breakdown[nutrient] = {
                'jumlah_gram': round(amount_needed, 2),
                'biaya': round(cost, 0)
            }
            
            total_cost += cost
        
        return {
            'breakdown': breakdown,
            'total_biaya': round(total_cost, 0),
            'biaya_per_liter': round(total_cost / volume, 0)
        }
    
    def analyze_deficiency(self, current_ec: float, current_ph: float, 
                          optimal_ec: float, optimal_ph: float) -> Dict:
        """
        Menganalisis defisiensi atau kelebihan nutrisi
        
        Args:
            current_ec: EC saat ini
            current_ph: pH saat ini
            optimal_ec: EC optimal
            optimal_ph: pH optimal
            
        Returns:
            Dict dengan analisis dan rekomendasi
        """
        analysis = {
            'status': 'Optimal',
            'masalah': [],
            'rekomendasi': [],
            'tingkat_keparahan': 'Rendah'
        }
        
        # Analisis EC
        ec_diff = current_ec - optimal_ec
        if abs(ec_diff) > 0.5:
            analysis['tingkat_keparahan'] = 'Tinggi'
            if ec_diff > 0:
                analysis['status'] = 'Kelebihan Nutrisi'
                analysis['masalah'].append(f"EC terlalu tinggi ({current_ec} vs {optimal_ec} mS/cm)")
                analysis['rekomendasi'].append("Tambahkan air bersih untuk menurunkan EC")
                analysis['rekomendasi'].append(f"Perlu tambahan {abs(ec_diff) * 20:.0f}% air")
            else:
                analysis['status'] = 'Kekurangan Nutrisi'
                analysis['masalah'].append(f"EC terlalu rendah ({current_ec} vs {optimal_ec} mS/cm)")
                analysis['rekomendasi'].append("Tambahkan nutrisi AB Mix")
                analysis['rekomendasi'].append(f"Perlu tambahan {abs(ec_diff) * 10:.0f}% nutrisi")
        elif abs(ec_diff) > 0.2:
            analysis['tingkat_keparahan'] = 'Sedang'
            if ec_diff > 0:
                analysis['status'] = 'Sedikit Berlebih'
                analysis['rekomendasi'].append("Monitor ketat, pertimbangkan dilusi ringan")
            else:
                analysis['status'] = 'Sedikit Kurang'
                analysis['rekomendasi'].append("Monitor ketat, pertimbangkan penambahan nutrisi")
        
        # Analisis pH
        ph_diff = current_ph - optimal_ph
        if abs(ph_diff) > 0.5:
            if ph_diff > 0:
                analysis['masalah'].append(f"pH terlalu tinggi/basa ({current_ph} vs {optimal_ph})")
                analysis['rekomendasi'].append("Tambahkan pH Down (asam fosfat/nitrat)")
                analysis['rekomendasi'].append("Turunkan pH secara bertahap 0.2-0.3 per hari")
            else:
                analysis['masalah'].append(f"pH terlalu rendah/asam ({current_ph} vs {optimal_ph})")
                analysis['rekomendasi'].append("Tambahkan pH Up (kalium hidroksida)")
                analysis['rekomendasi'].append("Naikkan pH secara bertahap 0.2-0.3 per hari")
        
        return analysis
    
    def get_adjustment_guide(self, current_ec: float, target_ec: float, volume: int) -> Dict:
        """
        Panduan penyesuaian EC
        
        Args:
            current_ec: EC saat ini
            target_ec: EC target
            volume: Volume larutan (liter)
            
        Returns:
            Dict dengan panduan penyesuaian
        """
        ec_diff = target_ec - current_ec
        
        if ec_diff > 0:
            # Perlu menaikkan EC (tambah nutrisi)
            nutrient_needed = abs(ec_diff) * volume * 0.5  # gram (estimasi)
            return {
                'aksi': 'Tambah Nutrisi',
                'jumlah_nutrisi': round(nutrient_needed, 1),
                'cara': f"Tambahkan {nutrient_needed:.1f} gram AB Mix ke {volume} liter larutan",
                'catatan': "Tambahkan secara bertahap, aduk rata, tunggu 30 menit, lalu ukur ulang"
            }
        elif ec_diff < 0:
            # Perlu menurunkan EC (tambah air)
            water_needed = abs(ec_diff) * volume * 0.3  # liter (estimasi)
            return {
                'aksi': 'Tambah Air',
                'jumlah_air': round(water_needed, 1),
                'cara': f"Tambahkan {water_needed:.1f} liter air bersih ke larutan",
                'catatan': "Tambahkan secara bertahap, aduk rata, tunggu 30 menit, lalu ukur ulang"
            }
        else:
            return {
                'aksi': 'Tidak Perlu Penyesuaian',
                'cara': 'EC sudah optimal',
                'catatan': 'Monitor rutin setiap hari'
            }
    
    def generate_recommendation(self, tanaman: str, fase: str, current_ec: float, 
                               current_ph: float, target_hasil: str = 'Standard',
                               volume: int = 100) -> Dict:
        """
        Generate rekomendasi lengkap (fungsi utama AI)
        
        Args:
            tanaman: Nama tanaman
            fase: Fase pertumbuhan
            current_ec: EC saat ini
            current_ph: pH saat ini
            target_hasil: Standard, Tinggi, Maksimal
            volume: Volume larutan (liter)
            
        Returns:
            Dict dengan rekomendasi lengkap
        """
        # Dapatkan formula optimal
        recommendation = self.recommend_formula(tanaman, fase, target_hasil)
        
        # Hitung biaya
        cost = self.calculate_cost(recommendation['formula'], volume)
        
        # Analisis kondisi saat ini
        analysis = self.analyze_deficiency(
            current_ec, current_ph,
            recommendation['optimal_ec'], recommendation['optimal_ph']
        )
        
        # Panduan penyesuaian
        adjustment = self.get_adjustment_guide(
            current_ec, recommendation['optimal_ec'], volume
        )
        
        return {
            'tanaman': tanaman,
            'fase': fase,
            'target_hasil': target_hasil,
            'optimal_ec': recommendation['optimal_ec'],
            'optimal_ph': recommendation['optimal_ph'],
            'formula_type': recommendation['formula_type'],
            'formula': recommendation['formula'],
            'biaya': cost,
            'analisis': analysis,
            'penyesuaian': adjustment,
            'insight': self._generate_insight(tanaman, fase, analysis)
        }
    
    def _generate_insight(self, tanaman: str, fase: str, analysis: Dict) -> str:
        """Generate AI insight berdasarkan kondisi"""
        insights = []
        
        # Insight berdasarkan tanaman & fase
        if tanaman in ['Tomat', 'Cabai'] and fase == 'Berbuah':
            insights.append("💡 Fase berbuah membutuhkan K tinggi untuk kualitas buah optimal")
        elif tanaman in ['Selada', 'Kangkung', 'Pakcoy'] and fase == 'Vegetatif':
            insights.append("💡 Sayuran daun membutuhkan N tinggi untuk pertumbuhan maksimal")
        
        # Insight berdasarkan analisis
        if analysis['tingkat_keparahan'] == 'Tinggi':
            insights.append("⚠️ Segera lakukan penyesuaian untuk mencegah kerusakan tanaman")
        elif analysis['status'] == 'Optimal':
            insights.append("✅ Kondisi nutrisi optimal, pertahankan monitoring rutin")
        
        return " | ".join(insights) if insights else "Monitor rutin untuk hasil terbaik"
