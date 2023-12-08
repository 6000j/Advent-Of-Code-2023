# Day 8 problem 2
import collections
class node_p:
    def __init__(self, line) -> None:
        parts = line.strip().split(' = ')
        self.name = parts[0]
        self.left = parts[1].split(', ')[0][1:]
        self.right = parts[1].split(', ')[1][:-1]
        self.is_start = (self.name[-1] == 'A')
        self.is_end = (self.name[-1] == 'Z')
    
    def correct_nodes(self, nodes):
        self.t_left = nodes[self.left]
        self.t_right = nodes[self.right]


class node_loop:
    """Node loops store a start node and their loop course!
    """
    def __init__(self, start_node, trailin, path, loop_size) -> None:
        self.start_node = start_node
        self.trailin = trailin
        self.path = path
        self.endpt_path = [nd.is_end for nd in path]
        self.loop_size = loop_size
        # print(self.endpt_path)

    
    def get_nth_step(self, n):
        if n < self.trailin:
            return self.path[n]
        else:
            return self.path[self.trailin + (n-self.trailin % self.loop_size)]
    
    def get_nth_step_endpt(self, n):
        if n < self.trailin:
            return self.endpt_path[n]
        else:
            return self.endpt_path[self.trailin + ((n-self.trailin) % self.loop_size)]
    
    def get_pogged_values_up_to(self, n, list=None):
        oup = []
        loop_ends = []
        if list is not None:
            for k in list:
                if self.get_nth_step_endpt(k):
                    oup.append(k)
        else:
            for i in range(0, len(self.endpt_path[:self.trailin])):
                if self.endpt_path[i]:
                    oup.append(i)
            for i in range(len(self.endpt_path[:self.trailin]), len(self.endpt_path)):
                if self.endpt_path[i]:
                    loop_ends.append(i)
            for point in loop_ends:
                curr_score = point
                while curr_score < n:
                    oup.append(curr_score)
                    curr_score += self.loop_size
        # print("gotten values of", oup)
        return oup

    def __repr__(self) -> str:
        return "<Start: " + str(self.start_node.name) + "; Trailin: " + str(self.trailin) + "; Loop_size: " + str(self.loop_size) + ">"    
    


def next_node(current_node, instruction):
    if instruction == 'L':
        oup = current_node.t_left
    elif instruction == 'R':
        oup = current_node.t_right
    return oup

def get_node_loop_stats(starting_node, instructions):
    loop_start = None
    trailin = 0
    nodes_and_loc = []
    nodes_seen = []
    current_node = starting_node
    current_seen = 0
    while (current_node, current_seen % len(instructions)) not in nodes_and_loc:
        nodes_and_loc.append((current_node, current_seen % len(instructions)))
        nodes_seen.append(current_node)
        current_node = next_node(current_node, instructions[current_seen % len(instructions)])
        current_seen += 1
    # Now we've found a loop
    trailin = nodes_and_loc.index((current_node, current_seen % len(instructions)))
    loop_start = nodes_seen[trailin]
    loop_size = current_seen - trailin
    return node_loop(starting_node, trailin, nodes_seen, loop_size)

f = open("input_1.txt", 'r')
# f = open("test_input.txt", 'r')
lines = f.readlines()
f.close()

goal = pow(10, 13)

nodes = dict()
instruction_list = lines[0].strip()
for node_line in lines[2:]:
    new_node = node_p(node_line)
    nodes[new_node.name] = new_node
for asd in nodes.values():
    asd.correct_nodes(nodes)


current_nodes = [nd for nd in nodes.values() if nd.is_start == True]
current_node_loops = [get_node_loop_stats(nd, instruction_list) for nd in current_nodes]
# print(current_node_loops)

print("made starting node list! It has size", len(current_nodes))
# current_to_check = range(0, pow(10, 10))
# print("made the list to check!")

pogged_values = None
for ilp in range(0, len(current_node_loops)):
    lp = current_node_loops[ilp]
    if ilp == 0:
        pogged_values = lp.get_pogged_values_up_to(goal)
        # lp.get_pogged_values_up_to(100000)
    else:
        pogged_values = lp.get_pogged_values_up_to(goal, pogged_values)
    if pogged_values == []:
        print("something has gone wrong at ilp", ilp)
    print("Done step", ilp)

# print(pogged_values)
print(min(pogged_values))
#     for k in current_to_check:
#         if lp.get_nth_step_endpt(k):
#             new_to_check.append(k)
#     current_to_check = new_to_check
#     print("Done a node!")
# print(min(current_to_check))


# steps = 0
# done = False
# while not done:
#     for i in range(0, len(instruction_list)):
#         done = True
#         for k in range(0, len(current_nodes)):
#             current_nodes[k] = next_node(current_nodes[k], instruction_list[i])
#             # if current_nodes[k].is_end:
#                 # print('a node has made it to the water after', steps+1, 'steps')
#             done = (current_nodes[k].is_end and done)
            
#         steps = steps + 1
#         if steps % 100000 == 0:
#             print("Done", steps, "steps")
#         if done:
#             break

# print(steps)