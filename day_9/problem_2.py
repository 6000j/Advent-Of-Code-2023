# Day 9 problem 2

def full_calculation(history):
    layers = [history]
    curr_history = history
    while curr_history.count(0) != len(curr_history):
        curr_history = go_down_one_layer(curr_history)
        layers.append(curr_history)
    layers = go_up_layers(layers)
    return layers[0][0]

def go_down_one_layer(sequence):
    oup = []
    for i in range(0, len(sequence)-1):
        oup.append(sequence[i+1] - sequence[i])
    return oup


def go_up_layers(layers):
    # Going back up from a full array of the layers
    for i in reversed(range(1, len(layers))):
        layers[i-1].insert(0, layers[i-1][0] - layers[i][0])
    return layers

f = open("input_1.txt", 'r')
# f = open("test_input.txt", 'r')
lines = f.readlines()
f.close()

total = 0
all_layers = []
for line in lines:
    temp_layer = [int(k) for k in line.strip().split()]
    all_layers.append(temp_layer)
    total += full_calculation(temp_layer)

print(total)
