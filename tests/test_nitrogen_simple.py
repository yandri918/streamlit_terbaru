# -*- coding: utf-8 -*-
"""
Simple test for Nitrogen Release Service
Validates against WAGRI example data
"""

import sys
from pathlib import Path

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from agrisensa_commodities.services.nitrogen_release_service import NitrogenReleaseService


# WAGRI Example Input
input_data = {
    "start_date": "20240503",
    "water_date": "20240510",
    "end_date": "20240514",
    "material_amount": 123,
    "material_type": 1,
    "material_props": {
        "MC": 33.5,
        "ADSON": 19.9,
        "TN": 3.61,
        "Nm": 0.31
    },
    "coefficients": {
        "Q10": 1.47,
        "A1": 1595,
        "b": 0.189,
        "KD": 0.016786
    },
    "daily_temperatures": [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
}

# WAGRI Expected Output
expected_daily = [
    0.2584124111723678,
    0.2632424746458326,
    0.2680512130099664,
    0.2728352249671581,
    0.2775910108090447,
    0.28231588706607585,
    0.2870074286336999,
    0.30951135034666954,
    0.3300628002746264,
    0.34953820770159494,
    0.36835826149601536,
    0.38611118394565663
]

expected_cum = [
    0.2584124111723678,
    0.5216548858182004,
    0.7897060988281668,
    1.062541323795325,
    1.3401323346043696,
    1.6224482216704454,
    1.9094556503041453,
    2.2189670006508146,
    2.549029800925441,
    2.898568008627036,
    3.2669262701230513,
    3.653037454068708
]

print("=" * 60)
print("WAGRI NITROGEN RELEASE VALIDATION TEST")
print("=" * 60)

# Run calculation
result = NitrogenReleaseService.calculate_daily_release(**input_data)

# Check for errors
if "error" in result:
    print(f"ERROR: {result['error']}")
    sys.exit(1)

# Validate daily list
print("\nValidating Daily Release Values:")
print("-" * 60)

daily_match = True
max_diff = 0
for i, (actual, expected) in enumerate(zip(result['daily_list'], expected_daily)):
    diff = abs(actual - expected)
    percent_diff = (diff / expected * 100) if expected != 0 else 0
    max_diff = max(max_diff, percent_diff)
    
    match = "PASS" if percent_diff < 1.0 else "FAIL"
    print(f"Day {i+1:2d}: Actual={actual:.6f}, Expected={expected:.6f}, Diff={percent_diff:.3f}% [{match}]")
    
    if percent_diff >= 1.0:
        daily_match = False

# Validate cumulative list
print("\nValidating Cumulative Release Values:")
print("-" * 60)

cum_match = True
for i, (actual, expected) in enumerate(zip(result['cum_list'], expected_cum)):
    diff = abs(actual - expected)
    percent_diff = (diff / expected * 100) if expected != 0 else 0
    max_diff = max(max_diff, percent_diff)
    
    match = "PASS" if percent_diff < 1.0 else "FAIL"
    print(f"Day {i+1:2d}: Actual={actual:.6f}, Expected={expected:.6f}, Diff={percent_diff:.3f}% [{match}]")
    
    if percent_diff >= 1.0:
        cum_match = False

# Summary
print("\n" + "=" * 60)
print("TEST RESULTS SUMMARY")
print("=" * 60)

print(f"\nTotal N Released: {result['total_release_kg']:.4f} kg")
print(f"Release Percentage: {result['release_percentage']:.2f}%")
print(f"Maximum Difference: {max_diff:.3f}%")

if daily_match and cum_match:
    print("\n*** ALL TESTS PASSED! ***")
    print("Results match WAGRI example data within 1% tolerance")
    sys.exit(0)
else:
    print("\n*** SOME TESTS FAILED! ***")
    if not daily_match:
        print("- Daily release values do not match")
    if not cum_match:
        print("- Cumulative release values do not match")
    sys.exit(1)
