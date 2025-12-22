with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the duplicate DOMContentLoaded
lines = content.split('\n')
dom_loaded_lines = []

for i, line in enumerate(lines):
    if 'document.addEventListener' in line and 'DOMContentLoaded' in line:
        dom_loaded_lines.append(i)
        print(f"Found DOMContentLoaded at line {i+1}")

if len(dom_loaded_lines) >= 2:
    print(f"\nFound {len(dom_loaded_lines)} DOMContentLoaded declarations")
    print("Removing the duplicate one...")
    
    # Remove the second DOMContentLoaded and its closing bracket
    # Find the second occurrence and remove it along with its content
    second_start = dom_loaded_lines[1]
    
    # Find the closing of the second DOMContentLoaded
    bracket_count = 0
    second_end = second_start
    for i in range(second_start, len(lines)):
        if '{' in lines[i]:
            bracket_count += lines[i].count('{')
        if '}' in lines[i]:
            bracket_count -= lines[i].count('}')
        if bracket_count == 0 and i > second_start:
            second_end = i
            break
    
    # Remove lines from second_start to second_end
    new_lines = lines[:second_start] + lines[second_end+1:]
    
    # Write back
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print(f"Removed lines {second_start+1} to {second_end+1}")
    print("File fixed!")
else:
    print("No duplicate found")
