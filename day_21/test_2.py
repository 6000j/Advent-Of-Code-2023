# Day 21 problem 2
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
def get_adjacents_0(location, x_len, y_len):
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

@cache
def get_adjacents(location, x_len, y_len):
    oup = set()
    oup.add((location[0]-1, location[1]))
    oup.add((location[0]+1, location[1]))
    oup.add((location[0], location[1]-1))
    oup.add((location[0], location[1]+1))
    # else:
    #     print("error")
    oup.difference_update(bad_tiles)
    return oup
@cache
def get_infinite_adjacents(location, x_len, y_len):
    xfactor = location[0] // x_len
    yfactor = location[1] // y_len
    oup = set()

    for mini_loc in get_adjacents((location[0] % x_len, location[1]% y_len), x_len, y_len):
        oup.add((mini_loc[0] + x_len*xfactor, mini_loc[1] + y_len*yfactor))
        # oup.add(mini_loc)
    return oup
    

f = open("input_1.txt", 'r')
f = open("test_input.txt", 'r')
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

'''
Here's the idea:
- We note that because the border of the garden has no rocks, the fastest way to ever enter a garden would be to use the borders as a network! 
- In fact, there are no rocks directly from either side of S! This means we can use it as a border by itself!
- So, we want to look at how long it takes us to get to various places I think?
'''
num_steps = 26501365
num_steps = 5


print(x_len, y_len)
tiles_at = set()
tiles_at.add(start_tile)
print(tiles_at)
# old_tiles_at = [set(), set()]
for i in range(num_steps):
    # if old_tiles_at[i%2] == tiles_at:
    #     break
    # else:
    #     old_tiles_at[i%2] = tiles_at.copy()
    new_tiles_at = set()
    for tile in tiles_at:
        new_tiles_at.update(get_infinite_adjacents(tile, x_len, y_len))
    new_tiles_at.difference_update(bad_tiles)
    tiles_at = new_tiles_at


print(len(tiles_at))

# print(i)
# print("Evens:", len(old_tiles_at[0]), ", Odds:", len(old_tiles_at[1]))