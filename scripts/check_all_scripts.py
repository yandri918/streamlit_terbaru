with open('templates/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("All <script> and </script> tags:")
for i, line in enumerate(lines):
    if '<script' in line.lower() or '</script>' in line.lower():
        print(f"Line {i+1}: {line.rstrip()}")

print("\n\nChecking script tag balance:")
script_count = 0
for i, line in enumerate(lines):
    if '<script' in line.lower():
        script_count += 1
        print(f"Line {i+1}: OPEN (count: {script_count})")
    if '</script>' in line.lower():
        script_count -= 1
        print(f"Line {i+1}: CLOSE (count: {script_count})")

if script_count == 0:
    print("\n✅ All script tags are balanced")
else:
    print(f"\n❌ Script tags NOT balanced! Count: {script_count}")
