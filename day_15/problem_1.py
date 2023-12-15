# Day 15 problem 1


def hash(inp):
    curr = 0
    for char in inp:
        curr = ((curr + ord(char)) * 17) % 256
    return curr

f = open("input_1.txt", 'r')
# f = open("test_input.txt", 'r')
lines = f.readlines()
f.close()

total = 0
for inp in lines[0].strip().split(','):
    total += hash(inp)
print(total)