# Day 13 problem 1
import os
# Taken from https://www.geeksforgeeks.org/python-transpose-elements-of-two-dimensional-list/
def transpose(inp):
    # print(len(inp))
    # print(len(inp[0]))
    oup = [[row[i] for row in inp] for i in range(len(inp[0]))]
    return oup

f = open("input_1.txt", 'r')
f = open("test_input.txt", 'r')
# lines = f.readlines()
blocks = f.read().split("\n\n")
f.close()

# print(blocks)
block_clean = []
for block in blocks:
    block_clean.append([line.strip() for line in block.splitlines()])
# print(block_clean)
total = 0
# Horizontal maybe?
for block in block_clean:
    prev_line = []
    for i in range(0, len(block)):
        line = block[i]
        if min(i, len(block)-i) > 0:
            mirror = True
            for j in range(0, min(i, len(block)-i)):
                # print("i+j", i+j, "i-j-1", i-j-1, "len", len(block))
                if i+j > len(block)-1 or i-j-1 < 0:
                    print("Error", i, j, len(block))
                    break
                if block[i+j] != block[i-j-1]:
                    mirror = False
                    break
            if mirror == True:
                # print("Success hundred", i)
                total += 100*(i)
                
# vertical maybe?
for odd_block in block_clean:
    block = transpose(odd_block)
    prev_line = []
    for i in range(0, len(block)):
        line = block[i]
        if min(i, len(block)-i) > 0:
            mirror = True
            for j in range(0, min(i, len(block)-i)):
                # print("i+j", i+j, "i-j-1", i-j-1, "len", len(block))
                if i+j > len(block)-1 or i-j-1 < 0:
                    print("Error", i, j, len(block))
                    break
                if block[i+j] != block[i-j-1]:
                    mirror = False
                    break
            if mirror == True:
                # print("Success one", i)
                # print(block[i-1])
                # print(block[i])
                # print(block[i+1])

                total += 1*(i)
        # else:
            # print(min(i, len(block)-i-1))

print(total)