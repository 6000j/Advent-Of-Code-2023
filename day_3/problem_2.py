# Day 3 problem 2
import typing

class num_loc:
    def __init__(self, value, locations) -> None:
        self.value = value
        self.locations = locations
        self.adj_locations = set()
        for location in locations:
            i = location[0]
            j = location[1]
            if i > 0:
                self.adj_locations.add((i-1, j))
                if j > 0:
                    self.adj_locations.add((i-1, j-1))
                if j < columns-1:
                    self.adj_locations.add((i-1, j+1))
            # Correct Row
            self.adj_locations.add((i, j))
            if j > 0:
                self.adj_locations.add((i, j-1))
            if j < columns-1:
                self.adj_locations.add((i, j+1))
            # Below row
            if i < rows-1:
                self.adj_locations.add((i+1, j))
                if j > 0:
                    self.adj_locations.add((i+1, j-1))
                if j < columns-1:
                    self.adj_locations.add((i+1, j+1))
        



f = open("input_1.txt", 'r')
lines = f.readlines()
f.close()
for v in range(0, len(lines)):
    lines[v] = lines[v].strip()

# Getting constants
rows = len(lines)
columns = len(lines[0])
print('Rows:', rows)
print('Columns:', columns)
# Creating our array
used = [[False for _ in range (columns)] for _ in range(rows)]

adj_numbers = [[[] for _ in range (columns)] for _ in range(rows)]


# Now we want to iterate over it to mark what is used and what isn't
for i in range(0,rows):
    for j in range(0, columns):
        # Checking if we're a symbol
        if lines[i][j] == '*':
            used[i][j] = True



values = []
start = 0
tracking = False
# Now we want to create a 2d array that has all the values in it, I think?
for i in range(0, rows):
    curr_row = lines[i]
    tracking = False
    start = 0
    for j in range(0, len(curr_row)):
        c = curr_row[j]
        # If we're a digit
        if c.isdigit():
            if tracking:
                pass
            else:
                start = j
                tracking = True
        else:
            if tracking:
                # Adding the number to our list
                new_loc = num_loc(int(curr_row[start:j]), ([(i, y) for y in range(start, j)]))
                values.append(new_loc)
                tracking = False
            else:
                pass
    if tracking:
        # Adding the number to our list
        new_loc = num_loc(int(curr_row[start:j+1]), ([(i, y) for y in range(start, j+1)]))
        values.append(new_loc)
        tracking = False

total = 0

# Now we iterate over the numbers list and check if they're real!
for num in values:
    for adj_loc in num.adj_locations:
        adj_numbers[adj_loc[0]][adj_loc[1]].append(num.value)

for i in range(len(adj_numbers)):
    curr_row = adj_numbers[i]
    for j in range(len(curr_row)):
        if used[i][j] and len(adj_numbers[i][j]) == 2:
            total += adj_numbers[i][j][0] * adj_numbers[i][j][1]

print(total)
