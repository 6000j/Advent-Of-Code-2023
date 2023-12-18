# Day 18 problem 1
from functools import cache
from enum import Enum
import copy
# Taken from https://www.geeksforgeeks.org/python-transpose-elements-of-two-dimensional-list/
def transpose(inp):
    # print(len(inp))
    # print(len(inp[0]))
    oup = [[row[i] for row in inp] for i in range(len(inp[0]))]
    return oup

class direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4
    ANY = 5

@cache
def move_forwards_2(location, direct):
    if direct == direction.UP:
        return (location[0]-1, location[1])
    elif direct == direction.DOWN:
        return (location[0]+1, location[1])
    elif direct == direction.LEFT:
        return (location[0], location[1]-1)
    elif direct == direction.RIGHT:
        return (location[0], location[1]+1)
    else:
        print("error")

def move_and_paint(location, direct, distance, colour_code, dug_out):
    curr_location = location
    # Adding the new edge
    dug_out.append((location, direct, colour_code))
    for _ in range(distance):
        curr_location = move_forwards_2(curr_location, direct)
        dug_out.append((curr_location, direct, colour_code))
    return curr_location
    

f = open("input_1.txt", 'r')
f = open("test_input.txt", 'r')
lines = f.readlines()
f.close()

painted_edges = []
line_instructions = []

# First we want to get the sizes of our area:
for line in lines:
    d_char, dist_char, code_brack = line.strip().split()
    if d_char == 'D':
        curr_direct = direction.DOWN
    elif d_char == 'U':
        curr_direct = direction.UP
    elif d_char == 'L':
        curr_direct = direction.LEFT
    elif d_char == 'R':
        curr_direct = direction.RIGHT
    curr_dist = int(dist_char)
    curr_hex_code = code_brack[1:-1]
    line_instructions.append((curr_direct, curr_dist, curr_hex_code))


# performing our instructions
min_x = 0
max_x = 0
min_y = 0
max_y = 0
curr_location = (0,0)
for instr in line_instructions:
    curr_location = move_and_paint(curr_location, instr[0], instr[1], instr[2], painted_edges)
    print(curr_location)
    if curr_location[0] < min_x:
        min_x = curr_location[0]
    if curr_location[0] > max_x:
        max_x = curr_location[0]
    if curr_location[1] < min_y:
        min_y = curr_location[1]
    if curr_location[1] > max_y:
        max_y = curr_location[1]

# Getting our actual map of locations:
real_map = [['.' for _ in range(0, max_y-min_y+1)] for _ in range(0, max_x-min_x+1)]
x_len = len(real_map)
y_len = len(real_map[0])
print(x_len, y_len)

for plot in painted_edges:
    real_map[plot[0][0]-min_x][plot[0][1]-min_y] = '#'

# for line in real_map:
#     print(''.join(line))

# Edges for flood fill
for k in range(0, x_len):
    if real_map[k][0] != '#':
        real_map[k][0] = '*'
    if real_map[k][y_len-1] != '#':
        real_map[k][y_len-1] = '*'
for k in range(0, y_len):
    if real_map[0][k] != '#':
        real_map[0][k] = '*'
    if real_map[x_len-1][k] != '#':
        real_map[x_len-1][k] = '*'


done = False
while not done:
    new_real_map = copy.deepcopy(real_map)
    # print_nice_contained(larger_map)
    for x in range(x_len):
        for y in range(y_len):
            if real_map[x][y] != '#' and  real_map[x][y] != '*':
                if real_map[x-1][y] == '*':
                    new_real_map[x][y] = '*'
                if real_map[x+1][y] == '*':
                    new_real_map[x][y] = '*'
                if real_map[x][y-1] == '*':
                    new_real_map[x][y] = '*'
                if real_map[x][y+1] == '*':
                    new_real_map[x][y] = '*'
    if new_real_map == real_map:
        done = True
    real_map = new_real_map

# for line in real_map:
#     print(''.join(line))

oup = 0
for k in real_map:
    oup += k.count('#')
    oup += k.count('.')
print(oup)

print(line_instructions)