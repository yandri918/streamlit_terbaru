# -*- coding: utf-8 -*-
"""
Test for Phosphorus Release Service
Validates against WAGRI example data
"""

import sys
from pathlib import Path

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from agrisensa_commodities.services.phosphorus_release_service import PhosphorusReleaseService

print("=" * 60)
print("WAGRI PHOSPHORUS RELEASE VALIDATION TEST")
print("=" * 60)

# WAGRI Example Data
# Input: 100 kg material, TP=6.02%, FE_P=70%, Region_PK=1
# Expected Output: CumList = [3.186, 3.186, ..., 3.186]

result = PhosphorusReleaseService.calculate_p_release(
    start_date="20210122",
    end_date="20210131",  # 10 days for testing
    material_amount=100.0,
    material_type=3,
    material_props={
        "MC": 26.5,
        "TP": 6.02
    },
    coefficients={
        "Region_PK": 1,
        "FE_P": 70
    }
)

print("\nTest Results:")
print("-" * 60)
print(f"Total P in Material: {result['total_p_in_material']:.2f} kg")
print(f"Available P: {result['available_p']:.4f} kg")
print(f"Availability: {result['availability_percentage']:.1f}%")
print(f"Total Days: {result['total_days']}")
print(f"\nCumList (first 5 values): {result['cum_list'][:5]}")

# Expected from WAGRI
expected_p = 3.186  # From WAGRI output

print(f"\nExpected P (WAGRI): {expected_p:.4f} kg")
print(f"Actual P: {result['available_p']:.4f} kg")
print(f"Difference: {abs(result['available_p'] - expected_p):.4f} kg")
print(f"Percentage Diff: {abs(result['available_p'] - expected_p) / expected_p * 100:.2f}%")

# Test material presets
print("\n" + "=" * 60)
print("TESTING MATERIAL PRESETS")
print("=" * 60)

for material_name in PhosphorusReleaseService.list_material_presets():
    preset = PhosphorusReleaseService.get_material_preset(material_name)
    print(f"\n{material_name}:")
    print(f"  MC: {preset['MC']}%")
    print(f"  TP: {preset['TP']}%")
    print(f"  Description: {preset['description']}")

# Test P to P2O5 conversion
print("\n" + "=" * 60)
print("TESTING P <-> P2O5 CONVERSION")
print("=" * 60)

p_kg = 10.0
p2o5_kg = PhosphorusReleaseService.convert_p_to_p2o5(p_kg)
p_back = PhosphorusReleaseService.convert_p2o5_to_p(p2o5_kg)

print(f"\n{p_kg} kg P = {p2o5_kg:.2f} kg P2O5")
print(f"{p2o5_kg:.2f} kg P2O5 = {p_back:.2f} kg P")
print(f"Conversion accurate: {abs(p_kg - p_back) < 0.01}")

# Test comparison with synthetic
print("\n" + "=" * 60)
print("TESTING COMPARISON WITH SYNTHETIC")
print("=" * 60)

comparison = PhosphorusReleaseService.compare_with_synthetic(
    organic_p=result['available_p'],
    synthetic_type="SP-36"
)

print(f"\nOrganic P: {comparison['organic_p']:.2f} kg")
print(f"Organic P2O5: {comparison['organic_p2o5']:.2f} kg")
print(f"Equivalent {comparison['synthetic_type']}: {comparison['synthetic_needed_kg']:.2f} kg")
print(f"Advantage: {comparison['advantage']}")

print("\n" + "=" * 60)
print("TEST COMPLETED")
print("=" * 60)
