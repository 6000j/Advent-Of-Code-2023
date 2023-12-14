# Day 14 problem 1

# Taken from https://www.geeksforgeeks.org/python-transpose-elements-of-two-dimensional-list/
def transpose(inp):
    # print(len(inp))
    # print(len(inp[0]))
    oup = [[row[i] for row in inp] for i in range(len(inp[0]))]
    return oup

f = open("input_1.txt", 'r')
# f = open("test_input.txt", 'r')
lines = f.readlines()
f.close()

# Making a 2d space
board = []
for line in lines:
    board.append(list(line.strip()))
# for line in board:
    # print(line)
# board = transpose(board)
total = 0
# Rolling upwards along each column
for j in range(0, len(board[0])):
    # Now we want to iterate over each line
    roll_to = 0
    for i in range(0, len(board)):
        # yes this is awful stride, i will fix it if it's too slow
        curr_square = board[i][j]
        if curr_square == '.':
            pass
        if curr_square == '#':
            #total += len(board)-i
            roll_to = i+1
        if curr_square == 'O':
            # print("added", len(board[0])-roll_to, "weight due to", (i,j))
            total += len(board[0])-roll_to
            roll_to = roll_to + 1

print(total)