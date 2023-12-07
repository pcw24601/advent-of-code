time = 44806572
distance = 208158110501102

answer_this_race = 0
for charge in range(time):
    my_dist = charge * (time - charge)
    if my_dist > distance:
        answer_this_race += 1 

print(answer_this_race)