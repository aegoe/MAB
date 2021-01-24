from scipy.stats import rv_discrete

import random
from collections import Counter

# x1 = [3, 4, 5, 6, 7, 8, 9, 10]
# px1= [0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.05]
#
# sample = rv_discrete(values=(x1,px1)).rvs(size=100)
#
# sample_mean = sample.mean()
# sample_sd = sample.std()
#
# print(sample_mean)
# print(sample_sd)

x2 = [0, 1, 2, 3, 20, 25, 35, 40]
px2 = [0.25, 0.25, 0.15, 0.15, 0.05, 0.05, 0.05, 0.05]

sample2 = rv_discrete(values=(x2,px2)).rvs(size=100)

sample_mean2 = sample2.mean()
sample_sd2 = sample2.std()

print(sample_mean2)
print(sample_sd2)