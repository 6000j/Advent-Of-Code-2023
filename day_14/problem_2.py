# Day 14 problem 2


boards_seen = []

# Taken from https://www.geeksforgeeks.org/python-transpose-elements-of-two-dimensional-list/
def transpose(inp):
    # print(len(inp))
    # print(len(inp[0]))
    oup = [[row[i] for row in inp] for i in range(len(inp[0]))]
    return oup

# https://stackoverflow.com/questions/8421337/rotating-a-two-dimensional-array-in-python
def rotate_array(inp):
    return list(zip(*inp[::-1]))


def board_to_nice(board):
    oup = ""
    for line in board:
        oup += ''.join(line) + '\n'
    oup = oup.strip()
    return oup

def nice_to_board(nice):
    # print("nice:\n", nice)
    board = []
    board = [list(line.strip()) for line in nice.splitlines()]
    # print(board_to_nice(board) == nice)
    # print(board)
    return board

def slide_up(board):
    oup = [['.' for _ in range(len(board[0]))] for _ in range(len(board))]
    for j in range(0, len(board[0])):
        # Now we want to iterate over each line
        roll_to = 0
        for i in range(0, len(board)):
            # yes this is awful stride, i will fix it if it's too slow
            curr_square = board[i][j]
            if curr_square == '.':
                pass
            if curr_square == '#':
                oup[i][j] = '#'
                roll_to = i+1
            if curr_square == 'O':
                oup[roll_to][j] = 'O'
                roll_to = roll_to + 1
    return oup

def cycle(bd):
    board = bd
    for i in range(4):
        board = slide_up(board)
        board = rotate_array(board)
    return board

f = open("input_1.txt", 'r')
# f = open("test_input.txt", 'r')
lines = f.readlines()
f.close()

# Making a 2d space
board = []
for line in lines:
    board.append(list(line.strip()))

print(board_to_nice(cycle(board)))

goal = pow(10, 9)
# goal = 3
for m in range(goal):
    if board_to_nice(board) in boards_seen:
        loc = boards_seen.index(board_to_nice(board))
        cycle_length = len(boards_seen) - loc
       #  print(board_to_nice(cycle(board)))
        board = nice_to_board(boards_seen[loc + ((goal - m) % cycle_length)])
        # print('\n')
        # print(board_to_nice(board))
        break
    else:
        boards_seen.append(board_to_nice(board))
        board = cycle(board)

total = 0
for i in range(len(board)):
    for c in board[i]:
        if c == "O":
            total += len(board)-i

print(total)
# print(board_to_nice(board))
# for line in board:
    # print(line)
# board = transpose(board)
# total = 0
# # Rolling upwards along each column
# for j in range(0, len(board[0])):
#     # Now we want to iterate over each line
#     roll_to = 0
#     for i in range(0, len(board)):
#         # yes this is awful stride, i will fix it if it's too slow
#         curr_square = board[i][j]
#         if curr_square == '.':
#             pass
#         if curr_square == '#':
#             #total += len(board)-i
#             roll_to = i+1
#         if curr_square == 'O':
#             # print("added", len(board[0])-roll_to, "weight due to", (i,j))
#             total += len(board[0])-roll_to
#             roll_to = roll_to + 1

# print(total)