# Day 7 problem 1

from operator import itemgetter, attrgetter
# Compare hands
# def compare_hands(hand_1, hand_2):

# Hand to number
def cards_to_number(hand_string):
    oup = []
    for card in list(hand_string):
        if card.isdigit():
            oup.append(int(card))
        elif card == 'T':
            oup.append(10)
        elif card == 'J':
            oup.append(11)
        elif card == 'Q':
            oup.append(12)
        elif card == 'K':
            oup.append(13)
        elif card == 'A':
            oup.append(14)
    return oup

class hand_class:
    def __init__(self, line) -> None:
        self.hand = cards_to_number(line.split()[0].strip())
        self.bid = int(line.split()[1].strip())
        self.type = self.calculate_hand_type()

    def calculate_hand_type(self):
        temp = sorted(self.hand)
        # Four of a kind
        if temp.count(temp[0]) == 5:
            return 7
        # Four of a kind
        if sorted([temp.count(i) for i in temp]) == [1, 4, 4, 4, 4]:
            return 6
        # Full House:
        if sorted([temp.count(i) for i in temp]) == [2, 2, 3, 3, 3]:
            return 5
        # Three of a kind
        if sorted([temp.count(i) for i in temp]) == [1, 1, 3, 3, 3]:
            return 4
        # Two Pairs:
        if sorted([temp.count(i) for i in temp]) == [1, 2, 2, 2, 2]:
            return 3
        # One Pair:
        if sorted([temp.count(i) for i in temp]) == [1, 1, 1, 2, 2]:
            return 2
        # High Card
        if sorted([temp.count(i) for i in temp]) == [1, 1, 1, 1, 1]:
            return 1







f = open("input_1.txt", 'r')
# f = open("test_input.txt", 'r')
lines = f.readlines()
f.close()

hands = []
bids = []

# pre-processing
for line in lines:
    hands.append(hand_class(line))

sorted_hands = sorted(hands, key=attrgetter('hand'))
sorted_hands = sorted(sorted_hands, key=attrgetter('type'))

total = 0
for i in range(0, len(sorted_hands)):
    total += (i+1)*sorted_hands[i].bid

print(total)
# Scoring hands:
# We can just try to sort?
