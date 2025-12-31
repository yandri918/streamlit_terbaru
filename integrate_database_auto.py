"""
AUTOMATED PEST DATABASE INTEGRATION SCRIPT
==========================================
This script will automatically integrate 29 additional pest/disease entries
from pest_database_expansion.py into pest_disease_service.py

Total: 24 (current) + 29 (new) = 53 entries

Author: AgriSensa Team
Date: 2025-12-31
"""

import os
import shutil
from datetime import datetime

print("=" * 70)
print("AUTOMATED PEST DATABASE INTEGRATION")
print("=" * 70)
print()

# File paths
SERVICE_FILE = 'agrisensa_commodities/services/pest_disease_service.py'
EXPANSION_FILE = 'agrisensa_commodities/services/pest_database_expansion.py'
BACKUP_FILE = f'{SERVICE_FILE}.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'

# Step 1: Create backup
print(f"Step 1: Creating backup...")
shutil.copy2(SERVICE_FILE, BACKUP_FILE)
print(f"✓ Backup created: {BACKUP_FILE}")
print()

# Step 2: Read files
print("Step 2: Reading files...")
with open(SERVICE_FILE, 'r', encoding='utf-8') as f:
    service_content = f.read()

with open(EXPANSION_FILE, 'r', encoding='utf-8') as f:
    expansion_content = f.read()

print(f"✓ Service file: {len(service_content)} bytes")
print(f"✓ Expansion file: {len(expansion_content)} bytes")
print()

# Step 3: Import expansion data
print("Step 3: Loading expansion data...")
import sys
sys.path.insert(0, os.getcwd())

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

print(f"✓ Rice: {len(RICE_ADDITIONAL_PESTS)} pests + {len(RICE_ADDITIONAL_DISEASES)} diseases")
print(f"✓ Corn: {len(CORN_ADDITIONAL_PESTS)} pests + {len(CORN_ADDITIONAL_DISEASES)} diseases")
print(f"✓ Tomato: {len(TOMATO_ADDITIONAL_PESTS)} pests + {len(TOMATO_ADDITIONAL_DISEASES)} diseases")
print(f"✓ Chili: {len(CHILI_ADDITIONAL_PESTS)} pests + {len(CHILI_ADDITIONAL_DISEASES)} diseases")
print(f"✓ Soybean: {len(SOYBEAN_ADDITIONAL_PESTS)} pests + {len(SOYBEAN_ADDITIONAL_DISEASES)} diseases")

total_new = (len(RICE_ADDITIONAL_PESTS) + len(RICE_ADDITIONAL_DISEASES) +
             len(CORN_ADDITIONAL_PESTS) + len(CORN_ADDITIONAL_DISEASES) +
             len(TOMATO_ADDITIONAL_PESTS) + len(TOMATO_ADDITIONAL_DISEASES) +
             len(CHILI_ADDITIONAL_PESTS) + len(CHILI_ADDITIONAL_DISEASES) +
             len(SOYBEAN_ADDITIONAL_PESTS) + len(SOYBEAN_ADDITIONAL_DISEASES))

print(f"\n✓ Total new entries: {total_new}")
print()

# Step 4: Load current database and merge
print("Step 4: Merging databases...")
from agrisensa_commodities.services.pest_disease_service import PestDiseaseService

# Get the PEST_DATABASE from the service
ps = PestDiseaseService()
PEST_DATABASE = ps.PEST_DATABASE.copy()

# Merge Rice
PEST_DATABASE['rice']['pests'].extend(RICE_ADDITIONAL_PESTS)
PEST_DATABASE['rice']['diseases'].extend(RICE_ADDITIONAL_DISEASES)
print(f"✓ Rice: {len(PEST_DATABASE['rice']['pests'])} pests + {len(PEST_DATABASE['rice']['diseases'])} diseases")

# Merge Corn
PEST_DATABASE['corn']['pests'].extend(CORN_ADDITIONAL_PESTS)
PEST_DATABASE['corn']['diseases'].extend(CORN_ADDITIONAL_DISEASES)
print(f"✓ Corn: {len(PEST_DATABASE['corn']['pests'])} pests + {len(PEST_DATABASE['corn']['diseases'])} diseases")

# Merge Tomato
PEST_DATABASE['tomato']['pests'].extend(TOMATO_ADDITIONAL_PESTS)
PEST_DATABASE['tomato']['diseases'].extend(TOMATO_ADDITIONAL_DISEASES)
print(f"✓ Tomato: {len(PEST_DATABASE['tomato']['pests'])} pests + {len(PEST_DATABASE['tomato']['diseases'])} diseases")

# Merge Chili
PEST_DATABASE['chili']['pests'].extend(CHILI_ADDITIONAL_PESTS)
PEST_DATABASE['chili']['diseases'].extend(CHILI_ADDITIONAL_DISEASES)
print(f"✓ Chili: {len(PEST_DATABASE['chili']['pests'])} pests + {len(PEST_DATABASE['chili']['diseases'])} diseases")

# Merge Soybean
PEST_DATABASE['soybean']['pests'].extend(SOYBEAN_ADDITIONAL_PESTS)
PEST_DATABASE['soybean']['diseases'].extend(SOYBEAN_ADDITIONAL_DISEASES)
print(f"✓ Soybean: {len(PEST_DATABASE['soybean']['pests'])} pests + {len(PEST_DATABASE['soybean']['diseases'])} diseases")

# Calculate totals
total_pests = sum(len(PEST_DATABASE[crop]['pests']) for crop in PEST_DATABASE)
total_diseases = sum(len(PEST_DATABASE[crop]['diseases']) for crop in PEST_DATABASE)
grand_total = total_pests + total_diseases

print(f"\n✓ GRAND TOTAL: {total_pests} pests + {total_diseases} diseases = {grand_total} entries")
print()

# Step 5: Generate new service file
print("Step 5: Generating new service file...")

import json

# Convert PEST_DATABASE to formatted string
def dict_to_python_str(obj, indent=0):
    """Convert dict/list to properly formatted Python code string"""
    ind = "    " * indent
    
    if isinstance(obj, dict):
        lines = ["{"]
        items = list(obj.items())
        for i, (key, value) in enumerate(items):
            comma = "," if i < len(items) - 1 else ""
            if isinstance(value, (dict, list)):
                val_str = dict_to_python_str(value, indent + 1)
                lines.append(f'{ind}    "{key}": {val_str}{comma}')
            elif isinstance(value, str):
                # Escape quotes in strings
                escaped = value.replace('"', '\\"')
                lines.append(f'{ind}    "{key}": "{escaped}"{comma}')
            else:
                lines.append(f'{ind}    "{key}": {value}{comma}')
        lines.append(f'{ind}}}')
        return '\n'.join(lines)
    
    elif isinstance(obj, list):
        if not obj:
            return "[]"
        lines = ["["]
        for i, item in enumerate(obj):
            comma = "," if i < len(obj) - 1 else ""
            if isinstance(item, (dict, list)):
                item_str = dict_to_python_str(item, indent + 1)
                lines.append(f'{ind}    {item_str}{comma}')
            elif isinstance(item, str):
                escaped = item.replace('"', '\\"')
                lines.append(f'{ind}    "{escaped}"{comma}')
            else:
                lines.append(f'{ind}    {item}{comma}')
        lines.append(f'{ind}]')
        return '\n'.join(lines)
    
    return str(obj)

# Find where PEST_DATABASE starts and ends in the original file
import re

# Find the PEST_DATABASE definition
db_start = service_content.find('PEST_DATABASE = {')
if db_start == -1:
    print("✗ ERROR: Could not find PEST_DATABASE in service file")
    exit(1)

# Find the end of PEST_DATABASE (look for the closing brace followed by method definition)
# We'll look for the pattern "    }\n    \n    @staticmethod" or similar
db_end_pattern = r'\n    \}\n    \n    @staticmethod'
match = re.search(db_end_pattern, service_content[db_start:])
if match:
    db_end = db_start + match.start() + len('\n    }')
else:
    print("✗ ERROR: Could not find end of PEST_DATABASE")
    exit(1)

# Generate new PEST_DATABASE string
new_db_str = "PEST_DATABASE = " + dict_to_python_str(PEST_DATABASE, 1)

# Replace old database with new one
new_content = service_content[:db_start] + new_db_str + service_content[db_end:]

# Write to new file
OUTPUT_FILE = 'agrisensa_commodities/services/pest_disease_service_NEW.py'
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"✓ New service file generated: {OUTPUT_FILE}")
print(f"  File size: {len(new_content)} bytes")
print()

# Step 6: Verification
print("Step 6: Verifying integration...")
print("  Testing if new file can be imported...")

try:
    # Try to import the new service
    import importlib.util
    spec = importlib.util.spec_from_file_location("pest_disease_service_new", OUTPUT_FILE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Create service instance
    new_ps = module.PestDiseaseService()
    new_crops = new_ps.get_available_crops()
    new_total = sum(c['pest_count'] + c['disease_count'] for c in new_crops)
    
    print(f"✓ New service imported successfully")
    print(f"✓ Verified total: {new_total} entries")
    
    if new_total == grand_total:
        print(f"✓ Entry count matches! ({new_total} == {grand_total})")
    else:
        print(f"⚠ Warning: Entry count mismatch ({new_total} != {grand_total})")
    
except Exception as e:
    print(f"✗ Error importing new service: {e}")
    print("  The file may have syntax errors. Please review manually.")

print()
print("=" * 70)
print("INTEGRATION COMPLETE!")
print("=" * 70)
print()
print("Next steps:")
print(f"1. Review the new file: {OUTPUT_FILE}")
print(f"2. If everything looks good, replace the original:")
print(f"   - Delete or rename: {SERVICE_FILE}")
print(f"   - Rename: {OUTPUT_FILE} -> {SERVICE_FILE}")
print(f"3. Backup is saved at: {BACKUP_FILE}")
print(f"4. Update UI to show '53 entries' instead of '50+'")
print(f"5. Test the application")
print()
print("✅ All done!")
