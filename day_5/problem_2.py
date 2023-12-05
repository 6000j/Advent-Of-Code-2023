# Day 5 problem 2

import re
import sys

class map_list:
    def __init__(self, maps):
        self.maps = maps

    def get_conversion(self, inp):
        for map in self.maps:
            if map.in_map(inp):
                return map.get_conversion(inp)
        return inp
    
    def sanity_check(self, largest_number_to_check):
        broken = 0
        for i in range(largest_number_to_check):
            k = 0
            for map in self.maps:
                if map.in_map(i):
                    k += 1
            if k > 1:
                print(f"{i} is in {k} maps!")
                broken = 1
        if broken == 0:
            print("Sanity check successful!")



class map_struct:
    def __init__(self, dst, src, lenst) -> None:
        self.dst = dst
        self.src = src
        self.lenst = lenst
        self.largest_src = src+lenst - 1
        self.largest_dst = dst+lenst - 1
        self.offset = self.dst - self.src

    def in_map(self, inp):
        return self.src <= inp and inp <= self.largest_src
    

    def get_conversion(self, inp):
        if self.in_map(inp):
            return inp + self.offset
        else:
            print(f"error, trying to convert {inp}, but my range is {self.src} to {self.largest_src}")
            return None
        
    def __repr__(self):
        return f'(dst: {self.dst}, src: {self.src}, len: {self.lenst})'
    


            
def concat_map_lists(fst, snd):
    good = []
    for map_fst in fst.maps:
        good = good + concat_map_to_list(map_fst, snd)
    # print(good)
    return map_list(good)

def concat_map_to_list(mp, list):
    good = []
    in_progress = [mp]
    new_in_progress = []
    for map_snd in list.maps:
        new_in_progress = []
        for proggers in in_progress:
            (concatted, leftovers) = concat_maps(proggers, map_snd)
            if concatted is not None:
                good.append(concatted)
            new_in_progress = new_in_progress + leftovers
            # for k in leftovers:
            #     new_in_progress.append(k)
        in_progress = new_in_progress
    good = good + new_in_progress
    # for k in new_in_progress:
    #     good.append(k)
    return good

def concat_maps(fst: map_struct, snd: map_struct):
    concatted = None
    leftovers = []
    start_of_overlap = max(fst.dst, snd.src)
    start_overlap_src_equiv = start_of_overlap - fst.offset
    end_of_overlap = min(fst.largest_dst, snd.largest_src)
    end_overlap_src_equiv = end_of_overlap - fst.offset

    if start_of_overlap <= end_of_overlap:
        concatted = map_struct(snd.get_conversion(start_of_overlap), start_overlap_src_equiv, end_of_overlap - start_of_overlap + 1)
        # if concatted.lenst == 0:
            # print("Zero!")
        if start_of_overlap > fst.dst:
            # if start_overlap_src_equiv - fst.src == 0:
                # print("Zero a!")
            leftovers.append(map_struct(fst.dst, fst.src, start_overlap_src_equiv - fst.src))
        if end_of_overlap < fst.largest_dst:
            # if fst.largest_src - end_overlap_src_equiv == 0:
                # print("Zero b!")
            leftovers.append(map_struct(fst.dst + end_overlap_src_equiv-fst.src + 1, end_overlap_src_equiv + 1, fst.largest_src - end_overlap_src_equiv))
    else:
        leftovers.append(fst)
    return (concatted, leftovers)


def parse_map(our_lines) -> map_list:
    map_st = []
    for a_line in our_lines:
        line = a_line.strip()
        if len([int(v) for v in line.split()]) == 3:
            [dst, src, lenst] = [int(v) for v in line.split()]
            map_st.append(map_struct(dst, src, lenst))
    # print(dict_edit)
    return map_list(map_st)


f = open("input_1.txt", 'r')
# f = open("test_input.txt", 'r')
inp = f.read()
map_batches = re.split(r"^.+-to-.+ map:\n", inp, flags=re.M)
f.close()

# print(map_batches)
# for batch in map_batches:
#     print(batch.split("\n")[0])

map_lists = []
end_scores = []
# Maps
for batch in map_batches[1:]:
    batch_lines = batch.splitlines()
    new_map = parse_map(batch_lines)
    map_lists.append(new_map)
    # print("made a batch")
print("Made maps successfully")

map_size = pow(10, 10)
# Trying to concat all maps
curr_maps = map_list([map_struct(0, 0, map_size)])

for i in range(0, len(map_lists)):
    # print(curr_maps.maps)
    curr_maps = concat_map_lists(curr_maps, map_lists[i])
curr_maps.sanity_check(100)
# print(curr_maps.maps)

# Testing something
seeds = [int(v) for v in map_batches[0].split()[1:]]
# for seed in seeds:
#     val = curr_maps.get_conversion(seed)
#     print(val) 

seed_list_tmp = []
for i in range(0, len(seeds)//2):
    seed_list_tmp.append(map_struct(seeds[2*i], seeds[2*i], seeds[2*i+1]))
seed_list = map_list(seed_list_tmp)

seed_list = concat_map_lists(seed_list, curr_maps)
min = sys.maxsize
for map in seed_list.maps:
    if map.dst < min:
        min = map.dst
print(min)
# print(seed_list.maps)
# # Making seeds
# for k in range(0, len(seed_base)//2):
#     base = seed_base[2*k]
#     length = seed_base[2*k+1]
#     for i in range(seed_base[2*k], seed_base[2*k] + seed_base[2*k+1] - 1):
#         val = i
#         # print(val)
#         for map in maps:
#             val = get_pair(val, map)
#         if val < current_best:
#             current_best = val
#             print(current_best)
#     print(k)



# # Seeds
# seed_base = [int(v) for v in map_batches[0].split()[1:]]
# print("seeds:", len(seed_base))
# seeds = []
# current_best = sys.maxsize
# for k in range(0, len(seed_base)//2):
#     base = seed_base[2*k]
#     length = seed_base[2*k+1]
#     for i in range(seed_base[2*k], seed_base[2*k] + seed_base[2*k+1] - 1):
#         val = i
#         # print(val)
#         for map in maps:
#             val = get_pair(val, map)
#         if val < current_best:
#             current_best = val
#             print(current_best)
#     print(k)
# print("total seeds", len(seeds))

# for seed in seeds:
#     val = int(seed)
#     print(val)
#     for map in maps:
#         val = get_pair(val, map)
#         # print(f"\t{val}")
#     # print(seed, val)
#     end_scores.append(val)
# print(end_scores)



# for seed in seeds:
#     val = int(seed)
#     # print(val)
#     for map in maps:
#         val = get_pair(val, map)
#         # print(f"\t{val}")
#     # print(seed, val)
#     end_scores.append(val)

# print(current_best)
