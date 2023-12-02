f = open("problem_1_input.txt", 'r')

total = 0
for line in f:
    curr_line = 0
    for c in line:
        if c.isdigit():
            curr_line += 10*int(c)
            break
    for c in reversed(line):
        if c.isdigit():
            curr_line += int(c)
            break
    total += curr_line

print(total)
