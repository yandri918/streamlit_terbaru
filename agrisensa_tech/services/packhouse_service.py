"""
Packhouse Service
Logic for Post-Harvest Grading QC and Label Generation.
"""
from datetime import datetime

class PackhouseService:
    """
    Service untuk manajemen Packhouse (Grading & Labeling).
    Standard MHI - Melon GH.
    """
    
    # Kriteria Grade Standard (Bisa dicustom)
    GRADE_SPECS = {
        'Melon Premium (Grade A)': {
            'min_weight_kg': 1.5,
            'max_weight_kg': 2.5,
            'brix_min': 12,
            'appearance': 'Perfect net, no defects'
        },
        'Melon Standard (Grade B)': {
            'min_weight_kg': 1.0,
            'max_weight_kg': 1.49,
            'brix_min': 10,
            'appearance': 'Minor cosmetic defects allowed'
        },
        'Reject': {
            'desc': 'Undersized, pest damage, cracked'
        }
    }
    
    def calculate_grading_stats(self, batch_data):
        """
        Hitung statistik hasil panen.
        batch_data = [
            {'weight': 1.6, 'brix': 13, 'visual': 'ok'}, ...
        ]
        """
        stats = {
            'total_pcs': 0,
            'grade_a_count': 0,
            'grade_b_count': 0,
            'reject_count': 0,
            'total_weight_kg': 0
        }
        
        for item in batch_data:
            stats['total_pcs'] += 1
            w = item['weight']
            stats['total_weight_kg'] += w
            
            # Simple Logic (Bisa diperluas)
            if item['grade'] == 'A':
                stats['grade_a_count'] += 1
            elif item['grade'] == 'B':
                stats['grade_b_count'] += 1
            else:
                stats['reject_count'] += 1
                
        # Percentages
        if stats['total_pcs'] > 0:
            stats['pct_a'] = (stats['grade_a_count'] / stats['total_pcs']) * 100
            stats['pct_b'] = (stats['grade_b_count'] / stats['total_pcs']) * 100
            stats['pct_reject'] = (stats['reject_count'] / stats['total_pcs']) * 100
        else:
            stats['pct_a'] = 0
            stats['pct_b'] = 0
            stats['pct_reject'] = 0
            
        return stats

    def generate_label_text(self, batch_id, gh_source, product_name="Melon Premium", grade="A", weight=0):
        """
        Generate text template for printable label.
        """
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        label = f"""
        --------------------------------
        AGRISENSA FRESH PRODUCE
        --------------------------------
        Product : {product_name}
        Grade   : {grade}
        Origin  : {gh_source}
        Batch   : {batch_id}
        Date    : {date_str}
        Weight  : {weight} kg
        --------------------------------
        QC Checked | Traceable
        --------------------------------
        """
        return label
