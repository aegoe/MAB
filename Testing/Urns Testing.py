import scipy.stats as ss
import numpy as np
import matplotlib.pyplot as plt
import random
from collections import Counter

Urn_1 = [('Black', 1), ('Yellow', 5), ('Blue', 3), ('Green', 1)]

Urn_2 = [('Black', 1), ('Yellow', 3), ('Blue', 5), ('Green', 1)]

Urn_3 = [('White', 1), ('Yellow', 5), ('Black', 3), ('Green', 1)]

Draw_1 = [val for val, cnt in Urn_1 for i in range(cnt)]

random.choices(Draw_1, k=10)

#Draw_1 = random.choices(Urn_1, k = 10)
#Draw_2 = random.choices(Urn_2, k = 10)
#Draw_3 = random.choices(Urn_3, k = 10)

print(Draw_1)
count_1 = Counter(Draw_1)
print(count_1)

for k, v in count_1.items():
    if k == 'Black':
        count_1[k] = v * -1
    elif k == 'Yellow':
        count_1[k] = v * 0
    elif k == 'Blue':
        count_1[k] = v * 1
    elif k == 'Green':
        count_1[k] = v * 2

print(count_1)

payoff = 0
for values in count_1.values():
    payoff += values

print(payoff)
