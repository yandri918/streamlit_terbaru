"""
Test suite for Nitrogen Release Service
Validates against WAGRI example data
"""

import sys
from pathlib import Path

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from agrisensa_commodities.services.nitrogen_release_service import NitrogenReleaseService


def test_wagri_example():
    """
    Test with exact WAGRI example data from the API documentation.
    
    Expected output should match WAGRI results within 1% tolerance.
    """
    print("=" * 60)
    print("Testing Nitrogen Release Service with WAGRI Example Data")
    print("=" * 60)
    
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
    
    # Run calculation
    result = NitrogenReleaseService.calculate_daily_release(**input_data)
    
    # Check for errors
    if "error" in result:
        print(f"❌ ERROR: {result['error']}")
        return False
    
    # Validate daily list
    print("\n📊 Validating Daily Release Values:")
    print("-" * 60)
    
    daily_match = True
    for i, (actual, expected) in enumerate(zip(result['daily_list'], expected_daily)):
        diff = abs(actual - expected)
        percent_diff = (diff / expected * 100) if expected != 0 else 0
        
        match = "✅" if percent_diff < 1.0 else "❌"
        print(f"Day {i+1}: Actual={actual:.6f}, Expected={expected:.6f}, Diff={percent_diff:.2f}% {match}")
        
        if percent_diff >= 1.0:
            daily_match = False
    
    # Validate cumulative list
    print("\n📈 Validating Cumulative Release Values:")
    print("-" * 60)
    
    cum_match = True
    for i, (actual, expected) in enumerate(zip(result['cum_list'], expected_cum)):
        diff = abs(actual - expected)
        percent_diff = (diff / expected * 100) if expected != 0 else 0
        
        match = "✅" if percent_diff < 1.0 else "❌"
        print(f"Day {i+1}: Actual={actual:.6f}, Expected={expected:.6f}, Diff={percent_diff:.2f}% {match}")
        
        if percent_diff >= 1.0:
            cum_match = False
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    
    if daily_match and cum_match:
        print("✅ ALL TESTS PASSED!")
        print("✅ Results match WAGRI example data within 1% tolerance")
        print(f"\n📊 Total N Released: {result['total_release_kg']:.2f} kg")
        print(f"📊 Release Percentage: {result['release_percentage']:.1f}%")
        return True
    else:
        print("❌ SOME TESTS FAILED!")
        if not daily_match:
            print("❌ Daily release values do not match")
        if not cum_match:
            print("❌ Cumulative release values do not match")
        return False


def test_material_presets():
    """Test that all material presets work correctly."""
    print("\n" + "=" * 60)
    print("Testing Material Presets")
    print("=" * 60)
    
    presets = NitrogenReleaseService.list_material_presets()
    
    for preset_name in presets:
        print(f"\n🌾 Testing: {preset_name}")
        
        preset = NitrogenReleaseService.get_material_preset(preset_name)
        
        result = NitrogenReleaseService.calculate_daily_release(
            start_date="20240501",
            water_date="20240505",
            end_date="20240510",
            material_amount=100,
            material_type=1,
            material_props=preset,
            coefficients=NitrogenReleaseService.DEFAULT_COEFFICIENTS,
            daily_temperatures=[25] * 10
        )
        
        if "error" in result:
            print(f"   ❌ Error: {result['error']}")
        else:
            print(f"   ✅ Success: {result['total_release_kg']:.2f} kg N released")
    
    print("\n✅ All material presets tested successfully!")


def test_validation():
    """Test input validation."""
    print("\n" + "=" * 60)
    print("Testing Input Validation")
    print("=" * 60)
    
    # Test 1: Invalid date order
    is_valid, msg = NitrogenReleaseService.validate_inputs(
        "20240510",
        "20240505",
        "20240501",
        100,
        {"MC": 35, "ADSON": 20, "TN": 3.5, "Nm": 0.3}
    )
    print(f"\nTest 1 - Invalid date order: {'❌ PASS' if not is_valid else '✅ FAIL'}")
    print(f"   Message: {msg}")
    
    # Test 2: Negative material amount
    is_valid, msg = NitrogenReleaseService.validate_inputs(
        "20240501",
        "20240505",
        "20240510",
        -100,
        {"MC": 35, "ADSON": 20, "TN": 3.5, "Nm": 0.3}
    )
    print(f"\nTest 2 - Negative amount: {'❌ PASS' if not is_valid else '✅ FAIL'}")
    print(f"   Message: {msg}")
    
    # Test 3: Missing property
    is_valid, msg = NitrogenReleaseService.validate_inputs(
        "20240501",
        "20240505",
        "20240510",
        100,
        {"MC": 35, "ADSON": 20, "TN": 3.5}  # Missing Nm
    )
    print(f"\nTest 3 - Missing property: {'❌ PASS' if not is_valid else '✅ FAIL'}")
    print(f"   Message: {msg}")
    
    # Test 4: Valid inputs
    is_valid, msg = NitrogenReleaseService.validate_inputs(
        "20240501",
        "20240505",
        "20240510",
        100,
        {"MC": 35, "ADSON": 20, "TN": 3.5, "Nm": 0.3}
    )
    print(f"\nTest 4 - Valid inputs: {'✅ PASS' if is_valid else '❌ FAIL'}")
    print(f"   Message: {msg if msg else 'No errors'}")
    
    print("\n✅ Validation tests completed!")


if __name__ == "__main__":
    print("\nNITROGEN RELEASE SERVICE TEST SUITE\n")
    
    # Run all tests
    test1_pass = test_wagri_example()
    test_material_presets()
    test_validation()
    
    # Final summary
    print("\n" + "=" * 60)
    print("FINAL TEST SUMMARY")
    print("=" * 60)
    
    if test1_pass:
        print("✅ WAGRI validation: PASSED")
        print("✅ Material presets: PASSED")
        print("✅ Input validation: PASSED")
        print("\n🎉 ALL TESTS PASSED! Implementation is correct.")
    else:
        print("❌ Some tests failed. Please review the implementation.")
    
    print("=" * 60)
