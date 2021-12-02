from day2_data import data
import numpy as np
import re

directions = np.array(re.split('[\n \s]', data), dtype=np.str_)

strings = directions[::2]
values = directions[1::2].astype(np.int8)

distance_forward = np.sum(values[strings == "forward"])
distance_down = np.sum(values[strings == "down"])
distance_up = np.sum(values[strings == "up"])

print(distance_forward * (distance_down - distance_up))
