with open('templates/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Track bracket balance line by line
balance = 0
problem_lines = []

for i, line in enumerate(lines):
    if i >= 445:  # Start from script tag
        open_count = line.count('{')
        close_count = line.count('}')
        balance += (open_count - close_count)
        
        if open_count > 0 or close_count > 0:
            print(f"Line {i+1}: balance={balance:+3d} | {line.rstrip()[:80]}")
        
        # Track where balance goes negative (too many closing brackets)
        if balance < 0:
            problem_lines.append((i+1, balance, line.rstrip()))

print(f"\n\nFinal balance: {balance}")
if balance > 0:
    print(f"❌ Missing {balance} closing brackets }}")
elif balance < 0:
    print(f"❌ Too many closing brackets: {-balance}")
else:
    print("✅ Balanced!")

if problem_lines:
    print("\n\nLines where balance went negative:")
    for line_num, bal, content in problem_lines:
        print(f"Line {line_num}: balance={bal} | {content[:80]}")

# Check the last few lines before </script>
print("\n\nLast 10 lines before </script>:")
for i in range(len(lines)-10, len(lines)):
    print(f"Line {i+1}: {lines[i].rstrip()}")
