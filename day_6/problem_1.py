# Day 6 problem 1

# Simulating a race?

f = open("input_1.txt", 'r')
# f = open("test_input.txt", 'r')
lines = f.readlines()
f.close()

# Times 
times = [int(v) for v in lines[0].split()[1:]]
# Distances
distances = [int(v) for v in lines[1].split()[1:]]


total = 1
# We know this will look like a curve, so we want to find the start and end
for i in range(len(times)):
    min = 0
    max = 0
    time_avail = times[i]
    distance_to_beat = distances[i]
    for k in range(1, time_avail):
        dist_travelled = (k * (time_avail-k))
        if dist_travelled > distance_to_beat:
            min = k
            break
    for j in reversed(range(1, time_avail)):
        dist_travelled = (j * (time_avail-j))
        if dist_travelled > distance_to_beat:
            max = j
            break

    total = total * (max-min + 1)

print(total)