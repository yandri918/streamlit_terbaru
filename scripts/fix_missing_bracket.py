with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add missing closing bracket and parenthesis before </script>
# The DOMContentLoaded event listener needs to be closed properly

old_ending = """            });

    </script>"""

new_ending = """            });
        }); // Close DOMContentLoaded

    </script>"""

content = content.replace(old_ending, new_ending)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed missing bracket and parenthesis!")
print("Added: }); // Close DOMContentLoaded")

# Verify fix
with open('templates/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

open_brackets = 0
close_brackets = 0
for i, line in enumerate(lines):
    if i >= 445:
        open_brackets += line.count('{')
        close_brackets += line.count('}')

print(f"\nVerification:")
print(f"Open {{ : {open_brackets}")
print(f"Close }} : {close_brackets}")
if open_brackets == close_brackets:
    print("✅ Brackets are now balanced!")
else:
    print(f"❌ Still missing {open_brackets - close_brackets} brackets")
