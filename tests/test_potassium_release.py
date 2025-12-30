# -*- coding: utf-8 -*-
"""
Test for Potassium Release Service
Validates against WAGRI example data

Author: AgriSensa Team
Date: 2025-12-30
"""

import sys
from pathlib import Path

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from agrisensa_commodities.services.potassium_release_service import PotassiumReleaseService


def test_wagri_example():
    """
    Test against WAGRI example data.
    
    Input:
    - MaterialAmount: 100 kg
    - TK: 4.17%
    - FE_K: 70%
    - Region_PK: 1
    
    Expected Output:
    - K available: 2.7891045 kg
    """
    print("=" * 60)
    print("TEST: WAGRI Example Validation")
    print("=" * 60)
    
    result = PotassiumReleaseService.calculate_k_release(
        start_date="20210122",
        end_date="20220223",
        material_amount=100,
        material_type=3,  # Kompos Kotoran Ayam
        material_props={"MC": 26.5, "TK": 4.17},
        coefficients={"Region_PK": 1, "FE_K": 70}
    )
    
    print(f"\nInput:")
    print(f"  Material Amount: 100 kg")
    print(f"  TK: 4.17%")
    print(f"  FE_K: 70%")
    print(f"  Region_PK: 1")
    
    print(f"\nWAGRI Expected:")
    print(f"  K available: 2.7891045 kg")
    
    print(f"\nOur Output:")
    print(f"  Total K in material: {result['total_k_in_material']:.4f} kg")
    print(f"  K available: {result['available_k']:.4f} kg")
    print(f"  K2O equivalent: {PotassiumReleaseService.convert_k_to_k2o(result['available_k']):.4f} kg")
    
    # Calculate accuracy
    expected = 2.7891045
    actual = result['available_k']
    accuracy = (1 - abs(expected - actual) / expected) * 100
    
    print(f"\nAccuracy: {accuracy:.2f}%")
    
    if accuracy > 99.5:
        print("✅ PASS: Accuracy > 99.5%")
    else:
        print(f"❌ FAIL: Accuracy {accuracy:.2f}% < 99.5%")
    
    return accuracy > 99.5


def test_material_presets():
    """Test all material presets."""
    print("\n" + "=" * 60)
    print("TEST: Material Presets")
    print("=" * 60)
    
    presets = PotassiumReleaseService.list_material_presets()
    print(f"\nTotal presets: {len(presets)}")
    
    for preset_name in presets:
        preset = PotassiumReleaseService.get_material_preset(preset_name)
        print(f"\n{preset_name}:")
        print(f"  Category: {preset['category']}")
        print(f"  MC: {preset['MC']}%")
        print(f"  TK: {preset['TK']}%")
        print(f"  Material Type: {preset['material_type']}")
        print(f"  Description: {preset['description']}")
    
    print("\n✅ All presets loaded successfully")
    return True


def test_k_k2o_conversion():
    """Test K/K2O conversion."""
    print("\n" + "=" * 60)
    print("TEST: K/K2O Conversion")
    print("=" * 60)
    
    k_amount = 10.0
    k2o_amount = PotassiumReleaseService.convert_k_to_k2o(k_amount)
    k_back = PotassiumReleaseService.convert_k2o_to_k(k2o_amount)
    
    print(f"\nK: {k_amount} kg")
    print(f"K2O: {k2o_amount} kg")
    print(f"K (converted back): {k_back} kg")
    
    if abs(k_amount - k_back) < 0.001:
        print("✅ PASS: Conversion accurate")
        return True
    else:
        print("❌ FAIL: Conversion error")
        return False


def test_synthetic_comparison():
    """Test comparison with synthetic fertilizers."""
    print("\n" + "=" * 60)
    print("TEST: Synthetic Fertilizer Comparison")
    print("=" * 60)
    
    organic_k = 10.0  # kg
    
    fertilizers = ["KCl", "K2SO4", "NPK 15-15-15", "NPK 16-16-16", "KNO3"]
    
    for fert in fertilizers:
        comparison = PotassiumReleaseService.compare_with_synthetic(organic_k, fert)
        
        print(f"\n{fert}:")
        print(f"  K2O content: {comparison['synthetic_k2o_content']}%")
        print(f"  Equivalent needed: {comparison['synthetic_needed_kg']:.2f} kg")
        print(f"  Info: {comparison['fertilizer_info']}")
    
    print("\n✅ All comparisons completed")
    return True


def test_split_application():
    """Test split application recommendations."""
    print("\n" + "=" * 60)
    print("TEST: Split Application Recommendations")
    print("=" * 60)
    
    available_k = 50.0  # kg
    
    crops = ["rice", "corn", "vegetables", "fruits", "general"]
    soils = ["sandy", "medium", "clay"]
    
    for crop in crops:
        for soil in soils:
            schedule = PotassiumReleaseService.recommend_split_application(
                available_k, crop, soil
            )
            
            print(f"\n{crop.upper()} on {soil} soil:")
            print(f"  Splits: {schedule['splits']}")
            print(f"  Reason: {schedule['reason']}")
            
            for i, app in enumerate(schedule['schedule'], 1):
                print(f"  Application {i}:")
                print(f"    Timing: {app['timing']}")
                print(f"    Amount: {app['amount_k']:.2f} kg K ({app['percentage']}%)")
                print(f"    K2O: {app['amount_k2o']:.2f} kg")
    
    print("\n✅ All split recommendations generated")
    return True


if __name__ == "__main__":
    print("\nPOTASSIUM RELEASE SERVICE - TEST SUITE")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("WAGRI Validation", test_wagri_example()))
    results.append(("Material Presets", test_material_presets()))
    results.append(("K/K2O Conversion", test_k_k2o_conversion()))
    results.append(("Synthetic Comparison", test_synthetic_comparison()))
    results.append(("Split Application", test_split_application()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\nALL TESTS PASSED!")
    else:
        print("\nSOME TESTS FAILED")
    
    print("=" * 60)
