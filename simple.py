import sys

def fast_input():
    return sys.stdin.readline().rstrip("\r\n")

def fast_output(x):
    sys.stdout.write(str(x) + "\n")

def max_salary_after_deletion(t, test_cases):
    results = []
    for s in test_cases:
        if len(s) == 1:
            results.append("0")
        else:
            max_number = 0
            for i in range(len(s)):
                temp_number = int(s[:i] + s[i+1:])
                max_number = max(max_number, temp_number)
            results.append(str(max_number))
    return results

t = int(fast_input())
test_cases = [fast_input() for _ in range(t)]

results = max_salary_after_deletion(t, test_cases)

for result in results:
    fast_output(result)
