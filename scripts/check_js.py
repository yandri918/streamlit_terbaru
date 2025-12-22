with open('templates/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Lines around DOMContentLoaded (455-465):")
for i in range(455, 465):
    print(f'{i+1}: {lines[i].rstrip()}')

print("\n\nChecking if script is inside <script> tags:")
script_start = -1
script_end = -1
for i, line in enumerate(lines):
    if '<script>' in line:
        script_start = i
        print(f"<script> tag at line {i+1}")
    if '</script>' in line:
        script_end = i
        print(f"</script> tag at line {i+1}")

if script_start > 0 and script_end > 0:
    print(f"\nScript block: lines {script_start+1} to {script_end+1}")
    print(f"DOMContentLoaded at line 460")
    if script_start < 460 < script_end:
        print("✅ DOMContentLoaded is INSIDE script tags")
    else:
        print("❌ DOMContentLoaded is OUTSIDE script tags!")
