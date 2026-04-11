"""
Quick diagnostic script to test RAB Calculator imports and functions
"""

import sys
from pathlib import Path

# Add path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("=" * 50)
print("RAB Calculator Diagnostic")
print("=" * 50)

# Test 1: Import design system
try:
    from utils.design_system import apply_design_system, icon, COLORS
    print("✅ Design system import: OK")
except Exception as e:
    print(f"❌ Design system import: FAILED - {e}")

# Test 2: Import rab_templates
try:
    from utils.rab_templates import get_all_templates, get_template, REGIONAL_BENCHMARKS, calculate_efficiency_score
    print("✅ RAB templates import: OK")
except Exception as e:
    print(f"❌ RAB templates import: FAILED - {e}")

# Test 3: Check templates
try:
    templates = get_all_templates()
    print(f"✅ Templates loaded: {len(templates)} templates")
    print(f"   Template names: {list(templates.keys())}")
except Exception as e:
    print(f"❌ Templates load: FAILED - {e}")

# Test 4: Check benchmarks
try:
    print(f"✅ Regional benchmarks: {len(REGIONAL_BENCHMARKS)} regions")
    print(f"   Regions: {list(REGIONAL_BENCHMARKS.keys())}")
except Exception as e:
    print(f"❌ Benchmarks: FAILED - {e}")

# Test 5: Test efficiency calculation
try:
    test_data = {
        'biaya_per_kg': 2500,
        'target_produksi': 6.5,
        'roi': 50
    }
    test_benchmark = REGIONAL_BENCHMARKS['Jawa Barat']
    scores = calculate_efficiency_score(test_data, test_benchmark)
    print(f"✅ Efficiency calculation: OK")
    print(f"   Scores: {scores}")
except Exception as e:
    print(f"❌ Efficiency calculation: FAILED - {e}")

print("=" * 50)
print("Diagnostic Complete")
print("=" * 50)
