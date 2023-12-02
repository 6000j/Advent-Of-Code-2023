# Day 2, Problem 2
import re
import typing

# Parsing a single line
def is_game_possible(game_line) -> int:
    colours = {'red':0, 'green':0, 'blue':0}
    game_halves = game_line.split(':')
    # Getting which game we're currently on
    # game_number = int(game_halves[0].split(' ')[1])
    # Parsing our cubes for this game 
    games = game_halves[1].split(';')
    for game in games:
        hands = game.split(',')
        for hand_i in hands:
            hand = hand_i.strip()
            val = int(hand.split(' ')[0])
            # Iterating over all our inputs
            for k in colours.keys():
                if hand.endswith(k):
                    if val > colours[k]:
                        colours[k] = val
    oup = 1
    for k in colours.keys():
        oup = oup * colours[k]
    return oup

f = open("input_1.txt", 'r')
lines = f.readlines()
f.close()
# rgb = {'red':12, 'green':13, 'blue':14}
total = 0
for line in lines:
    total += is_game_possible(line)

print(total)
