"""
Script to integrate pest database expansion into main service
This will merge 32 additional entries from pest_database_expansion.py into pest_disease_service.py
"""

import sys
import os

# Add path
sys.path.insert(0, 'c:/Users/yandr/OneDrive/Desktop/agrisensa-api')

# Import the expansion data
from agrisensa_commodities.services.pest_database_expansion import (
    RICE_ADDITIONAL_PESTS,
    RICE_ADDITIONAL_DISEASES,
    CORN_ADDITIONAL_PESTS,
    CORN_ADDITIONAL_DISEASES,
    TOMATO_ADDITIONAL_PESTS,
    TOMATO_ADDITIONAL_DISEASES,
    CHILI_ADDITIONAL_PESTS,
    CHILI_ADDITIONAL_DISEASES,
    SOYBEAN_ADDITIONAL_PESTS,
    SOYBEAN_ADDITIONAL_DISEASES
)

# Import the main service
from agrisensa_commodities.services.pest_disease_service import PestDiseaseService

# Count entries
rice_new = len(RICE_ADDITIONAL_PESTS) + len(RICE_ADDITIONAL_DISEASES)
corn_new = len(CORN_ADDITIONAL_PESTS) + len(CORN_ADDITIONAL_DISEASES)
tomato_new = len(TOMATO_ADDITIONAL_PESTS) + len(TOMATO_ADDITIONAL_DISEASES)
chili_new = len(CHILI_ADDITIONAL_PESTS) + len(CHILI_ADDITIONAL_DISEASES)
soybean_new = len(SOYBEAN_ADDITIONAL_PESTS) + len(SOYBEAN_ADDITIONAL_DISEASES)

total_new = rice_new + corn_new + tomato_new + chili_new + soybean_new

print("=" * 60)
print("PEST DATABASE EXPANSION INTEGRATION")
print("=" * 60)
print(f"\nNew entries to add:")
print(f"  Rice:    {rice_new} entries ({len(RICE_ADDITIONAL_PESTS)} pests + {len(RICE_ADDITIONAL_DISEASES)} diseases)")
print(f"  Corn:    {corn_new} entries ({len(CORN_ADDITIONAL_PESTS)} pests + {len(CORN_ADDITIONAL_DISEASES)} diseases)")
print(f"  Tomato:  {tomato_new} entries ({len(TOMATO_ADDITIONAL_PESTS)} pests + {len(TOMATO_ADDITIONAL_DISEASES)} diseases)")
print(f"  Chili:   {chili_new} entries ({len(CHILI_ADDITIONAL_PESTS)} pests + {len(CHILI_ADDITIONAL_DISEASES)} diseases)")
print(f"  Soybean: {soybean_new} entries ({len(SOYBEAN_ADDITIONAL_PESTS)} pests + {len(SOYBEAN_ADDITIONAL_DISEASES)} diseases)")
print(f"\n  TOTAL NEW: {total_new} entries")

# Get current database status
ps = PestDiseaseService()
crops = ps.get_available_crops()
current_total = sum(c['pest_count'] + c['disease_count'] for c in crops)

print(f"\n  Current database: {current_total} entries")
print(f"  After integration: {current_total + total_new} entries")
print("\n" + "=" * 60)

# Now we need to modify the PEST_DATABASE in the service file
# We'll read the file, find the sections, and insert the new data

file_path = 'agrisensa_commodities/services/pest_disease_service.py'

print(f"\nReading {file_path}...")

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("✓ File read successfully")
print(f"  File size: {len(content)} bytes")

# We'll create a backup first
backup_path = file_path + '.backup_before_expansion'
with open(backup_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✓ Backup created: {backup_path}")

print("\n✅ Ready for integration!")
print("\nNext steps:")
print("1. Manually add entries to each crop section in pest_disease_service.py")
print("2. OR use a text editor to copy-paste from pest_database_expansion.py")
print("3. Test the service after integration")
