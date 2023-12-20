# Day 20 problem 1
from enum import Enum
import copy
# Taken from https://www.geeksforgeeks.org/python-transpose-elements-of-two-dimensional-list/
def transpose(inp):
    # print(len(inp))
    # print(len(inp[0]))
    oup = [[row[i] for row in inp] for i in range(len(inp[0]))]
    return oup

class HighLow(Enum):
    LOW = 0
    HIGH = 1
    

class Module:
    state: HighLow
    destination_names: [str]
    destinations:["""Module"""]
    name: str

    def __init__(self, dest_names: [str], name) -> None:
        self.destinations = []
        self.destination_names = dest_names
        self.name = name
        self.points_to_rx = False

    # Updating the destinations, call once they've all been called
    def update_destinations(self, mod_dict) -> None:
        for dst in self.destination_names:
            if dst in mod_dict.keys():
                self.destinations.append(mod_dict[dst])
                # Code for Conjunction modules
                if isinstance(mod_dict[dst], Conjunction):
                    # print("hi")
                    mod_dict[dst].inputs.append([self, HighLow.LOW])
            else:
                self.destinations.append(Module([], dst))
    
    # Pushes the signals we make to the queue
    def recieve_signal(self, signal: HighLow, signal_queue: ["""Module""", HighLow, """Module"""], source: """Module""") -> None:
        pass

    def send_to_destinations(self, signal: HighLow, signal_queue: ["""Module""", HighLow, """Module"""]) -> None:
        for dst in self.destinations:
            signal_queue.append((dst, signal, self))
    
    def __repr__(self):
        return "<" + self.name + ":" + str(str(self.__class__).split('.')[1][:-2]) + ";" + str([dst.name for dst in self.destinations]) + ">" 
        

# Simple, easy
class Broadcaster(Module):
    def __init__(self, dest_names, name) -> None:
        super().__init__(dest_names, name)

    def recieve_signal(self, signal: HighLow, signal_queue: [("""Module""", HighLow, """Module""")], source: """Module""") -> None:
        self.send_to_destinations(signal, signal_queue)

class FlipFlop(Module):
    def __init__(self, dest_names, name) -> None:
        super().__init__(dest_names, name)
        self.state = HighLow.LOW
    
    def recieve_signal(self, signal: HighLow, signal_queue: ["""Module""", HighLow, """Module"""], source: """Module""") -> None:
        if signal == HighLow.LOW:
            if self.state == HighLow.LOW:
                self.state = HighLow.HIGH
                self.send_to_destinations(HighLow.HIGH, signal_queue)
            else:
                self.state = HighLow.LOW
                self.send_to_destinations(HighLow.LOW, signal_queue)
    
    def __repr__(self):
        return "<" + self.name + ":" + str(str(self.__class__).split('.')[1][:-2]) + "," + self.state.name + ";" + str([dst.name for dst in self.destinations]) + ">" 

class Conjunction(Module):
    inputs: [[Module, HighLow]]
    def __init__(self, dest_names: [str], name) -> None:
        super().__init__(dest_names, name)
        self.inputs = []

    def recieve_signal(self, signal: HighLow, signal_queue: ["""Module""", HighLow, """Module"""], source: """Module""") -> None:
        send_low = True
        for i in range(len(self.inputs)):
            if self.inputs[i][0] is source:
                # print("Updated in conjunctions")
                self.inputs[i][1] = signal
            if self.inputs[i][1] == HighLow.LOW:
                send_low = False
        if send_low:
            self.send_to_destinations(HighLow.LOW, signal_queue)
        else:
            self.send_to_destinations(HighLow.HIGH, signal_queue)

class RX_Mod(Module):
    counts_this_cycle: int
    def __init__(self, dest_names: [str], name) -> None:
        super().__init__(dest_names, name)
        self.counts_this_cycle = 0
    
    def recieve_signal(self, signal: HighLow, signal_queue: ["""Module""", HighLow, """Module"""], source: Module) -> None:
        if signal == HighLow.LOW:
            print("rx low!")
            self.counts_this_cycle += 1


def parse_module_line_add_to_dict(ln: str, modules_dict: {str: Module}) -> None:
    clean_line = ln.strip()
    [name_type, dest_names_str] = ln.split('->')
    # Handling name
    if name_type[0] == 'b':
        oup_name = 'broadcaster'
    else:
        oup_name = name_type.strip()[1:]
    
    # Handling destination names
    dest_names = []
    for k in dest_names_str.split(','):
        dest_names.append(k.strip())
    
    if name_type[0] == '%':
        insert_module = FlipFlop(dest_names, oup_name)
    elif name_type[0] == '&':
        insert_module = Conjunction(dest_names, oup_name)
    else:
        insert_module = Broadcaster(dest_names, oup_name)
    
    modules_dict[oup_name] = insert_module


f = open("input_1.txt", 'r')
# f = open("test_input.txt", 'r')
lines = f.readlines()
f.close()

# Parsing our modules
modules_dict: {str, Module} = {}
for line in lines:
    parse_module_line_add_to_dict(line, modules_dict)
modules_dict['button'] = Broadcaster(['broadcaster'], 'button')
rx_md = RX_Mod([], 'rx')
modules_dict['rx'] = rx_md

# Updating our modules
for md in modules_dict.values():
    md.update_destinations(modules_dict)

# And now we process them!
signal_queue: ["""Module""", HighLow, """Module"""] = []
# print(modules_dict['kl'].inputs)
rx_count = 0

i = 0
# rx_names = ['mk', 'fp', 'xt', 'zc']
# current_rx_approaching = [pt[1]==HighLow.HIGH for pt in modules_dict['kl'].inputs]
# print(current_rx_approaching)

baseline = {}
for k in modules_dict.keys():
    curr = modules_dict[k]
    if isinstance(curr, FlipFlop):
        baseline[k] = curr.state
    elif isinstance(curr, Conjunction):
        baseline[k] = [pt[1]==HighLow.HIGH for pt in curr.inputs]

# now we have to idk do some kind of comparison

while True:
    # print("Iteration", i)
    # print("Before iteration", i)
    # for val in modules_dict.values():
    #     print(val)
    # print("\n\n")
    rx_count = 0
    signal_queue.append((modules_dict['button'], HighLow.LOW, modules_dict['button']))
    # low_count -= 1
    while len(signal_queue) > 0:
        (dst, hl, src) = signal_queue.pop(0)

        # print(src.name, hl, dst.name)
        # if dst.name == "rx" and hl == HighLow.LOW:
        #     print('rx')
        #     rx_count += 1
        # if src.name == "kl" and [m[1] for m in src.inputs].count(HighLow.HIGH) > 1:
        #     print("Iteration", i, "Kl!:", [m[1] for m in src.inputs].count(HighLow.HIGH))
    # # elif hl == HighLow.HIGH:
        # if dst.name == 'kl':
        #     print(dst.name, "mentioned by", src.name, hl, [m[1] for m in dst.inputs])
            
        dst.recieve_signal(hl, signal_queue, src)
    i += 1

    if rx_md.counts_this_cycle == 1:
        g = open('oup_3.txt', 'wa')
        print("Done after", i, "iterations")
        g.write("Done after", i, "iterations")
        g.close()
        break
    elif rx_md.counts_this_cycle > 0:
        g = open('oup_3.txt', 'wa')
        print(rx_md.counts_this_cycle, "after", i, "iterations")
        g.write(rx_md.counts_this_cycle, "after", i, "iterations")
        g.close()
    else:
        rx_md.counts_this_cycle = 0

    if i % pow(10, 5) == 0:
        print("Done", i, "cycles")
    # changes = 0
    # last = None
    # temp = []
    # for k in modules_dict.keys():
    #     curr = modules_dict[k]
    #     if isinstance(curr, FlipFlop):
    #         if baseline[k] != curr.state:
    #             changes += 1
    #             last = (k, curr)
    #     elif isinstance(curr, Conjunction):
    #         if baseline[k] != [pt[1]==HighLow.HIGH for pt in curr.inputs]:
    #             changes += 1
    #             last = (k, [pt[1]==HighLow.HIGH for pt in curr.inputs])
    
    # if changes == 0:
    #     print("After", i, "cycles, nothing has changed??")
    # if changes == 1:
    #     print("After", i, "cycles, exactly one thing changed:")
    #     print('\t', last[0], last[1])
    # if [pt[1]==HighLow.HIGH for pt in modules_dict['kl'].inputs] != current_rx_approaching:
    #     print("After", i, "iterations, kl inputs have seen a change:")
    #     for m in range(len(current_rx_approaching)):
    #         if current_rx_approaching[m] != [pt[1]==HighLow.HIGH for pt in modules_dict['kl'].inputs][m]:
    #             print('\t', current_rx_approaching[m], ":", current_rx_approaching[m], "->", [pt[1]==HighLow.HIGH for pt in modules_dict['kl'].inputs])
    #     current_rx_approaching = [pt[1]==HighLow.HIGH for pt in modules_dict['kl'].inputs]

print("done")