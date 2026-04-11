"""Service for agronomy research statistical analysis."""
import numpy as np
from scipy import stats

class ResearchService:
    """Service for analyzing experimental data."""
    
    @staticmethod
    def analyze_ral(data):
        """
        Analyze Completely Randomized Design (Rancangan Acak Lengkap - RAL).
        
        Args:
            data (dict): {
                "treatment_names": ["P0", "P1", "P2"],
                "replications": 3,
                "parameters": {
                    "Tinggi Tanaman": [
                        [10, 12, 11], # Data for P0 (R1, R2, R3)
                        [15, 16, 14], # Data for P1
                        [20, 22, 21]  # Data for P2
                    ]
                }
            }
            
        Returns:
            dict: Analysis results including ANOVA table and conclusions.
        """
        results = {}
        treatment_names = data.get('treatment_names', [])
        
        for param_name, values in data.get('parameters', {}).items():
            # values is a list of lists (treatments x replications)
            # Convert to numpy array for easier calculation
            try:
                groups = [np.array(v) for v in values]
                
                # 1. Descriptive Statistics
                descriptive = []
                for i, group in enumerate(groups):
                    desc = {
                        "treatment": treatment_names[i] if i < len(treatment_names) else f"P{i}",
                        "mean": round(float(np.mean(group)), 2),
                        "std": round(float(np.std(group, ddof=1)), 2),
                        "min": float(np.min(group)),
                        "max": float(np.max(group))
                    }
                    descriptive.append(desc)
                
                # 2. One-Way ANOVA
                f_stat, p_value = stats.f_oneway(*groups)
                
                # Interpretation
                significant = bool(p_value < 0.05)
                conclusion = ""
                if significant:
                    best_treatment = max(descriptive, key=lambda x: x['mean'])
                    conclusion = f"Perlakuan memberikan pengaruh **NYATA** (Signifikan) terhadap {param_name}. <br>Rata-rata tertinggi dicapai oleh **{best_treatment['treatment']}** ({best_treatment['mean']})."
                else:
                    conclusion = f"Perlakuan memberikan pengaruh **TIDAK NYATA** (Non-Signifikan) terhadap {param_name}. Perbedaan antar perlakuan mungkin hanya kebetulan."

                # 3. BNJ / Tukey HSD (Simplified Logic for MVP)
                # If significant, we ideally run post-hoc. 
                # For MVP, we just rank them.
                ranking = sorted(descriptive, key=lambda x: x['mean'], reverse=True)

                results[param_name] = {
                    "descriptive": descriptive,
                    "anova": {
                        "f_value": round(float(f_stat), 4),
                        "p_value": round(float(p_value), 6),
                        "significant": significant
                    },
                    "conclusion": conclusion,
                    "ranking": ranking
                }
                
            except Exception as e:
                results[param_name] = {"error": str(e)}
                
        return results
