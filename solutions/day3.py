import numpy as np
from itertools import count

# Read data
report = np.genfromtxt("data/day3.txt", dtype=np.int_, delimiter=1)

# Part 1
gamma = np.sum(report, axis=0) > (report.shape[0] / 2)
epsilon = ~gamma
powers_of_two = 1 << np.arange(gamma.shape[0])[::-1]
gamma_decimal = gamma.dot(powers_of_two)
epsilon_decimal = epsilon.dot(powers_of_two)

print(gamma_decimal * epsilon_decimal)


# Part 2
def match_record(records, comparison_func):
    record = records.copy()
    counter = count()
    while record.shape[0] > 1:
        i = next(counter)
        bit_value = comparison_func(np.sum(record[:, i]), (record.shape[0] / 2))
        record = record[record[:, i] == bit_value]
    return record[0]

o2_record = match_record(report, np.greater_equal)
co2_record = match_record(report, np.less)
o2_rating = o2_record.dot(powers_of_two)
co2_rating = co2_record.dot(powers_of_two)

print(o2_rating * co2_rating)
