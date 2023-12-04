# Day 4 problem 1

f = open("input_1.txt", 'r')
lines = f.readlines()
f.close()

# Preprocessing
for v in range(0, len(lines)):
    lines[v] = lines[v].strip()
for i in range(len(lines)):
    lines[i] = lines[i].split(':')[1].strip()

total = 0
# This is easy, right?
for line in lines:
    curr_score = 0
    (win_line, have_line) = line.split("|")
    win_line = win_line.strip()
    have_line = have_line.strip()
    win_nums = [int(val) for val in win_line.split()]
    have_nums = [int(val) for val in have_line.split()]
    for have in have_nums:
        if have in win_nums:
            if curr_score == 0:
                curr_score = 1
            else:
                curr_score = curr_score*2
    total += curr_score

print(total)
    