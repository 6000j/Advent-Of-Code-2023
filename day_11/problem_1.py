# Day 11 problem 1

# Taken from https://www.geeksforgeeks.org/python-transpose-elements-of-two-dimensional-list/
def transpose(inp):
    oup = [[row[i] for row in inp] for i in range(len(inp[0]))]
    return oup

f = open("input_1.txt", 'r')
# f = open("test_input.txt", 'r')
lines = f.readlines()
f.close()

lines = [line.strip() for line in lines]

# for line in lines:
#     print(''.join(line))
# print('----')
new_lines = []
for line in lines:
    new_lines.append(line)
    if line.count('#') == 0:
        new_lines.append(line)

new_new_lines = []
for line in transpose(new_lines):
    new_new_lines.append(line)
    if line.count('#') == 0:
        new_new_lines.append(line)


lines = transpose(new_new_lines)
# for line in lines:
#     print(''.join(line))

# Now we need to calculate distances:
galaxies = []
for x in range(len(lines)):
    for y in range(len(lines[0])):
        if lines[x][y] == '#':
            galaxies.append((x,y))

total = 0
for galaxy in galaxies:
    for other_galaxy in galaxies:
        total += abs(galaxy[0] - other_galaxy[0]) + abs(galaxy[1] - other_galaxy[1])
total = total / 2

print(total)