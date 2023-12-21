# Day 17 problem 1
from enum import Enum
from functools import cache
from operator import itemgetter, attrgetter

grid_map = []
# distances_map = 
end_of_map = (10000, 10000)

seen_with = {}

# max_steps = 500

class Node:
    def __init__(self, location, direct, moves_in_direction, cost) -> None:
        self.location = location
        self.direct = direct
        self.moves_in_direction = moves_in_direction
        self.cost = cost
        self.neighbours = []
        self.distance = 100000
        self.visited = False
        self.in_modded = False

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


def create_layout(grid_map):
    temp_dict = {}
    x_len = len(grid_map)
    y_len = len(grid_map[0])

    # This sets up alllll our stuff
    for x in range(x_len):
        for y in range(y_len):
            for direct in [direction.UP, direction.DOWN, direction.LEFT, direction.RIGHT]:
                for moves_in_direction in range(1, 11):
                    temp_dict[((x, y), direct, moves_in_direction)] = Node((x,y), direct, moves_in_direction, grid_map[x][y])

    # Hardcoding start and end
    start = Node((0,0), direction.ANY, 0, 0)
    for direct in [direction.UP, direction.DOWN, direction.LEFT, direction.RIGHT]:
        for moves_in_direction in range(1, 11):
            temp_dict[((0, 0), direct, moves_in_direction)] = start
    end = Node((x_len-1,y_len-1), direction.ANY, 0, grid_map[x_len-1][y_len-1])
    for direct in [direction.UP, direction.DOWN, direction.LEFT, direction.RIGHT]:
        for moves_in_direction in range(1, 11):
            temp_dict[((x_len-1, y_len-1), direct, moves_in_direction)] = end

    for nd in temp_dict.values():
        direct = nd.direct
        moves_in_direction = nd.moves_in_direction
        (x, y) = nd.location
        if moves_in_direction < 4:
            if direct == direction.ANY:
                directions_to_check = [direction.RIGHT, direction.DOWN, direction.UP, direction.LEFT]
            else:
                directions_to_check = [direct]
        else:
            directions_to_check = other_directions_list[direct].copy()
            # print(directions_to_check)
            if moves_in_direction >= 10:
                directions_to_check.remove(direct)
            
        if x <= 0 and (direction.UP in directions_to_check):
            directions_to_check.remove(direction.UP)
        if x >= x_len-1 and (direction.DOWN in directions_to_check):
            directions_to_check.remove(direction.DOWN)
        if y <= 0 and (direction.LEFT in directions_to_check):
            directions_to_check.remove(direction.LEFT)
        if y >= y_len-1 and (direction.RIGHT in directions_to_check):
            directions_to_check.remove(direction.RIGHT)
        # print(location, directions_to_check)
        for c_direct in directions_to_check:              
            if c_direct == direct:
                nd.neighbours.append(temp_dict[(move_forwards_2((x,y), c_direct), c_direct, moves_in_direction + 1)])
            else:
                nd.neighbours.append(temp_dict[(move_forwards_2((x,y), c_direct), c_direct, 1)])
        # print(nd.location, nd.neighbours)
    
    return temp_dict


# This works! Now to set stuff up
def djikstras(node_map: [Node], start_nd, end_nd):
    i = 0
    modified_nodes = []
    curr_node = None
    # really bad way of finding the starting node
    for nd in node_map:
        if nd.location == (0,0):
            # print("found")
            nd.distance = 0
            curr_node = nd
        
    modified_nodes.append(curr_node)
    curr_node = min(modified_nodes, key=attrgetter('distance'))
    modified_nodes.remove(curr_node)
    # print(curr_node.location, curr_node.neighbours)
    while curr_node.location != end_nd.location:
        # print(curr_node.location, curr_node.distance, curr_node.neighbours)
        for neighbour in curr_node.neighbours:
            if not neighbour.visited:
                neighbour.distance = min(neighbour.distance, curr_node.distance+neighbour.cost)
                if not neighbour.in_modded:
                    modified_nodes.append(neighbour)
                    neighbour.in_modded = True
        curr_node.visited = True
        # node_map = sorted(node_map, key=attrgetter('distance'))
        curr_node = min(modified_nodes, key=attrgetter('distance'))
        modified_nodes.remove(curr_node)
        i += 1
        if i % 10000 == 0:
            print("Done", i, "nodes, current distance is", curr_node.distance)
    # we got to the end
    return curr_node.distance
            


# ???
f = open("input_1.txt", 'r')
# f = open("test_input.txt", 'r')
lines = f.readlines()
f.close()

grid_map = []
for line in lines:
    grid_map.append([int(i) for i in line.strip()])

end_of_map = (len(grid_map)-1, len(grid_map[0])-1)

nd_map = create_layout(grid_map)
print("Made layout!")
print(djikstras(list(nd_map.values()), nd_map[(0,0), direction.UP, 1], nd_map[(end_of_map), direction.RIGHT, 1]))
# print(end_of_map)
# current_best = sum([sum(line) for line in grid_map])

