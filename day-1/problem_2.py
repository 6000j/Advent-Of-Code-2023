
f = open("problem_1_input.txt", 'r')

#f = open("test_input.txt", 'r')
# g = open('test_output.txt', 'w')

numbers = {'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9}
total = 0
# First we have to turn the words into numbers
for line in f:
    # This will work once we convert all the inputs
    curr_line = 0
    for i in range(0, len(line)):
        if line[i].isdigit():
            curr_line += 10*int(line[i])
            break
        for k in numbers:
            if line.startswith(k, i):
                curr_line += 10*numbers.get(k)
                break
        if curr_line != 0:
            break

    segment = 0
    for i in range(len(line)-1, -1, -1):
        if line[i].isdigit():
            curr_line += int(line[i])
            break
        for k in numbers:
            if line[:i].endswith(k):
                curr_line += numbers.get(k)
                segment = 1
                break
        if segment != 0:
            break
    total += curr_line
            
f.close()
print(total)
