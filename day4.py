import numpy as np

# Read data
numbers = np.loadtxt("data/day4_numbers.txt", dtype=np.int_, delimiter=",")
boards = np.loadtxt("data/day4_boards.txt", dtype=np.int_)

# Board info
BOARD_SIZE = 5

# Rearrange data
boards = np.array(np.split(boards, int(boards.shape[0] / BOARD_SIZE)))

idx = numbers.shape[0]
potential_boards = boards
bingo_boards = np.repeat(True, boards.shape[0])
while potential_boards.shape[0] > 1 and idx > 0:
    idx = int(idx / 2)
    has_numbers = np.isin(potential_boards, numbers[:idx])
    bingo_axis_1 = np.sum(np.sum(has_numbers, axis=1) >= BOARD_SIZE, axis=1)
    bingo_axis_2 = np.sum(np.sum(has_numbers, axis=2) >= BOARD_SIZE, axis=1)
    bingo_boards = np.logical_or(bingo_axis_1, bingo_axis_2)
    potential_boards = potential_boards[bingo_boards]

# Find marked numbers in the final board
matching_numbers = np.isin(potential_boards, numbers[:idx])
bingo_col = np.sum(matching_numbers, 1) == BOARD_SIZE
bingo_row = np.sum(matching_numbers, 2) == BOARD_SIZE

# Extract the numbers in the bingo line
if np.sum(bingo_col):
    bingo_numbers = potential_boards[0, :, bingo_col[0]]
else:
    bingo_numbers = potential_boards[0, bingo_row[0], :]

# Find when the numbers in the bingo line were called and pick the last
called_idxs = np.argwhere(np.isin(numbers[:idx], bingo_numbers[0]))
last_called_idx = np.max(called_idxs)
last_called = numbers[last_called_idx]

# Answer part 1:
uncalled = ~np.isin(potential_boards, numbers[:last_called_idx + 1])
total_uncalled = np.sum(potential_boards[uncalled])
print(last_called * total_uncalled)
