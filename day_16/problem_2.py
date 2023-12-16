# Day 16 problem 2
from enum import Enum

visited = []
locations_been = []

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

def move_forwards(location, direct):
    if direct == direction.UP:
        return (location[0], location[1]-1)
    elif direct == direction.DOWN:
        return (location[0], location[1]+1)
    elif direct == direction.LEFT:
        return (location[0]-1, location[1])
    elif direct == direction.RIGHT:
        return (location[0]+1, location[1])
    else:
        print("error")


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


def beam_path(grid, location, direct: direction):
    
    curr_location = (location[0], location[1])
    curr_direction = direct
    while (curr_location, curr_direction) not in visited:
        
        x = curr_location[0]
        y = curr_location[1]
        # print(curr_location, curr_direction)

        if x < 0 or x >= len(grid) or y < 0 or y >= len(grid[0]):
            break
        curr_tile = grid[x][y]
        locations_been[x][y] = True
        visited.append((curr_location, curr_direction))
        # print(curr_location, curr_direction, curr_tile)
        if curr_tile == '/':
            # visited.append((curr_location, curr_direction))
            if curr_direction == direction.UP:
                curr_direction = direction.RIGHT
            elif curr_direction == direction.DOWN:
                curr_direction = direction.LEFT
            elif curr_direction == direction.LEFT:
                curr_direction = direction.DOWN
            elif curr_direction == direction.RIGHT:
                curr_direction = direction.UP
            curr_location = move_forwards_2(curr_location, curr_direction)
        elif curr_tile == '\\': 
            # visited.append((curr_location, curr_direction))
            if curr_direction == direction.UP:
                curr_direction = direction.LEFT
            elif curr_direction == direction.DOWN:
                curr_direction = direction.RIGHT
            elif curr_direction == direction.LEFT:
                curr_direction = direction.UP
            elif curr_direction == direction.RIGHT:
                curr_direction = direction.DOWN
            curr_location = move_forwards_2(curr_location, curr_direction)
        elif curr_tile == "|" and (curr_direction == direction.RIGHT or curr_direction == direction.LEFT):
            # visited.append((curr_location, curr_direction))
            # locations_been[x][y] = True
            beam_path(grid, curr_location, direction.UP)
            beam_path(grid, curr_location, direction.DOWN)
            # print("split updown at", curr_location, curr_direction)
            break
        elif curr_tile == '-' and (curr_direction == direction.UP or curr_direction == direction.DOWN):
            # visited.append((curr_location, curr_direction))
            # locations_been[x][y] = True
            beam_path(grid, curr_location, direction.LEFT)
            beam_path(grid, curr_location, direction.RIGHT)
            # print("split leftright at", curr_location, curr_direction)
            break
        else:
            # Next tile function body
            # visited.append((curr_location, curr_direction))
            curr_location = move_forwards_2(curr_location, curr_direction)
        

            


    # return locations_been

f = open("input_1.txt", 'r')
# f = open("test_input.txt", 'r')
lines = f.readlines()
f.close()

grid_map = []
for line in lines:
    grid_map.append(list(line.strip()))

# 
# grid_map = transpose(grid_map)
# for line in grid_map:
#     print(''.join(line))
# print(len(grid_map), len(grid_map[0]))
locations_been = [[False for _ in range(len(grid_map[0]))] for _ in range(len(grid_map))]
# locations_nice = [['.' for _ in range(len(grid_map[0]))] for _ in range(len(grid_map))]
# locations_nice = [grid_map[i].copy() for i in range(len(grid_map))]
# beam_path(grid_map, (0,0), direction.RIGHT)
scores = []
for i in range(len(grid_map)):
    # Going Right
    total = 0
    visited = []
    locations_been = [[False for _ in range(len(grid_map[0]))] for _ in range(len(grid_map))]
    beam_path(grid_map, (i,0), direction.RIGHT)
    for line in locations_been:
        total += line.count(True)
    scores.append(total)
    # Going Left
    total = 0
    visited = []
    locations_been = [[False for _ in range(len(grid_map[0]))] for _ in range(len(grid_map))]
    beam_path(grid_map, (i, len(grid_map)), direction.LEFT)
    for line in locations_been:
        total += line.count(True)
    scores.append(total)
    
    # Going Down
    total = 0
    visited = []
    locations_been = [[False for _ in range(len(grid_map[0]))] for _ in range(len(grid_map))]
    beam_path(grid_map, (0, i), direction.DOWN)
    for line in locations_been:
        total += line.count(True)
    scores.append(total)
    # Going Up
    total = 0
    visited = []
    locations_been = [[False for _ in range(len(grid_map[0]))] for _ in range(len(grid_map))]
    beam_path(grid_map, (len(grid_map), i), direction.UP)
    for line in locations_been:
        total += line.count(True)
    scores.append(total)
    
print(max(scores))


# print("")
# for vs in visited:
#     x, y = vs[0][0], vs[0][1]
#     curr_direction = vs[1]
#     if grid_map[x][y] != '.':
#         locations_nice[x][y] = grid_map[x][y]
#     elif locations_nice[x][y] == '.':
#         if curr_direction == direction.UP:
#             locations_nice[x][y] = '^'
#         elif curr_direction == direction.DOWN:
#             locations_nice[x][y] = 'v'
#         elif curr_direction == direction.LEFT:
#             locations_nice[x][y] = '<'
#         elif curr_direction == direction.RIGHT:
#             locations_nice[x][y] = '>'
#     elif locations_nice[x][y].isdigit():
#         locations_nice[x][y] = str(int(locations_nice[x][y]) + 1)
#     else:
#         locations_nice[x][y] = "2"

# for ln in locations_nice:
#     print(''.join(ln))

# print(len(set([vs[0] for vs in visited])))
# print(total)