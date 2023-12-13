# Day 13 problem 1
import os
# Taken from https://www.geeksforgeeks.org/python-transpose-elements-of-two-dimensional-list/
def transpose(inp):
    # print(len(inp))
    # print(len(inp[0]))
    oup = [[row[i] for row in inp] for i in range(len(inp[0]))]
    return oup

def are_one_away(first, second):
    return ([first[i] == second[i] for i in range(len(first))].count(False) == 1)

f = open("input_1.txt", 'r')
# f = open("test_input.txt", 'r')
# lines = f.readlines()
blocks = f.read().split("\n\n")
f.close()

# print(blocks)
block_clean = []
for block in blocks:
    block_clean.append([line.strip() for line in block.splitlines()])
# print(block_clean)
total = 0
good_list = []
# Horizontal maybe?
for k in range(len(block_clean)):
    block = block_clean[k]
    for i in range(0, len(block)):
        line = block[i]
        if min(i, len(block)-i) > 0:
            have_fudged = False
            mirror = True
            for j in range(0, min(i, len(block)-i)):
                if i+j > len(block)-1 or i-j-1 < 0:
                    print("Error", i, j, len(block))
                    break
                if block[i+j] != block[i-j-1]:
                    if are_one_away(block[i+j], block[i-j-1]) and have_fudged == False:
                        # print("Fudged", i)
                        # print("\t", i+j, block[i+j])
                        # print("\t", i-j-1, block[i-j-1])
                        have_fudged = True
                    else:
                        mirror = False
                        # print("Broken", i)
                        # print("\t", i+j, block[i+j])
                        # print("\t", i-j-1, block[i-j-1])
                        break
            if (mirror == True) and (have_fudged == True):
                good_list.append(k)
                # print("one hundred", i)
                total += 100*(i)
                break
            
            
bad_blocks = [block_clean[k] for k in range(len(block_clean)) if k not in good_list]             
# vertical maybe?
for k in range(len(bad_blocks)):
    block = transpose(bad_blocks[k])
    for i in range(0, len(block)):
        line = block[i]
        if min(i, len(block)-i) > 0:
            have_fudged = False
            mirror = True
            for j in range(0, min(i, len(block)-i)):
                # print("i+j", i+j, "i-j-1", i-j-1, "len", len(block))
                if i+j > len(block)-1 or i-j-1 < 0:
                    print("Error", i, j, len(block))
                    break
                if block[i+j] != block[i-j-1]:
                    if are_one_away(block[i+j], block[i-j-1]) and have_fudged == False:
                        # print("Fudged")
                        # print("\t", block[i+j])
                        # print("\t", block[i-j-1])
                        have_fudged = True
                    else:
                        mirror = False
                        break
            if (mirror == True) and (have_fudged == True):
                # print("one", i)
                total += 1*(i)
                break
print(total)