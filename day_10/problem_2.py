# Day 10 problem 1
import copy

# Taken from https://www.geeksforgeeks.org/python-transpose-elements-of-two-dimensional-list/
def transpose(inp):
    oup = [[row[i] for row in inp] for i in range(len(inp[0]))]
    return oup

def get_next_location(curr_location, prev_location, pipe, return_both = False):
    # Pipe is a character
    locations_pot = []
    curr_x = curr_location[0]
    curr_y = curr_location[1]
    if pipe == '|':
       locations_pot = [(curr_x, curr_y+1), (curr_x, curr_y-1)]
    elif pipe == '-':
        locations_pot = [(curr_x+1, curr_y), (curr_x-1, curr_y)]
    elif pipe == 'L':
        locations_pot = [(curr_x, curr_y-1), (curr_x+1, curr_y)]
    elif pipe == 'J':
        locations_pot = [(curr_x, curr_y-1), (curr_x-1, curr_y)]
    elif pipe == '7':
        locations_pot = [(curr_x, curr_y+1), (curr_x-1, curr_y)]
    elif pipe == 'F':
        locations_pot = [(curr_x, curr_y+1), (curr_x+1, curr_y)]
    elif pipe == 'S':
        # print("Found the starting position at", curr_location)
        locations_pot = ['S', 'tart']
    else:
        # print("bad")
        locations_pot = ['Bad', 'bad'] 
    
    if return_both:
        return locations_pot
    elif locations_pot[0] != prev_location:
        return locations_pot[0]
    else:
        return locations_pot[1]

def find_connecting_tiles_from_the_start(pipe_map, fix_map = False):
    x_length = len(pipe_map)
    y_length = len(pipe_map[0])
    start_x = None
    start_y = None
    for x in range(x_length):
        for y in range(y_length):
            if pipe_map[x][y] == 'S':
                start_x = x
                start_y = y
                break
    if start_x is None or start_y is None:
        print("Emergency")

    above = False
    below = False
    left = False
    right = False
    start_pos = (start_x, start_y)
    start_tile_type = None
    # now we do this stuff
    x = start_x
    y = start_y
    if start_x > 0:
        if start_pos in get_next_location((start_x-1, start_y), start_pos, pipe_map[x-1][y], return_both=True):
            left = True
    if start_x < (x_length-1):
        if start_pos in get_next_location((start_x+1, start_y), start_pos, pipe_map[x+1][y], return_both=True):
            right = True
    if start_y > 0:
        if start_pos in get_next_location((start_x, start_y-1), start_pos, pipe_map[x][y-1], return_both=True):
            above = True
    if start_y < (y_length-1):
        if start_pos in get_next_location((start_x, start_y+1), start_pos, pipe_map[x][y+1], return_both=True):
            below = True
    if left:
        if right:
            start_tile_type = '-'
        if above:
            start_tile_type = 'J'
        if below:
            start_tile_type = '7'
    elif right:
        if above:
            start_tile_type = 'L'
        if below:
            start_tile_type = 'F'
    else:
        start_tile_type = '|'
    
    # Now we map out the whole thing
    
    starting_to_check = None
    tiles_in_loop = []
    if above:
        starting_to_check = (start_x, start_y-1)
    elif below:
        starting_to_check = (start_x, start_y+1)
    elif left:
        starting_to_check = (start_x-1, start_y)
    # print("above", above, "below", below, "Left", left, "right", right)

    tiles_in_loop.append(start_pos)
    curr_tile = starting_to_check
    prev_tile = start_pos
    while curr_tile != start_pos:
        # print(curr_tile)
        tiles_in_loop.append(curr_tile)
        new_curr_tile = get_next_location(curr_tile, prev_tile, pipe_map[curr_tile[0]][curr_tile[1]])
        prev_tile = curr_tile
        curr_tile = new_curr_tile

    # For use with part 2
    if fix_map:
        new_map = pipe_map.copy()
        new_map[start_x][start_y] = start_tile_type
        return new_map
    else:
        return tiles_in_loop

def create_larger_map(pipe_map, loop):
    above = ['|', 'J', 'L']
    below = ['|', '7', 'F']
    left = ['-', 'J', '7']
    right = ['-', 'L', 'F']

    huge_map = [['.' for _ in range(2*len(pipe_map[0]))] for _ in range(2*len(pipe_map))]
    for x in range(len(pipe_map)):
        for y in range(len(pipe_map)):
            if (x,y) in loop:
                loc_val = pipe_map[x][y]
                huge_map[2*x][2*y] = loc_val
                if loc_val in above:
                    huge_map[2*x][2*y - 1] = '|'
                if loc_val in below:
                    huge_map[2*x][2*y + 1] = '|'
                if loc_val in left:
                    huge_map[2*x - 1][2*y] = '-'
                if loc_val in right:
                    huge_map[2*x + 1][2*y] = '-'
    print("x:", len(huge_map), "y:", len(huge_map[0]))
    return huge_map

def get_enclosed(pipe_map, loop):
    parts_list = ['-', '|', 'F', 'J', '7', 'L']
    good_map = find_connecting_tiles_from_the_start(pipe_map, fix_map=True)
    larger_map = create_larger_map(good_map, loop)
    print_nice_contained(larger_map)
    x_len = len(larger_map)
    y_len = len(larger_map[0])
    for x in range(x_len):
        if larger_map[x][0] not in parts_list:
            larger_map[x][0] = '*'
        if larger_map[x][y_len-1] not in parts_list:
            larger_map[x][y_len-1] = '*'
    for y in range(y_len):
        if larger_map[0][y] not in parts_list:
            larger_map[0][y] = '*'
        if larger_map[x_len-1][y] not in parts_list:
            larger_map[x_len-1][y] = '*'
    done = False
    while not done:
        new_larger_map = copy.deepcopy(larger_map)
        # print_nice_contained(larger_map)
        for x in range(x_len):
            for y in range(y_len):
                if larger_map[x][y] not in parts_list and larger_map[x][y] != '*':
                    if larger_map[x-1][y] == '*':
                        new_larger_map[x][y] = '*'
                    if larger_map[x+1][y] == '*':
                        new_larger_map[x][y] = '*'
                    if larger_map[x][y-1] == '*':
                        new_larger_map[x][y] = '*'
                    if larger_map[x][y+1] == '*':
                        new_larger_map[x][y] = '*'
        if new_larger_map == larger_map:
            done = True
        larger_map = new_larger_map
    # print_nice_contained(larger_map)

    total = 0
    for x in range(x_len//2):
        for y in range(y_len//2):
            if larger_map[2*x][2*y] == '.':
                total += 1
    return total






def print_nice_contained(contained):
    oup = ""
    for line in transpose(contained):
        for elt in line:
            oup+=elt
        oup += '\n'
    print(oup)





f = open("input_1.txt", 'r')
f = open("test_input.txt", 'r')
lines = f.readlines()
f.close()

pipe_map = []
for line in lines:
    pipe_map.append(line.strip())

print("X", len(pipe_map), "Y", len(pipe_map[0]))
pipe_map = transpose(pipe_map)
print("X", len(pipe_map), "Y", len(pipe_map[0]))
loop_map = find_connecting_tiles_from_the_start(pipe_map)

total = get_enclosed(pipe_map, loop_map)

print(total)