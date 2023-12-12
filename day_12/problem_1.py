# Day 12 problem 1

class Spring_line:
    def __init__(self, chart, group_lengths, curr_consec=0, just_finished = False) -> None:
        self.chart = chart
        self.group_lengths = group_lengths
        self.curr_consec = curr_consec
        self.just_finished = just_finished


def construct_spring_line_from_line(line):
    good_line = line.strip()
    spring_chart = good_line.split()[0]
    second_half = good_line.split()[1]
    group_lengths = [int(v) for v in second_half.split(',')]
    return Spring_line(list(spring_chart), group_lengths)
  
    
        

def count_possibilities(spring_line: Spring_line):
    chart = spring_line.chart
    consecs = spring_line.group_lengths
    curr_cons = spring_line.curr_consec
    # print(chart, consecs, curr_cons)
    if len(chart) == 0:
        if curr_cons != 0:
            if len(consecs) != 1 or consecs[0] != curr_cons:
                # print("0")
                return 0
            else:
                # print('1')
                return 1
        elif len(consecs) != 0:
            # print("0")
            return 0
        else:
            # print('1')
            return 1
    # We're going to recurse, so no for loop needed
    c = chart[0]
    if chart[0] == '.':
        if curr_cons != 0:
            if len(consecs) > 0:
                # If we've poorly ended a segment
                if curr_cons != consecs[0]:
                    return 0
                # If we've properly ended a segment
                elif curr_cons != 0 and curr_cons == consecs[0]:
                    new_spring = Spring_line(chart[1:], consecs[1:], curr_consec=0)
                    return count_possibilities(new_spring)
        else:
            new_spring = Spring_line(chart[1:], consecs, curr_consec=0)
            return count_possibilities(new_spring)
    elif chart[0] == '#':
        if len(consecs) == 0:
            # print('0')
            return 0
        elif curr_cons > consecs[0]:
            # print('0')
            return 0
        else:
            new_spring = Spring_line(chart[1:], consecs, curr_consec = curr_cons+1)
            return count_possibilities(new_spring)
    elif chart[0] == '?':
        good_list = list(chart)
        good_list[0] = '.'
        # print(good_list)
        good_line = Spring_line(good_list, consecs, curr_consec = curr_cons)
        bad_list = list(chart)
        bad_list[0] = '#'
        # print(bad_list)
        bad_line = Spring_line(bad_list, consecs, curr_consec = curr_cons)
        return count_possibilities(good_line) + count_possibilities(bad_line)

    print('None')
    return None

f = open("input_1.txt", 'r')
# f = open("test_input.txt", 'r')
lines = f.readlines()
f.close()



total = 0
for line in lines:
    score = count_possibilities(construct_spring_line_from_line(line))
    total += score
    # print('\t', score)
print(total)