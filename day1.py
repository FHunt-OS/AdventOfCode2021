from day1_data import data
import numpy as np

distance = np.array(data).astype(np.float64)

# Part 1
increase = np.diff(distance)
n_increase = np.sum(increase > 0)
print(n_increase)

# Part 2
distance_stacked = np.vstack((distance[:-2], distance[1:-1], distance[2:]))
sum_stacked = np.sum(distance_stacked, axis=0)
increase = np.diff(sum_stacked)
n_increase = np.sum(increase > 0)
print(n_increase)

