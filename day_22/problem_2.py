# Day 22 problem 2
from collections import namedtuple
from operator import attrgetter
from functools import cache

debug = False
# Taken from https://www.geeksforgeeks.org/python-transpose-elements-of-two-dimensional-list/
def transpose(inp):
    # print(len(inp))
    # print(len(inp[0]))
    oup = [[row[i] for row in inp] for i in range(len(inp[0]))]
    return oup


class Location:
    x: int
    y: int
    z: int
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z
    
    def copy(self) -> """Location""":
        return Location(self.x, self.y, self.z)

    def __repr__(self) -> str:
        return "(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"

    
# @cache
def do_location_ranges_intersect(s1: Location, e1: Location, a1: str, s2: Location, e2: Location, a2: str) -> bool:
    x_first_comparator = not (s1.x > e2.x) and not (e1.x < s2.x)
    y_first_comparator = not (s1.y > e2.y) and not (e1.y < s2.y)
    z_first_comparator = not (s1.z > e2.z) and not (e1.z < s2.z)
    x_second_comparator = not (s2.x > e1.x) and not (e2.x < s1.x)
    y_second_comparator = not (s2.y > e1.y) and not (e2.y < s1.y)
    z_second_comparator = not (s2.z > e1.z) and not (e2.z < s1.z)
    if debug:
        print('\t', a1, a2)
        print('\t', (s1.x == s2.x), (s1.y == s2.y), (s1.z == s2.z))
        print('\t', x_first_comparator, x_second_comparator, y_first_comparator, y_second_comparator, z_first_comparator, z_second_comparator)
    if a1 == 'x':
        if a2 == 'x':
            return (s1.y == s2.y) and (s1.z == s2.z) and x_first_comparator and x_second_comparator
        if a2 == 'y':
            return (s1.z == s2.z) and x_first_comparator and y_second_comparator
        if a2 == 'z':
            return (s1.y == s2.y) and x_first_comparator and z_second_comparator
    elif a1 == 'y':
        if a2 == 'x':
            return (s1.z == s2.z) and y_first_comparator and x_second_comparator
        if a2 == 'y':
            return (s1.x == s2.x) and (s1.z == s2.z) and y_first_comparator and y_second_comparator
        if a2 == 'z':
            return (s1.x == s2.x) and y_first_comparator and z_second_comparator
    elif a1 == 'z':
        if a2 == 'x':
            return (s1.y == s2.y) and z_first_comparator and x_second_comparator
        if a2 == 'y':
            return (s1.x == s2.x) and z_first_comparator and y_second_comparator
        if a2 == 'z':
            return (s1.x == s2.x) and (s1.y == s2.y) and z_first_comparator and z_second_comparator

def do_location_ranges_intersect_wrapper(b1: """Brick""", b2: """Brick"""):
    if debug:
        print(b1, ', ', b2)
    oup = do_location_ranges_intersect(b1.start_tile, b1.end_tile, b1.axis, b2.start_tile, b2.end_tile, b2.axis)
    if debug: 
        print('\t', oup)
    return oup

class Brick:
    # tiles: [Location]
    start_tile: Location
    end_tile: Location
    axis: str
    lowest_z: int
    supported_by: ["""Brick"""]
    supports: ["""Brick"""]

    supported_ids = [int]
    supports_ids = [int]
    id: int
    def __init__(self, start: Location, end: Location) -> None:
        self.tiles = []
        self.supported_by = []
        self.supports = []
        self.supported_ids = []
        self.supports_ids = []
        # Filling out our full list of space we occupy
        if start.x != end.x:
            self.axis = 'x'
            self.start_tile = Location(min(start.x, end.x), start.y, start.z)
            self.end_tile = Location(max(start.x, end.x), start.y, start.z)
            #self.tiles = [Location(i, start.y, start.z) for i in range(nice_start, nice_end+1)]
        elif start.y != end.y:
            self.axis = 'y'
            self.start_tile = Location(start.x, min(start.y, end.y), start.z)
            self.end_tile = Location(start.x, max(start.y, end.y), start.z)
            # self.tiles = [Location(start.x, j, start.z) for j in range(nice_start, nice_start+1)]
        elif start.z != end.z:
            self.axis = 'z'
            self.start_tile = Location(start.x, start.y, min(start.z, end.z))
            self.end_tile = Location(start.x, start.y, max(start.z, end.z))
            # self.tiles = [Location(start.x, start.y, k) for k in range(nice_start, nice_end+1)]
        # If we're only one cube large, we just do this and act as though we're on the x axis
        else: 
            self.axis = 'x'
            self.start_tile = Location(min(start.x, end.x), start.y, start.z)
            self.end_tile = Location(max(start.x, end.x), start.y, start.z)

        self.lowest_z = min(self.start_tile.z, self.end_tile.z)
        
    # USED ONLY FOR THE CURRENT POSITION TRACKER
    def fall_down_one(self) -> None:
        self.start_tile.z -= 1
        self.end_tile.z -= 1
        self.lowest_z -= 1


    def fall_down_safely(self, brick_list: ["""Brick"""]) -> None:
        curr_position = Brick(Location(self.start_tile.x, self.start_tile.y, self.start_tile.z), Location(self.end_tile.x, self.end_tile.y, self.end_tile.z))
        can_fall = True
        while can_fall:

            curr_position.fall_down_one()
            if curr_position.lowest_z < 1:
                can_fall = False
                break
            for brck in brick_list:
                if brck is not self:
                    if do_location_ranges_intersect_wrapper(curr_position, brck):
                        # print("hi")
                        can_fall = False
                        self.supported_by.append(brck)
                        self.supported_ids.append(brck.id)
                        brck.supports.append(self)
                        brck.supports_ids.append(self.id)
             # = Brick(Location(curr_position.start_tile.x, curr_position.start_tile.y, curr_position.start_tile.z - 1), Location(self.end_tile.x, self.end_tile.y, self.end_tile.z - 1))
        # Now that we can no longer fall:
        self.start_tile = curr_position.start_tile.copy()
        self.start_tile.z += 1
        self.end_tile = curr_position.end_tile.copy()
        self.end_tile.z += 1
        self.lowest_z = curr_position.lowest_z + 1
        if debug:
            print("settled at", self)
        # self.start_tile = curr_position.start_tile
        # self.end_tile = curr_position.end_tile
        # self.lowest_z = curr_position.lowest_z
    
    def __repr__(self):
        return "<Start: " + str(self.start_tile) + ", End: " + str(self.end_tile) + ", Axis: " + self.axis + ">"

    
    # Part 1 specific code lmao
    def disintegrate(self):
        for brick in self.supports:
            if len(brick.supported_by) == 1:
                return 0
        # print(self, self.supports)
        return 1
    
    def disintergrate_chain(self, brick_list):
        oup = 0
        for brick_id in self.supports_ids:
            brick = brick_list[brick_id]
            # self.supports_ids.remove(brick_id)
            brick.supported_ids.remove(self.id)
            if len(brick.supported_ids) == 0:
                oup += 1 + brick.disintergrate_chain(brick_list)
        return oup
        pass

    def copy(self) -> """Brick""":
        oup_brick = Brick(self.start_tile.copy(), self.end_tile.copy())
        oup_brick.id = self.id
        oup_brick.supported_ids = self.supported_ids.copy()
        oup_brick.supports_ids = self.supports_ids.copy()
        return oup_brick

    # def copy_from_list




f = open("input_1.txt", 'r')
# f = open("test_input.txt", 'r')
lines = f.readlines()
f.close()


brick_list: [Brick] = []
# Parser!
brick_list = [Brick(Location(int(x1), int(y1), int(z1)), Location(int(x2), int(y2), int(z2))) for [x1, y1, z1, x2, y2, z2] in [line.strip().replace('~', ',').split(',') for line in lines]]
# print(brick_list)
print("made bricks!")
brick_list = sorted(brick_list, key=attrgetter('lowest_z'))
# giving them all an id
for i in range(len(brick_list)):
    brick_list[i].id = i
# print(brick_list)
for i in range(len(brick_list)):
    brick = brick_list[i]
    brick.fall_down_safely(brick_list)
    if i % 100 == 0:
        print(i, "bricks have fallen down")
    
# for brick in brick_list:
#     brick.fall_down_safely(brick_list)
print(len(brick_list), "Bricks have fallen down safely!")
if debug:
    for brick in brick_list:
        print(brick.supports)
# temp_list = [brick.copy() for brick in brick_list]
# hopefully this works
total = 0
for i in range(len(brick_list)):
    temp_list = [brick.copy() for brick in brick_list]
    # print(temp_list)
    
    curr_brick = temp_list[i]
    # print(curr_brick.supports_ids)
    total += curr_brick.disintergrate_chain(temp_list)
    # print(total)
    if i % 100 == 0:
        print(i+1, "bricks have been disintergrated for a current score of", total)

print(total)