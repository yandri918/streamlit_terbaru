with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add console.log right after DOMContentLoaded
old_code = "        document.addEventListener('DOMContentLoaded', () => {\n            const baseUrl = window.location.origin;"

new_code = """        document.addEventListener('DOMContentLoaded', () => {
            console.log('🚀 AgriSensa: DOMContentLoaded fired!');
            console.log('🔧 Initializing event listeners...');
            const baseUrl = window.location.origin;
            console.log('📍 Base URL:', baseUrl);"""

content = content.replace(old_code, new_code)

# Add console.log for each form submission
forms_to_debug = [
    ('formBwd.addEventListener', 'Modul 1: BWD Analysis'),
    ('formRec.addEventListener', 'Modul 2: Recommendation'),
    ('formNpk.addEventListener', 'Modul 3: NPK Analysis'),
    ('priceForm.addEventListener', 'Modul 4: Price Check'),
]

for form_code, module_name in forms_to_debug:
    if form_code in content:
        # Find the line and add console.log
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if form_code in line and 'submit' in line:
                # Add console.log after event.preventDefault()
                for j in range(i, min(i+5, len(lines))):
                    if 'event.preventDefault()' in lines[j]:
                        lines[j] = lines[j] + f"\n                console.log('📝 {module_name}: Form submitted!');"
                        break
        content = '\n'.join(lines)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Debug logs added to index.html")
print("Now user should see console logs when:")
print("1. Page loads: '🚀 AgriSensa: DOMContentLoaded fired!'")
print("2. Form submits: '📝 Modul X: Form submitted!'")
