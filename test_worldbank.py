"""Test World Bank Service."""
import sys
sys.path.insert(0, 'C:\\Users\\yandr\\OneDrive\\Desktop\\agrisensa-api')

from app.services.worldbank_service import WorldBankService

print("Testing World Bank Service...")
print("=" * 50)

# Test 1: Get available products
print("\n1. Available Products:")
products = WorldBankService.get_all_available_products()
for p in products[:10]:  # Show first 10
    print(f"   - {p}")

# Test 2: Get price for specific commodity
print("\n2. Testing Price Fetch for 'cabai_merah_keriting':")
result = WorldBankService.get_price_for_commodity('cabai_merah_keriting')
if result:
    print(f"   Average Price: Rp {result['average_price']:,}")
    print(f"   Sample Size: {result['sample_size']} records")
    print(f"   Latest Date: {result['latest_date']}")
    print(f"   Markets: {', '.join(result['markets'][:3])}")
else:
    print("   No data found")

# Test 3: Get price for rice
print("\n3. Testing Price Fetch for 'beras_medium':")
result = WorldBankService.get_price_for_commodity('beras_medium')
if result:
    print(f"   Average Price: Rp {result['average_price']:,}")
    print(f"   Sample Size: {result['sample_size']} records")
else:
    print("   No data found")
