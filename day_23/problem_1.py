# Day 23 problem 1

debug = False
start_section = None
end_section = None

# Taken from https://www.geeksforgeeks.org/python-transpose-elements-of-two-dimensional-list/
def transpose(inp):
    # print(len(inp))
    # print(len(inp[0]))
    oup = [[row[i] for row in inp] for i in range(len(inp[0]))]
    return oup



class path_section:
    def __init__(self, location, c) -> None:
        self.location = location
        # self.cost = 1
        self.options_from = []
        self.options_to = []
        self.is_start = False
        self.is_end = False
        self.c = c
        # if c == '#'

    def get_immediate_points_to(self, grid_map) -> None:
        if self.c == '#':
            return
        else:
            if self.is_start:
                self.options_from.append(grid_map[self.location[0]+1][self.location[1]])
                grid_map[self.location[0]+1][self.location[1]].options_to.append(self)
            elif self.is_end:
                self.options_from.append(grid_map[self.location[0]-1][self.location[1]])
                grid_map[self.location[0]-1][self.location[1]].options_to.append(self)
            else:
                # not start or end
                sides = [
                    grid_map[self.location[0]+1][self.location[1]], # Down
                    grid_map[self.location[0]-1][self.location[1]], # Up
                    grid_map[self.location[0]][self.location[1]-1], # Left
                    grid_map[self.location[0]][self.location[1]+1]  # Right
                ]
                # Slopes
                if self.c == '^':
                    self.options_from.append(sides[1])
                    sides[1].options_to.append(self)
                elif self.c == 'v':
                    self.options_from.append(sides[0])
                    sides[0].options_to.append(self) 
                elif self.c == '<':
                    self.options_from.append(sides[2])
                    sides[2].options_to.append(self)
                elif self.c == '>':
                    self.options_from.append(sides[3])
                    sides[3].options_to.append(self)
                # Boring tile ouagh
                else:
                    for i in range(len(sides)):
                        side = sides[i]
                        if side.c != '#':
                            if not ((i == 0 and side.c == '^') or (i == 1 and side.c == 'v') or (i == 2 and side.c == '>') or (i == 3 and side.c == '<')):
                                self.options_from.append(side)
                                side.options_to.append(self)

        pass

    def __repr__(self) -> str:
        oup = ""
        oup += "(" + str(self.location) + ", " + self.c + ")"
        return oup


class garden_path:
    def __init__(self, start_location: path_section, end_location: path_section, cost, locations_within) -> None:
        self.start_location = start_location
        self.end_location = end_location
        self.cost = cost
        self.locations_within = locations_within
        self.come_from = end_location
        self.illegal = False
    
    def setup(self):
        self.locations_within = [self.start_location]
        if self.end_location != self.start_location:
            self.locations_within.append(self.end_location)


    def eat_ends_recursively(self):
        keep_going = True
        while keep_going:
            # if debug:
            #     print("From", self.start_location.location, "to", self.end_location.location)
            keep_going = self.eat_end()
            # if debug:
                # print(keep_going)
            if self.start_location is self.end_location:
                self.cost = 1
                self.illegal = True
                break
        if debug:
            # print(self.cost)
            pass
        

    def eat_end(self) -> bool:
        if self.end_location is end_section:
            if debug:
                print("We found the end")
                pass
            return False
        if len([k for k in self.end_location.options_from if k not in self.locations_within]) == 1:
            for k in self.end_location.options_from:
                if k not in self.locations_within:
                    # if debug:
                    #     print(k == self.locations_within[-1])
                    self.end_location = k
                    break
            # self.come_from = self.end_location
            # self.end_location = new_end
            self.cost += 1
            # if self.end_location in self.locations_within:
            #     self.cost = 1
            #     self.illegal = True
            #     if debug:
            #         print(self, self.locations_within)
            #         print("eat_end: Looped in on ourself")
            #     return False
            
            self.locations_within.append(self.end_location)
            # print(self.locations_within)
            return True
        else:
            if debug:
                print("We ran out of space")
            #     print(len(self.end_location.options_from) + (-1 if self.locations_within[-1] in self.end_location.options_from else 0))
            return False
        
    def __repr__(self):
        oup = "<"
        oup += "Start Location: " + str(self.start_location)
        oup += ", End Location: " + str(self.end_location)
        oup += ", Cost: " + str(self.cost) 
        oup += ", Illegal: " + str(self.illegal)
        oup += ">"
        return oup


def get_routes(path_dict, curr_visited, start_location, goal=end_section):
    if start_location == goal:
        return 0
    oup = 0
    cv = curr_visited.copy()
    cv.append(start_location)

    for route in path_dict[start_location.location]:
        if route.end_location not in cv:
            oup = max(oup, get_routes(path_dict, cv, route.end_location, goal) + route.cost)
    return oup


f = open("input_1.txt", 'r')
# f = open("test_input.txt", 'r')
lines = f.readlines()
f.close()

grid_map = []


for x in range(len(lines)):
    line = lines[x].strip()
    line_map = []
    for y in range(len(line)):
        line_map.append(path_section((x, y), line[y]))
    grid_map.append(line_map)
        


for sq in grid_map[0]:
    if sq.c == '.':
        sq.is_start = True
        start_section = sq
        break

for sq in grid_map[-1]:
    if sq.c == '.':
        sq.is_end = True
        end_section = sq
        break
print("Start:", start_section.location)
print("End:", end_section.location)

for ln in grid_map:
    for lc in ln:
        lc.get_immediate_points_to(grid_map)

if debug:
#     to_print = [(4,4), (5,3), (5,4), (5,5)]
#     for (x, y) in to_print:
#         print("(", x, ",", y, "),", grid_map[x][y].c, ",", grid_map[x][y].options_from)
    pass
    
# Now we want to make paths i guess?
# full_paths = []
# start_path = garden_path(start_section, start_section, 1, [])

# curr_path = start_path
path_dict = {}
places_to_map_from = [start_section]
places_mapped_from = []
while len(places_to_map_from) != 0:
    # print("hi")
    curr_section = places_to_map_from.pop(0)
    if debug:
        # print(curr_section.options_from)
        pass
    if curr_section != end_section:
        for loc in curr_section.options_from:
            curr_path = garden_path(curr_section, loc, 1, [])
            curr_path.setup()
            curr_path.eat_ends_recursively()
            if not curr_path.illegal:
                # full_paths.append(curr_path)
                path_dict.setdefault(curr_path.start_location.location, []).append(curr_path)
                path_dict[curr_path.start_location.location].append(curr_path)
                if not curr_path.end_location in places_mapped_from:
                    places_to_map_from.append(curr_path.end_location)
    places_mapped_from.append(curr_section)


# We can maybe turn our routes back into nodes, and then figure out something from there?
# print(full_paths)

# now we somehow have to find the longest path??? I guess we can do all the options or something??
print("we've successfully made our routes")
print(get_routes(path_dict, [], start_section, end_section))