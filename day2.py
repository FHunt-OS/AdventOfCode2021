from day2_data import data
import numpy as np
import re

directions = np.array(re.split('[\n \s]', data), dtype=np.str_)

instruction = directions[::2]
amount = directions[1::2].astype(np.int8)

forward = instruction == "forward"
down = instruction == "down"
up = instruction == "up"

# Part 1
distance_forward = np.sum(amount[forward])
distance_down = np.sum(amount[down])
distance_up = np.sum(amount[up])

change_in_depth = distance_down - distance_up
print(distance_forward * change_in_depth)

# Part 2
aim = amount.copy()

aim[instruction == "up"] = aim[up] * -1
aim[instruction == "forward"] = 0

aim_when_forward = np.cumsum(aim)[forward]
aim_changes = aim_when_forward * amount[forward]
change_in_depth = np.sum(aim_changes)

print(change_in_depth * distance_forward)
