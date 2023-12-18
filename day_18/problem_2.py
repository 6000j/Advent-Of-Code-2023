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
    UP = 3
    DOWN = 1
    RIGHT = 0
    LEFT = 2
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


# @cache
def move_forwards_3(location, direct, dist):
    if direct == direction.UP:
        return (location[0]-dist, location[1])
    elif direct == direction.DOWN:
        return (location[0]+dist, location[1])
    elif direct == direction.LEFT:
        return (location[0], location[1]-dist)
    elif direct == direction.RIGHT:
        return (location[0], location[1]+dist)
    else:
        print("error")

def move_and_paint(location, direct, distance, dug_out):
    curr_location = location
    curr_location = move_forwards_3(curr_location, direct, distance)
    # Adding the new edge
    add_location = curr_location
    # if direct == direction.UP:
    #     add_location = (add_location[0]+0.5, add_location[1])
    # elif direct == direction.DOWN:
    #     add_location = (add_location[0]-0.5, add_location[1])
    # elif direct == direction.LEFT:
    #     add_location = (add_location[0], add_location[1]+0.5)
    # elif direct == direction.RIGHT:
    #     add_location = (add_location[0], add_location[1]+0.5)
    
    # if len(dug_out) > 0:
    #     if direct == direction.UP or direct == direction.DOWN:
    #         add_location = (add_location[0]+0.5, add_location[1])
    #     elif direct == direction.DOWN:
    #         add_location = (add_location[0]+0.5, add_location[1])
    #     elif direct == direction.LEFT:
    #         add_location = (add_location[0], add_location[1]+0.5)
    #     elif direct == direction.RIGHT:
    #         add_location = (add_location[0], add_location[1]+0.5)
    dug_out.append(add_location)
    # if last_direct == direction.UP:
    #     add_location = (add_location[0]-0.5, add_location[1])
    # elif last_direct == direction.DOWN:
    #     add_location = (add_location[0]+0.5, add_location[1])
    # elif last_direct == direction.LEFT:
    #     add_location = (add_location[0], add_location[1]-0.5)
    # elif last_direct == direction.RIGHT:
    #     add_location = (add_location[0], add_location[1]+0.5)
    # dug_out.append(add_location)
    return curr_location

def hex_to_instructions(hex_colour):
    oup_dist = int(hex_colour[0:5], 16)
    dir_num = int(hex_colour[5])
    if dir_num == 0:
        oup_direction = direction.RIGHT
    elif dir_num == 1:
        oup_direction = direction.DOWN
    elif dir_num == 2:
        oup_direction = direction.LEFT
    elif dir_num == 3:
        oup_direction = direction.UP    
    
    # oup_direction = direction(int(hex_colour[5]))
    # print((oup_direction, oup_dist))
    return (oup_direction, oup_dist)

    

f = open("input_1.txt", 'r')
# f = open("test_input.txt", 'r')
lines = f.readlines()
f.close()

painted_edges = []
line_instructions = []

# First we want to get the sizes of our area:
for line in lines:
    d_char, dist_char, code_brack = line.strip().split()
    curr_hex_code = code_brack[2:-1]
    line_instructions.append(hex_to_instructions(curr_hex_code))


# line_instructions = [(direction.RIGHT, 6), (direction.DOWN, 5), (direction.LEFT, 2), (direction.DOWN, 2), (direction.RIGHT, 2), (direction.DOWN, 2), (direction.LEFT, 5), (direction.UP, 2), (direction.LEFT, 1), (direction.UP, 2), (direction.RIGHT, 2), (direction.UP, 3), (direction.LEFT, 2), (direction.UP, 2)]
# line_instructions = [(direction.RIGHT, 1), (direction.DOWN, 1), (direction.LEFT, 1), (direction.UP, 1)]
# performing our instructions
min_x = 0
max_x = 0
min_y = 0
max_y = 0
curr_location = (0,0)
prev_direct = direction.UP
for instr in line_instructions:
    # print(instr)
    curr_location = move_and_paint(curr_location, instr[0], instr[1], painted_edges)
    prev_direct = instr[0]
    # print(curr_location)
    # if curr_location[0] < min_x:
    #     min_x = curr_location[0]
    # if curr_location[0] > max_x:
    #     max_x = curr_location[0]
    # if curr_location[1] < min_y:
    #     min_y = curr_location[1]
    # if curr_location[1] > max_y:
    #     max_y = curr_location[1]
# for i in range(len(painted_edges)):
#     painted_edges[i] = (painted_edges[i][0] - min_x, painted_edges[i][1] - min_y)


# def unhappy(a, b, is_max):
#     # print(a, b)
#     checkers = []
#     for k in [-0.5, 0.5]:
#         for j in [-0.5, 0.5]:
#             checkers.append((a+k) * (b+j))
#     # print(checkers)
#     if is_max:
#         return max(checkers)
#     else:
        # return min(checkers)
        
# print(painted_edges[0], painted_edges[-1])
# painted_edges = [(0,0), (0,3), (2,3), (2,2), (1, 2), (1, 1), (2, 1), (2, 0)]
# print(painted_edges[0], painted_edges[-1])
print(painted_edges)
# painted_edges[-1] = (0,0)
# Shoelace formula tech!
total_options = [0, 0, 0, 0]
total = 0
for i in range(len(painted_edges)):
    
    total += painted_edges[i][0] * painted_edges[(i+1) % len(painted_edges)][1]
    total -= painted_edges[i][1] * painted_edges[(i+1) % len(painted_edges)][0]
    # # 0: Min, Min
    # total_options[0] += unhappy(painted_edges[i][0], painted_edges[(i+1) % len(painted_edges)][1], False)
    # total_options[0] -= unhappy(painted_edges[i][1], painted_edges[(i+1) % len(painted_edges)][0], False)
    # # 1: Min, Max
    # total_options[0] += unhappy(painted_edges[i][0], painted_edges[(i+1) % len(painted_edges)][1], False)
    # total_options[0] -= unhappy(painted_edges[i][1], painted_edges[(i+1) % len(painted_edges)][0], True)
    # # 2: Max, Min
    # total_options[0] += unhappy(painted_edges[i][0], painted_edges[(i+1) % len(painted_edges)][1], True)
    # total_options[0] -= unhappy(painted_edges[i][1], painted_edges[(i+1) % len(painted_edges)][0], False)
    # # 3: Max, Max
    # total_options[0] += unhappy(painted_edges[i][0], painted_edges[(i+1) % len(painted_edges)][1], True)
    # total_options[0] -= unhappy(painted_edges[i][1], painted_edges[(i+1) % len(painted_edges)][0], True)

# print(type(total))
# total += painted_edges[len(painted_edges)-1][0] * painted_edges[0][1]
# total -= painted_edges[len(painted_edges)-1][1] * painted_edges[0][0]
# print(type(total))
total = abs(total/2)

for i in range(len(total_options)):
    total_options[i] = abs(total_options[i]/2)
    print(total_options[i])
print(max(total_options))


perim_length = 0
old_vertex = (0,0)
for vertex in painted_edges:
    perim_length += abs(vertex[0] - old_vertex[0]) + abs(vertex[1] - old_vertex[1])
    old_vertex = vertex
total += perim_length/2 + 1
print(total)
# # # print(type(total))

# Getting our actual map of locations:
# real_map = [['.' for _ in range(0, max_y-min_y+1)] for _ in range(0, max_x-min_x+1)]
# x_len = len(real_map)
# y_len = len(real_map[0])
# print(x_len, y_len)

# for plot in painted_edges:
#     real_map[plot[0][0]-min_x][plot[0][1]-min_y] = '#'

# # for line in real_map:
# #     print(''.join(line))

# # Edges for flood fill
# for k in range(0, x_len):
#     if real_map[k][0] != '#':
#         real_map[k][0] = '*'
#     if real_map[k][y_len-1] != '#':
#         real_map[k][y_len-1] = '*'
# for k in range(0, y_len):
#     if real_map[0][k] != '#':
#         real_map[0][k] = '*'
#     if real_map[x_len-1][k] != '#':
#         real_map[x_len-1][k] = '*'


# done = False
# while not done:
#     new_real_map = copy.deepcopy(real_map)
#     # print_nice_contained(larger_map)
#     for x in range(x_len):
#         for y in range(y_len):
#             if real_map[x][y] != '#' and  real_map[x][y] != '*':
#                 if real_map[x-1][y] == '*':
#                     new_real_map[x][y] = '*'
#                 if real_map[x+1][y] == '*':
#                     new_real_map[x][y] = '*'
#                 if real_map[x][y-1] == '*':
#                     new_real_map[x][y] = '*'
#                 if real_map[x][y+1] == '*':
#                     new_real_map[x][y] = '*'
#     if new_real_map == real_map:
#         done = True
#     real_map = new_real_map

# # for line in real_map:
# #     print(''.join(line))

# oup = 0
# for k in real_map:
#     oup += k.count('#')
#     oup += k.count('.')
# print(oup)