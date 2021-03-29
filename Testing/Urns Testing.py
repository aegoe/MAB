from scipy.stats import rv_discrete

import random
from collections import Counter

# x1 = [0, 1, 2, 3, 4, 5, 6, 7]
# px1= [0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.05]
#
# sample = rv_discrete(values=(x1,px1)).rvs(size=100)
#
# sample_mean = sample.mean()
# sample_sd = sample.std()
#
# print(sample_mean)
# print(sample_sd)

# x2 = [-20, -5, -4, -3, 35, 40, 50, 95]
# px2 = [0.2, 0.2, 0.2, 0.2, 0.05, 0.05, 0.05, 0.05]
#
# sample2 = rv_discrete(values=(x2,px2)).rvs(size=100)
#
# sample_mean2 = sample2.mean()
# sample_sd2 = sample2.std()
#
# print(sample_mean2)
# print(sample_sd2)
#


# x3 = [-2,8]
# px3 = [0.5,0.5]
#
# sample3 = rv_discrete(values=(x3,px3)).rvs(size=100)
#
# sample_mean3 = sample3.mean()
# sample_sd3 = sample3.std()
#
# print(sample_mean3)
# print(sample_sd3)


x1 = [0, 1, 2, 3, 20, 25, 35, 40]
px1= [0.25, 0.25, 0.15, 0.15, 0.05, 0.05, 0.05, 0.05]

sample = rv_discrete(values=(x1,px1)).rvs(size=100)

sample_mean = sample.mean()
sample_sd = sample.std()

print(sample_mean)
print(sample_sd)

#
# x3 = [0,100]
# px3 = [0.95,0.05]
#
# sample3 = rv_discrete(values=(x3,px3)).rvs(size=100)
#
# sample_mean3 = sample3.mean()
# sample_sd3 = sample3.std()
#
# print(sample_mean3)
# print(sample_sd3)

