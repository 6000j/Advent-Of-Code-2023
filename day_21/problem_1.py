# Day 21 problem 1
from enum import Enum
from functools import cache

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

@cache
def get_adjacents(location, x_len, y_len):
    oup = set()
    if location[0] > 0:
        oup.add((location[0]-1, location[1]))
    if location[0] < x_len-1:
        oup.add((location[0]+1, location[1]))
    if location[1] > 0:
        oup.add((location[0], location[1]-1))
    if location[1] < y_len - 1:
        oup.add((location[0], location[1]+1))
    # else:
    #     print("error")
    return oup

f = open("input_1.txt", 'r')
# f = open("test_input.txt", 'r')
lines = f.readlines()
f.close()

start_tile = (-8, -8)
grid_map = []
for line in lines:
    grid_map.append([i for i in line.strip()])

bad_tiles = set()
# Naive solution that won't scale up (don't worry, I have a solution that should scale up in theory for when part 2 wants that lol)
x_len = len(grid_map)
y_len = len(grid_map[0])
for x in range(x_len):
    for y in range(y_len):
        if grid_map[x][y] == '#':
            bad_tiles.add((x,y))
        elif grid_map[x][y] == 'S':
            start_tile = (x,y)

tiles_at = set()
tiles_at.add(start_tile)
print(tiles_at)
for i in range(64):
    new_tiles_at = set()
    for tile in tiles_at:
        new_tiles_at.update(get_adjacents(tile, x_len, y_len))
    new_tiles_at.difference_update(bad_tiles)
    tiles_at = new_tiles_at

print(len(tiles_at))
