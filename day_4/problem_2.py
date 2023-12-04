# Day 4 problem 2

def check_wins(card_table, card_to_check):
    curr_score = 0
    total = 1
    (win_nums, have_nums, score) = card_table[card_to_check]
    if score != -1:
        return score
    for have in have_nums:
        if have in win_nums:
            curr_score = curr_score+1
    for i in range(card_to_check+1, card_to_check+curr_score+1):
        total += check_wins(card_table, i)
    card_table[card_to_check][2] = total
    return total
        

f = open("input_1.txt", 'r')
lines = f.readlines()
f.close()

# Preprocessing
for v in range(0, len(lines)):
    lines[v] = lines[v].strip()
for i in range(len(lines)):
    lines[i] = lines[i].split(':')[1].strip()
    (win_line, have_line) = lines[i].split("|")
    win_line = win_line.strip()
    have_line = have_line.strip()
    win_nums = [int(val) for val in win_line.split()]
    have_nums = [int(val) for val in have_line.split()]
    lines[i] = [win_nums, have_nums, -1]


total = 0
for i in range(0, len(lines)):
    total += check_wins(lines, len(lines)-i-1)
# # This is easy, right?
# for line in lines:
#     curr_score = 0
#     (win_line, have_line) = line.split("|")
#     win_line = win_line.strip()
#     have_line = have_line.strip()
#     win_nums = [int(val) for val in win_line.split()]
#     have_nums = [int(val) for val in have_line.split()]
#     for have in have_nums:
#         if have in win_nums:
#             if curr_score == 0:
#                 curr_score = 1
#             else:
#                 curr_score = curr_score*2
#     total += curr_score

print(total)
    