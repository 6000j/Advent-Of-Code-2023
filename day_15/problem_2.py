# Day 15 problem 2

boxes = [[] for _ in range(256)]
box_nums = [[] for _ in range(256)]

def hash(inp):
    curr = 0
    for i in range(len(inp)):
        char = inp[i]
        if char == '=':
            # getting lens length
            focal_length = int(inp[i+1:])
            # print(len(boxes))
            if inp[:i] in boxes[curr]:
                box_nums[curr][boxes[curr].index(inp[:i])] = focal_length
            else:
                boxes[curr].append(inp[:i])
                box_nums[curr].append(focal_length)
            break
        if char == '-':
            for j in range(len(boxes[curr])):
                if boxes[curr][j] == inp[:i]:
                    boxes[curr].pop(j)
                    box_nums[curr].pop(j)
                    break
        else:
            curr = ((curr + ord(char)) * 17) % 256
    # return curr

f = open("input_1.txt", 'r')
# f = open("test_input.txt", 'r')
lines = f.readlines()
f.close()

total = 0
for inp in lines[0].strip().split(','):
    hash(inp)

for i in range(len(box_nums)):
    for j in range(len(box_nums[i])):
        total += (1+i) * (1 + j) * (box_nums[i][j])
print(total)