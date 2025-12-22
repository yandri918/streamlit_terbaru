with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# The DOMContentLoaded starts at line 460 and never closes
# We need to add }); before </script>

old_ending = """            });

    </script>"""

new_ending = """            });
        }); // Close DOMContentLoaded event listener

    </script>"""

content = content.replace(old_ending, new_ending)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Added closing bracket for DOMContentLoaded!")

# Verify
with open('templates/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

open_b = 0
close_b = 0
for i, line in enumerate(lines):
    if i >= 445:
        open_b += line.count('{')
        close_b += line.count('}')

print(f"\nVerification:")
print(f"Open {{ : {open_b}")
print(f"Close }} : {close_b}")
if open_b == close_b:
    print("✅ ALL BRACKETS NOW BALANCED!")
else:
    print(f"❌ Still missing {open_b - close_b} brackets")
