"""Quick fix script for yield_benchmarks.py"""

# Read the file
with open('app/data/yield_benchmarks.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the syntax error: change {"Laris", "Gada"} to ["Laris", "Gada"]
content = content.replace('"high": {"Laris", "Gada"},', '"high": ["Laris", "Gada"],')

# Write back
with open('app/data/yield_benchmarks.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed yield_benchmarks.py")
