times = [44, 80, 65, 72]
distances = [208, 1581, 1050, 1102]

# times = [7,  15,   30]
# distances = [9,  40,  200]

answer = 1
for time, dist in zip(times, distances):
    answer_this_race = 0
    for charge in range(time):
        my_dist = charge * (time - charge)
        if my_dist > dist:
            answer_this_race += 1 
    answer *= answer_this_race

print(answer)