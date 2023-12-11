# Day 11 problem 1

# Taken from https://www.geeksforgeeks.org/python-transpose-elements-of-two-dimensional-list/
def transpose(inp):
    oup = [[row[i] for row in inp] for i in range(len(inp[0]))]
    return oup

# def get_dist_between(gala, galb, free_rows, free_columns):
    

f = open("input_1.txt", 'r')
# f = open("test_input.txt", 'r')
lines = f.readlines()
f.close()

lines = [line.strip() for line in lines]

# for line in lines:
#     print(''.join(line))
# print('----')
galaxy_rows = []
galaxy_columns = []
new_lines = []
for i in range(0, len(lines)):
    line = lines[i]
    new_lines.append(line)
    if line.count('#') == 0:
        galaxy_rows.append(i)
        # for i in range(0, 1000000):
        #     new_lines.append(line)

new_lines = transpose(new_lines)
new_new_lines = []
for i in range(len(new_lines)):
    line = new_lines[i]
    new_new_lines.append(line)
    if line.count('#') == 0:
        galaxy_columns.append(i)
        # for i in range(0, 1000000):
        #     new_new_lines.append(line)


lines = transpose(new_new_lines)
# for line in lines:
#     print(''.join(line))
# print("Empty Rows:", galaxy_rows)
# print("Empty Columns:", galaxy_columns)
# Now we need to calculate distances:
galaxies = []
for x in range(len(lines)):
    for y in range(len(lines[0])):
        if lines[x][y] == '#':
            galaxies.append((x,y))
# print("Galaxies", galaxies)

scale_factor = pow(10, 6)
total = 0
for galaxy in galaxies:
    for other_galaxy in galaxies:
        for i in range(min(galaxy[0], other_galaxy[0]), max(galaxy[0], other_galaxy[0])):
            if i in galaxy_rows:
                total += scale_factor
            else:
                total += 1
        for j in range(min(galaxy[1], other_galaxy[1]), max(galaxy[1], other_galaxy[1])):
            if j in galaxy_columns:
                total += scale_factor
            else:
                total += 1
        
total = total / 2

print(total)