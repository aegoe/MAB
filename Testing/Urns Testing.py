import scipy.stats as ss
import numpy as np
import matplotlib.pyplot as plt
import random
from collections import Counter

Urn_1 = [('Black', 1), ('Yellow', 5), ('Blue', 3), ('Green', 1)]

Urn_2 = [('Black', 1), ('Yellow', 3), ('Blue', 5), ('Green', 1)]

Urn_3 = [('White', 1), ('Yellow', 5), ('Black', 3), ('Green', 1)]

while True:
    while True:
        try:
            Urn_1_input = input('How often do you want to draw from Option 1? ')
            Urn_1_input_val = int(Urn_1_input)
            break
        except ValueError:
            print('You can only choose a number between 0 and 10')

    while True:
        try:
            Urn_2_input = input('How often do you want to draw from Option 2? ')
            Urn_2_input_val = int(Urn_2_input)
            break
        except ValueError:
            print('You can only choose a number between 0 and 10')

    while True:
        try:
            Urn_3_input = input('How often do you want to draw from Option 3? ')
            Urn_3_input_val = int(Urn_3_input)
            break
        except ValueError:
            print('You can only choose a number between 0 and 10')

    Urn_input_overall = Urn_1_input_val + Urn_2_input_val + Urn_3_input_val
    if Urn_input_overall == 10:
        break
    elif Urn_input_overall < 10:
        print('You need to spend all 10 points')
    elif Urn_input_overall > 10:
        print('You can only spend 10 points')


print(Urn_1_input_val)
print(Urn_2_input_val)
print(Urn_3_input_val)

# data_inputs = {}
# data_inputs['Urn_1_input'] = Urn_1_input
# data_inputs['Urn_2_input'] = Urn_2_input
# data_inputs['Urn_3_input'] = Urn_3_input

#print(data_inputs)

    # for k, v in data_inputs.items():
    #     try:
    #         data_inputs[k] = int(v)
    #         break
    #     except ValueError:
    #         print('You can only choose a number between 0 and 10')


# print(data_inputs)





Draw_1 = [val for val, cnt in Urn_1 for i in range(cnt)]
Draw_2 = [val for val, cnt in Urn_2 for i in range(cnt)]
Draw_3 = [val for val, cnt in Urn_3 for i in range(cnt)]

draws_1 = random.choices(Draw_1, k=Urn_1_input_val)
draws_2 = random.choices(Draw_2, k=Urn_2_input_val)
draws_3 = random.choices(Draw_3, k=Urn_3_input_val)

#Draw_1 = random.choices(Urn_1, k = 10)
#Draw_2 = random.choices(Urn_2, k = 10)
#Draw_3 = random.choices(Urn_3, k = 10)

print(Draw_1)
print(draws_1)

count_1 = Counter(draws_1)
count_2 = Counter(draws_2)
count_3 = Counter(draws_3)

data_counts = {}
data_counts['count_1'] = count_1
data_counts['count_2'] = count_2
data_counts['count_3'] = count_3


print(count_1)
print(data_counts)

for i in data_counts.keys():
    for k, v in data_counts[i].items():
        if k == 'Black':
            data_counts[i][k] = v * -1
        elif k == 'Yellow':
            data_counts[i][k] = v * 0
        elif k == 'Blue':
            data_counts[i][k] = v * 1
        elif k == 'Green':
            data_counts[i][k] = v * 2
        elif k == 'White':
            data_counts[i][k] = v * -2


print(data_counts)

payoff = 0

for i in data_counts.keys():
    for values in data_counts[i].values():
        payoff += values

#for values in count_1.values():
#    payoff += values

print('You total payoff for this round is: ', payoff)
