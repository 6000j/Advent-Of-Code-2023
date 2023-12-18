# Day 17 problem 1
from enum import Enum
from functools import cache

grid_map = []
# distances_map = 
end_of_map = (10000, 10000)
current_best = 103
seen_with = {}

# max_steps = 500


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


other_directions_list = {
    direction.UP:[direction.RIGHT, direction.LEFT, direction.UP],
    direction.DOWN:[direction.DOWN, direction.RIGHT, direction.LEFT],
    direction.LEFT:[direction.DOWN, direction.LEFT, direction.UP],
    direction.RIGHT:[direction.RIGHT, direction.DOWN, direction.UP],
    direction.ANY:[direction.RIGHT, direction.DOWN, direction.UP, direction.LEFT]
}

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


def heat_to_end_from(location, direct, moves_in_direction, num_steps, running_total, start_of=False):
    global current_best
    # print(location)
    # visited = [k for k in old_visited]
    # if num_steps > 10*len(grid_map):
    #     return 100000
    if running_total > current_best:
        # print("aha")
        return 100000
    
    temp = 0
    if (location, direct, moves_in_direction) in seen_with.keys() and seen_with[(location, direct, moves_in_direction)] < 100000: # and seen_with[(location, direct, moves_in_direction)][1] <= num_steps:
        return seen_with[(location, direct, moves_in_direction)]
        # return seen_with[(location, direct, moves_in_direction)]
        temp = seen_with[(location, direct, moves_in_direction)]
    # if (num_steps > max_steps):
    #     return 100000
    x = location[0]
    y = location[1]
    
    if (x < 0) or (x > len(grid_map)-1) or (y < 0) or (y > len(grid_map) - 1):
        return 100000
    
        
    # visited.append(location)
    if start_of == True:
        # print("hi")
        oup = 0
    elif location == (0, 0):
        return 100000
    else:
        oup = grid_map[x][y]

    if location == end_of_map:
        # print("ended", num_steps)
        return oup
    
    # new_visited = visited.copy()
    # if (x, y) in visited:
    #     return 10000000
    # new_visited.append(location)

    directions_to_check = other_directions_list[direct].copy()
    # print(directions_to_check)
    if moves_in_direction >= 3:
        directions_to_check.remove(direct)
    
    # if x <= 0 and (direction.UP in directions_to_check):
    #     directions_to_check.remove(direction.UP)
    # if x >= len(grid_map)-1 and (direction.DOWN in directions_to_check):
    #     directions_to_check.remove(direction.DOWN)
    # if y <= 0 and (direction.LEFT in directions_to_check):
    #     directions_to_check.remove(direction.LEFT)
    # if y >= len(grid_map[0])-1 and (direction.RIGHT in directions_to_check):
    #     directions_to_check.remove(direction.RIGHT)
    # print(location, directions_to_check)
    
    direction_scores = []
    
    for c_direct in directions_to_check:
        
        if c_direct == direct:
            wo = heat_to_end_from(move_forwards_2(location, c_direct), c_direct, moves_in_direction + 1, num_steps + 1, running_total+oup)
            if location == (0,0):
                print(wo)
                current_best = min([current_best, wo])
            direction_scores.append(wo)
        else:
            wo = heat_to_end_from(move_forwards_2(location, c_direct), c_direct, 1,                      num_steps + 1, running_total+oup)
            if location == (0,0):
                print(wo)
                current_best = min([current_best, wo])
            direction_scores.append(wo)
        

    if len(direction_scores) == 0:
        # print(direct)
        print("BAD")
        print(location, end_of_map, location == end_of_map)
        print(x, y, direct, moves_in_direction)
        return 100000
    # print(direction_scores)

    oup += min(direction_scores)
    if oup > current_best:
        # print("Shit")
        oup = 100000
    
    if ((location, direct, moves_in_direction) in seen_with.keys()) and (seen_with[(location, direct, moves_in_direction)] < oup):
        # print("idfk")
        oup = seen_with[(location, direct, moves_in_direction)]
    elif oup < 100000:
        # for k in range(1, moves_in_direction+1):
        #     if ((location, direct, k) in seen_with.keys()):
        #         if (seen_with[(location, direct, k)][0] >= num_steps) and (seen_with[(location, direct, k)][1] > oup):
        #             seen_with[(location, direct, k)] = (num_steps, oup)
        #     else:
        #         seen_with[(location, direct, k)] = (num_steps, oup)
        if ((location, direct, moves_in_direction) in seen_with.keys()): # and (seen_with[(location, direct, moves_in_direction)][0] >= num_steps) and (seen_with[(location, direct, moves_in_direction)][1] > oup):
            seen_with[(location, direct, moves_in_direction)] = oup# (num_steps, oup)
        else:
            seen_with[(location, direct, moves_in_direction)] = oup # (num_steps, oup)
        
    # for k in seen_with:
    #     print(k, grid_map[k[0][0]][k[0][1]], seen_with[k])
    # print("")
    # if temp != 0:
        # print("Oup:", oup, "Comparison", temp)
    return oup

@cache
def heat_map(location, direct, moves_in_direction, running_total, start_of=False):
    global current_best
    # print(location)
    # visited = [k for k in old_visited]
    # if num_steps > 10*len(grid_map):
    #     return 100000
    x = location[0]
    y = location[1]
    if (x < 0) or (x > len(grid_map)-1) or (y < 0) or (y > len(grid_map) - 1):
        return None
    if start_of == True:
        # print("hi")
        oup = 0
    elif location == (0, 0):
        return None
    else:
        oup = grid_map[x][y]
    score = running_total + oup
    if score > current_best:
        # print("aha")
        return None
    elif (location, direct, moves_in_direction) in seen_with.keys() and seen_with[(location, direct, moves_in_direction)] < score: # and seen_with[(location, direct, moves_in_direction)][1] <= num_steps:
        return None
    else:
        for k in range(1, moves_in_direction+1):
            if ((location, direct, k) in seen_with.keys()):
                if (seen_with[(location, direct, k)] > score):
                    seen_with[(location, direct, k)] = score
            else:
                seen_with[(location, direct, k)] = score
        if location == end_of_map:
            return None
        else:
            directions_to_check = other_directions_list[direct].copy()
            # print(directions_to_check)
            if moves_in_direction >= 3:
                directions_to_check.remove(direct)
            
            # if x <= 0 and (direction.UP in directions_to_check):
            #     directions_to_check.remove(direction.UP)
            # if x >= len(grid_map)-1 and (direction.DOWN in directions_to_check):
            #     directions_to_check.remove(direction.DOWN)
            # if y <= 0 and (direction.LEFT in directions_to_check):
            #     directions_to_check.remove(direction.LEFT)
            # if y >= len(grid_map[0])-1 and (direction.RIGHT in directions_to_check):
            #     directions_to_check.remove(direction.RIGHT)
            # print(location, directions_to_check)
            
            for c_direct in directions_to_check:              
                if c_direct == direct:
                    heat_map(move_forwards_2(location, c_direct), c_direct, moves_in_direction + 1, score)
                else:
                    heat_map(move_forwards_2(location, c_direct), c_direct, 1, score)

        return None


# ???
f = open("input_1.txt", 'r')
# f = open("test_input.txt", 'r')
lines = f.readlines()
f.close()

grid_map = []
for line in lines:
    grid_map.append([int(i) for i in line.strip()])

end_of_map = (len(grid_map)-1, len(grid_map[0])-1)
# print(end_of_map)
current_best = sum([sum(line) for line in grid_map])


curr_location = (0, 0)
test_list = [direction.RIGHT, direction.DOWN] * (len(grid_map)-1)
# print(test_list)
min_total = 0
for d in test_list:
    curr_location = move_forwards_2(curr_location, d)
    # print(curr_location, grid_map[curr_location[0]][curr_location[1]])
    min_total += grid_map[curr_location[0]][curr_location[1]]
current_best = min_total
# current_best = 103
# print(current_best)

heat_map((0,0), direction.ANY, 0, 0, start_of=True)
wins = 100000
# oup = heat_to_end_from((0,0), direction.ANY, 0, 0, 0, start_of = True)
print("Just getting keys now lmao")
for k in seen_with.keys():
    if k[0] == end_of_map:
        # print(seen_with[k])
        wins = min(wins, seen_with[k])
print(wins)
# print(oup)
# for k in seen_with:
#     print(k, grid_map[k[0][0]][k[0][1]], seen_with[k])
# print(seen_with)
# print(other_directions_list)
    
# curr_location = (0, 0)
# test_list = [direction.RIGHT, direction.RIGHT, direction.DOWN, direction.RIGHT, direction.RIGHT, direction.RIGHT, direction.UP,
            #   direction.RIGHT, direction.RIGHT, direction.RIGHT, direction.DOWN, direction.DOWN, direction.RIGHT, direction.RIGHT, direction.DOWN
            #   , direction.DOWN, direction.RIGHT, direction.DOWN, direction.DOWN, direction.DOWN, direction.RIGHT, direction.DOWN
            #   , direction.DOWN, direction.DOWN, direction.LEFT, direction.DOWN, direction.DOWN, direction.RIGHT]
# print(len(test_list))
# min_total = 0
# for d in test_list:
#     curr_location = move_forwards_2(curr_location, d)
#     print(curr_location, grid_map[curr_location[0]][curr_location[1]])
#     min_total += grid_map[curr_location[0]][curr_location[1]]
# print(min_total)
    
