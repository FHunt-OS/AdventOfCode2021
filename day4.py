import numpy as np


class IndexFinder:

    def __init__(self, min_idx, max_idx, priority):
        self.min_idx = int(min_idx)
        self.max_idx = int(max_idx)
        self.idx = int(max_idx / 2)
        self.priority = priority

    def next_search_idx(self, n_boards):
        if self.priority == "first":
            return self._idx_towards_first(n_boards)
        elif self.priority == "last":
            return self._idx_towards_last(n_boards)

    def _idx_towards_first(self, n_boards):
        if n_boards > 1:
            self.max_idx = self.idx
            self.idx = self.idx - int((self.idx - self.min_idx) / 2)
        else:
            self.min_idx = self.idx
            self.idx = self.idx + int((self.max_idx - self.idx) / 2)
        return self.idx

    def _idx_towards_last(self, n_boards):
        if n_boards > 0:
            self.min_idx = self.idx
            self.idx = self.idx + int((self.max_idx - self.idx) / 2)
        else:
            self.max_idx = self.idx
            self.idx = self.idx - int((self.idx - self.min_idx) / 2)
        return self.idx


def get_first_board(numbers, boards, board_size):
    potential_boards = boards
    idx_finder = IndexFinder(0, numbers.shape[0], "first")
    idx = idx_finder.idx
    while potential_boards.shape[0] != 1:
        bingo_boards = has_bingo(potential_boards, numbers[:idx], board_size)
        potential_boards = potential_boards[bingo_boards]
        idx = idx_finder.next_search_idx(potential_boards.shape[0])
    return {"board": potential_boards,
            "idx": idx}


def get_last_board(numbers, boards, board_size):
    potential_boards = boards
    idx_finder = IndexFinder(0, numbers.shape[0], "last")
    idx = idx_finder.idx
    while potential_boards.shape[0] != 1:
        bingo_boards = has_bingo(boards, numbers[:idx], board_size)
        potential_boards = boards[~bingo_boards]
        idx = idx_finder.next_search_idx(potential_boards.shape[0])
    return {"board": potential_boards,
            "idx": idx}


def has_bingo(boards, numbers, board_size):
    # Check which boards have bingo
    has_numbers = np.isin(boards, numbers)
    bingo_axis_1 = np.sum(np.sum(has_numbers, axis=1) >= board_size, axis=1)
    bingo_axis_2 = np.sum(np.sum(has_numbers, axis=2) >= board_size, axis=1)
    bingo_boards = np.logical_or(bingo_axis_1, bingo_axis_2)
    return bingo_boards


def get_bingo_number_idx(numbers, potential_boards, idx, board_size):
    # Find marked numbers in the final board
    matching_numbers = np.isin(potential_boards, numbers[:idx])
    bingo_col = np.sum(matching_numbers, 1) == board_size
    bingo_row = np.sum(matching_numbers, 2) == board_size

    # Extract the numbers in the bingo line
    if np.sum(bingo_col):
        bingo_numbers = potential_boards[0, :, bingo_col[0]]
    else:
        bingo_numbers = potential_boards[0, bingo_row[0], :]

    # Find when the numbers in the bingo line were called and pick the last
    called_idxs = np.argwhere(np.isin(numbers[:idx], bingo_numbers[0]))
    return np.max(called_idxs)


def get_score(numbers, last_board, bingo_number_idx):
    last_called = numbers[bingo_number_idx]
    uncalled = ~np.isin(last_board, numbers[:bingo_number_idx + 1])
    total_uncalled = np.sum(last_board[uncalled])
    return last_called * total_uncalled


if __name__ == "__main__":
    # Read data
    numbers = np.loadtxt("data/day4_numbers.txt", dtype=np.int_, delimiter=",")
    boards = np.loadtxt("data/day4_boards.txt", dtype=np.int_)

    # Board info
    board_size = boards.shape[1]

    # Rearrange data
    boards = np.array(np.split(boards, int(boards.shape[0] / board_size)))

    # Part 1
    first_board = get_first_board(numbers, boards, board_size)
    bingo_number_idx = get_bingo_number_idx(numbers, first_board["board"],
                                            first_board["idx"], board_size)
    print(get_score(numbers, first_board["board"], bingo_number_idx))

    # Part 2
    last_board = get_last_board(numbers, boards, board_size)
    bingo_number_idx = get_bingo_number_idx(numbers, last_board["board"],
                                            last_board["idx"], board_size)
    print(get_score(numbers, last_board["board"], bingo_number_idx))
