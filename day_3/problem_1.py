# Day 3 problem 1
import typing

class num_loc:
    def __init__(self, value, locations) -> None:
        self.value = value
        self.locations = locations
        



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
# Now we want to iterate over it to mark what is used and what isn't
for i in range(0,rows):
    for j in range(0, columns):
        # Checking if we're a symbol
        if (not lines[i][j].isnumeric()) and (not lines[i][j] == '.'):
            # Above row
            if i > 0:
                used[i-1][j] = True
                if j > 0:
                    used[i-1][j-1] = True
                if j < columns-1:
                    used[i-1][j+1] = True
            # Correct Row
            used[i][j] = True
            if j > 0:
                used[i][j-1] = True
            if j < columns-1:
                used[i][j+1] = True
            # Below row
            if i < rows-1:
                used[i+1][j] = True
                if j > 0:
                    used[i+1][j-1] = True
                if j < columns-1:
                    used[i+1][j+1] = True



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
    for location in num.locations:
        if used[location[0]][location[1]]:
            total += num.value
            break

print(total)
