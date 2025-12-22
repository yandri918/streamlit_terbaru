with open('templates/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
print("\nChecking lines around 1040-1045:")
for i in range(1035, min(1045, len(lines))):
    print(f"Line {i+1}: {lines[i].rstrip()}")

# Check bracket balance
open_brackets = 0
close_brackets = 0
open_parens = 0
close_parens = 0

for i, line in enumerate(lines):
    if i >= 445:  # Start from script tag
        open_brackets += line.count('{')
        close_brackets += line.count('}')
        open_parens += line.count('(')
        close_parens += line.count(')')

print(f"\n\nBracket balance in script:")
print(f"Open {{ : {open_brackets}")
print(f"Close }} : {close_brackets}")
print(f"Difference: {open_brackets - close_brackets}")

print(f"\nParenthesis balance:")
print(f"Open ( : {open_parens}")
print(f"Close ) : {close_parens}")
print(f"Difference: {open_parens - close_parens}")

if open_brackets != close_brackets:
    print(f"\n❌ FOUND PROBLEM: Missing {open_brackets - close_brackets} closing brackets }}")
elif open_parens != close_parens:
    print(f"\n❌ FOUND PROBLEM: Missing {open_parens - close_parens} closing parenthesis )")
else:
    print("\n✅ All brackets and parenthesis are balanced")
