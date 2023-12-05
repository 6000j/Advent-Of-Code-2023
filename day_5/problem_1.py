# Day 5 problem 1

import re
def parse_map(dict_edit, our_lines):
    for a_line in our_lines:
        line = a_line.strip()
        if len([int(v) for v in line.split()]) == 3:
        # (src, dst, len) = [int(v) for v in line.split()]
            dict_edit.append([int(v) for v in line.split()])
    # print(dict_edit)
    return dict_edit

def get_pair(inp_val, map_to_check):
    
    for [dst, src, len] in map_to_check:
        # print(src, inp_val, len)
        if inp_val in range(src, src+len):
            return dst+(inp_val-src)
    return inp_val

# f = open("input_1.txt", 'r')
#f = open("test_input.txt", 'r')
inp = f.read()
map_batches = re.split(r"^.+-to-.+ map:\n", inp, flags=re.M)
f.close()

# print(map_batches)
# for batch in map_batches:
#     print(batch.split("\n")[0])

# Seeds
seeds = [int(v) for v in map_batches[0].split()[1:]]
maps = []
end_scores = []
# Maps
for batch in map_batches[1:]:
    new_map = []
    batch_lines = batch.splitlines()
    parse_map(new_map, batch_lines)
    maps.append(new_map)
    # print("made a batch")

print("Made maps successfully")
for seed in seeds:
    val = int(seed)
    print(val)
    for map in maps:
        val = get_pair(val, map)
        # print(f"\t{val}")
    # print(seed, val)
    end_scores.append(val)

print(min(end_scores))
