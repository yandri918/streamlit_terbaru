"""
Fix notebook markdown formatting - convert \\n to proper line breaks
"""

import json

# Fix Notebook 2
with open('notebooks/2_Yield_Prediction_Model.ipynb', 'r') as f:
    nb2 = json.load(f)

# Fix markdown cells - convert string with \\n to list of lines
for cell in nb2['cells']:
    if cell['cell_type'] == 'markdown':
        if isinstance(cell['source'], str):
            # Split by \\n and create list
            cell['source'] = cell['source'].replace('\\n', '\n').split('\n')
            # Add newline to each line except last
            cell['source'] = [line + '\n' if i < len(cell['source'])-1 else line 
                            for i, line in enumerate(cell['source'])]

# Save fixed notebook
with open('notebooks/2_Yield_Prediction_Model.ipynb', 'w') as f:
    json.dump(nb2, f, indent=2)

# Fix Notebook 3
with open('notebooks/3_Price_Forecasting_Analysis.ipynb', 'r') as f:
    nb3 = json.load(f)

for cell in nb3['cells']:
    if cell['cell_type'] == 'markdown':
        if isinstance(cell['source'], str):
            cell['source'] = cell['source'].replace('\\n', '\n').split('\n')
            cell['source'] = [line + '\n' if i < len(cell['source'])-1 else line 
                            for i, line in enumerate(cell['source'])]

with open('notebooks/3_Price_Forecasting_Analysis.ipynb', 'w') as f:
    json.dump(nb3, f, indent=2)

print("✅ Notebooks fixed!")
print("Markdown cells now display properly without \\n")
