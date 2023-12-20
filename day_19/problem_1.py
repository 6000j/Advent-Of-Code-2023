# Day 19 problem 1

from enum import Enum
from functools import cache

# Taken from https://www.geeksforgeeks.org/python-transpose-elements-of-two-dimensional-list/
def transpose(inp):
    # print(len(inp))
    # print(len(inp[0]))
    oup = [[row[i] for row in inp] for i in range(len(inp[0]))]
    return oup

class Xmas_part:
    def __init__(self, x, m, a, s) -> None:
        self.x = x
        self.m = m
        self.a = a
        self.s = s
    
    def get_sum_of_parts(self) -> int:
        return self.x + self.m + self.a + self.s
    
    def __repr__(self) -> str:
        return "<x=" + str(self.x) + ", m=" + str(self.m) + ", a=" + str(self.a) + ", s=" + str(self.s) + ">"

class Rule:
    def __init__(self, tp_check, score_greater: bool, num_check, location_if_true, location_if_false) -> None:
        self.tp_check = tp_check
        self.score_greater = score_greater
        self.location_if_true = location_if_true
        self.location_if_false = location_if_false
        self.num_check = num_check
    
    def check_rule(self, part: Xmas_part):
        passed = False
        if self.tp_check == 'x':
            if self.score_greater:
                passed = part.x > self.num_check
            else:
                passed = part.x < self.num_check
        elif self.tp_check == 'm':
            if self.score_greater:
                passed = part.m > self.num_check
            else:
                passed = part.m < self.num_check
        elif self.tp_check == 'a':
            if self.score_greater:
                passed = part.a > self.num_check
            else:
                passed = part.a < self.num_check
        elif self.tp_check == 's':
            if self.score_greater:
                passed = part.s > self.num_check
            else:
                passed = part.s < self.num_check
        
        if passed:
            return self.location_if_true
        else:
            return self.location_if_false
    
    # This is jank
    def fix_loc_if_true(self, dict_of_workflows):
        if self.location_if_true not in ['A', 'R'] and isinstance(self.location_if_true, str):
            if self.location_if_true in dict_of_workflows:
                self.location_if_true = dict_of_workflows[self.location_if_true].list_of_rules[0]
                # print(self)
                # print("\t", self.location_if_true.location_if_true)
        #     else:
        #         print("bad, rule named", self.location_if_true, "not in dict")
        # elif not isinstance(self.location_if_true, Rule):
        #     print(type(self.location_if_true), self.location_if_true)
                
    def __repr__(self):
        oup = "<" + self.tp_check
        if self.score_greater:
            oup += ">"
        else:
            oup += "<"
        oup += str(self.num_check) + ">"
        # oup += + ":" + self.location_if_false
        return oup

class Workflow:
    def __init__(self, name, list_of_rules) -> None:
        header_rule = Rule('x', True, -1, list_of_rules[0], None)
        self.name = name
        self.list_of_rules = [header_rule] + list_of_rules

        
    def run_workflow(self, part: Xmas_part):
        curr_rule = self.list_of_rules[0]

        while isinstance(curr_rule, Rule):
            # print(curr_rule)
            # if curr_rule.location_if_true == None:
            #     print("\trule failed true", curr_rule)
            # if curr_rule.location_if_false == None:
            #     print("\trule failed false", curr_rule)
            curr_rule = curr_rule.check_rule(part)
        if curr_rule == 'A':
            # print('\tScored!:', part.get_sum_of_parts())
            return part.get_sum_of_parts()
        elif curr_rule == 'R':
            # print('\tFailed :(')
            return 0
        else:
            print("Error, non-Rule rule of value", curr_rule)
            return None
        
    def fix_rules(self):
        # setting up the chain
        for i in range(len(self.list_of_rules)-1):
            self.list_of_rules[i].location_if_false = self.list_of_rules[i+1]


f = open("input_1.txt", 'r')
# f = open("test_input.txt", 'r')
# lines = f.readlines()
blocks = f.read().split("\n\n")
f.close()

block_clean = []
for block in blocks:
    block_clean.append([line.strip() for line in block.splitlines()])

# blocks[0] are our rules, blocks[1] are our parts

# processing each line into a workflow
workflows = {}
for line in block_clean[0]:
    nm, rule_string = line.split('{')
    rule_string = rule_string.strip()[:-1]
    rules_split = rule_string.split(',')
    lst_of_rules = []
    # The last one is unconditional, so we need to take special actions there
    for i in range(len(rules_split)-1):
        rl = rules_split[i]
        [chk_string, destination] = rl.split(':')
        if '>' in chk_string:
            is_greater = True
            [chk_type, chk_score] = chk_string.split('>')
        else:
            is_greater = False
            [chk_type, chk_score] = chk_string.split('<')
        chk_score = int(chk_score)
        rul = Rule(chk_type, is_greater, chk_score, destination, None)
        lst_of_rules.append(rul)
    # Acting upon the last one
    rl = rules_split[-1]
    rul = Rule('x', True, -1, rl, None)
    lst_of_rules.append(rul)
    wkflow = Workflow(nm, lst_of_rules)
    workflows[nm] = wkflow

# Fixing them all
for workfl in workflows.values():
    for rl in workfl.list_of_rules:
        rl.fix_loc_if_true(workflows)
    workfl.fix_rules()

# Now we have to do parts:
prts = []
for line in block_clean[1]:
    line_good = line.strip()[1:-1].split(',')
    scores = []
    for k in line_good:
        scores.append(int(k.split('=')[1]))
    prts.append(Xmas_part(scores[0], scores[1], scores[2], scores[3]))

total = 0
for prt in prts:
    # print(prt)
    total += workflows['in'].run_workflow(prt)
print(total)

