# Day 8 problem 1

class node_p:
    def __init__(self, line) -> None:
        parts = line.strip().split(' = ')
        self.name = parts[0]
        self.left = parts[1].split(', ')[0][1:]
        self.right = parts[1].split(', ')[1][:-1]
        


f = open("input_1.txt", 'r')
# f = open("test_input.txt", 'r')
lines = f.readlines()
f.close()


nodes = dict()
instruction_list = lines[0].strip()
for node_line in lines[2:]:
    new_node = node_p(node_line)
    nodes[new_node.name] = new_node

current_node = nodes['AAA']
steps = 0
done = False
while not done:
    for i in range(0, len(instruction_list)):
        if instruction_list[i] == 'L':
            current_node = nodes[current_node.left]
        elif instruction_list[i] == 'R':
            current_node = nodes[current_node.right]
        steps = steps + 1
        if current_node.name == 'ZZZ':
            done = True
            break

print(steps)