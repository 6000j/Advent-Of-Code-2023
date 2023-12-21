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
num_steps = 22
# This is the number of loops we do from the start to another start in a straight line
num_borders = num_steps // x_len
num_borders = max(num_borders-1, 0)
# num_good_borders = num_borders if num_borders % 2 == 0 else
# Remaining steps after we hit a border
remaining_steps = num_steps % x_len
num_remaining_steps = num_steps - num_borders * x_len

# Four triangles, which then have extra chunks in them lol
num_full_squares = max(0, 2*(num_borders)*(num_borders+1))

# Now we calculate the partially completed counts:
top_left_count = 0
top_right_count = 0
bottom_left_count = 0
bottom_right_count = 0

# Getting our values
# The current issue is that the diagonals will have overlap with each other, so we must somehow figure out how to account for that :(
tiles_at = set()
tiles_at.add(start_tile)
print(x_len, y_len)
print(tiles_at)
print("Remaining steps:", num_remaining_steps)
for i in range(num_remaining_steps):
    new_tiles_at = set()
    for tile in tiles_at:
        new_tiles_at.update(get_infinite_adjacents(tile, x_len, y_len))
    new_tiles_at.difference_update(bad_tiles)
    tiles_at = new_tiles_at

top_left_count = len([[lc] for lc in tiles_at if (lc[0] < start_tile[0] and lc[1] < start_tile[1])])
top_right_count = len([[lc] for lc in tiles_at if (lc[0] < start_tile[0] and lc[1] > start_tile[1])])
bottom_left_count = len([[lc] for lc in tiles_at if (lc[0] > start_tile[0] and lc[1] < start_tile[1])])
bottom_right_count = len([[lc] for lc in tiles_at if (lc[0] > start_tile[0] and lc[1] > start_tile[1])])
print("Top Left:", top_left_count)
print("Top Right:", top_right_count)
print("Bottom Left:", bottom_left_count)
print("Bottom Right:", bottom_right_count)
# lines_count = len()
total = 0

# If this isn't even, it's BAD
# Note that we can pair each side with each other to resolve parity issues, which makes this far nicer
full_squares_cover = (((x_len-1)*(y_len-1)-len(bad_tiles))*num_full_squares)/2
total += full_squares_cover
# print("Just in full squares:", total)
# Now we're going to add the number of diagonals:
from_diagonals = (num_borders+2)*(top_left_count + top_right_count + bottom_left_count + bottom_right_count)
total += from_diagonals
# And now we have to calculate our scores on the lines themselves
# How many lines do we have???
# Full lines count:
# This is actually really dumb that this works, but
full_lines_count = 4 * pow(num_borders+1, 2)
# print("Full Lines:", full_lines_count)
partial_line_components = num_steps % x_len
# print("Lengths of partial lines", partial_line_components)
full_lines_score = full_lines_count / 2
total += full_lines_score
partial_line_score = 4 * (partial_line_components // 2 + ((num_borders+1)%2))
total += partial_line_score
# print(len(tiles_at))
# Printing our output nicely:
print("Total:", total)
print("\tJust full squares:", full_squares_cover)
print("\t\tNumber of full squares:", num_full_squares)
print("\tDiagonals:", from_diagonals)
print("\tFull Lines:", full_lines_score)
print("\t\tNumber of Full Lines:", full_lines_count)
print("\tPartial Lines:", partial_line_score)
print("\t\tLengths of partial lines", partial_line_components)









# print(x_len, y_len)
# tiles_at = set()
# tiles_at.add(start_tile)
# print(tiles_at)
# old_tiles_at = [set(), set()]
# for i in range(200):
#     if old_tiles_at[i%2] == tiles_at:
#         break
#     else:
#         old_tiles_at[i%2] = tiles_at.copy()
#     new_tiles_at = set()
#     for tile in tiles_at:
#         new_tiles_at.update(get_infinite_adjacents(tile, x_len, y_len))
#     new_tiles_at.difference_update(bad_tiles)
#     tiles_at = new_tiles_at


# print(len(tiles_at))

# print(i)
# print("Evens:", len(old_tiles_at[0]), ", Odds:", len(old_tiles_at[1]))