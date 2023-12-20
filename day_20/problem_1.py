# Day 20 problem 1
from enum import Enum
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

# 
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

# Updating our modules
for md in modules_dict.values():
    md.update_destinations(modules_dict)

# And now we process them!
signal_queue: ["""Module""", HighLow, """Module"""] = []


low_count = 0
high_count = 0
for _ in range(1000):
    signal_queue.append((modules_dict['button'], HighLow.LOW, modules_dict['button']))
    low_count -= 1
    while len(signal_queue) > 0:
        (dst, hl, src) = signal_queue.pop(0)
        # print(src.name, hl, dst.name)
        if hl == HighLow.HIGH:
            high_count += 1
        else:
            low_count += 1
        dst.recieve_signal(hl, signal_queue, src)


print(low_count*high_count)