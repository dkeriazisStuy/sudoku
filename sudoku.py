import sys
import random


def read_file(filename):
    with open(filename) as f:
        return f.read()


class Board:
    valid_set = set(range(9))

    def __init__(self, rows):
        self.rows = rows

    def __str__(self):
        result = ''
        for row in self.rows:
            for cell in row:
                if cell is None:
                    result += '_'
                else:
                    result += str(cell)
                result += ' '
            result += '\n'
        return result

    def copy(self):
        return Board([row.copy() for row in self.rows])

    def get_row(self, y):
        return self.rows[y]

    def get_col(self, x):
        return [row[x] for row in self.rows]

    def get_block(self, x, y):
        block = []
        block_x = x * 3
        block_y = y * 3
        for i in range(block_y, block_y + 3):
            for j in range(block_x, block_x + 3):
                block.append(self.rows[i][j])
        return block

    def get_first_unfilled(self):
        for y, row in enumerate(self.rows):
            for x, cell in enumerate(row):
                if cell is None:
                    return x, y
        return None, None

    def get_cell(self, x, y):
        return self.rows[y][x]

    def set_cell(self, x, y, n):
        self.rows[y][x] = n

    def valid_row(self, y):
        row = [i for i in self.get_row(y) if i is not None]
        return len(set(row)) == len(row)  # Uniqueness test

    def valid_col(self, x):
        col = [i for i in self.get_col(x) if i is not None]
        return len(set(col)) == len(col)  # Uniqueness test

    def valid_block(self, x, y):
        block = [i for i in self.get_block(x, y) if i is not None]
        return len(set(block)) == len(block)  # Uniqueness test

    def valid_cell(self, x, y):
        return self.valid_row(y) \
                and self.valid_col(x) \
                and self.valid_block(x // 3, y // 3)


def solve(board):
    x, y = board.get_first_unfilled()
    if x is None or y is None:
        return board
    new_board = board.copy()
    nums = list(range(1, 10))
    random.shuffle(nums)
    for n in nums:
        new_board.set_cell(x, y, n)
        if not new_board.valid_cell(x, y):
            continue
        result = solve(new_board)
        if result is None:
            continue
        else:
            return result
    return None


def rand_board():
    row = [None for _ in range(9)]
    return solve(Board([row for _ in range(9)]))


def remove_rand(board):
    result = None
    while result is None:
        x = random.randrange(9)
        y = random.randrange(9)
        result = board.get_cell(x, y)
    board.set_cell(x, y, None)


def gen_board(num_blank):
    if num_blank == 0:
        return rand_board()
    else:
        result = None
        while result is None:
            result = gen_board(num_blank - 1)
        remove_rand(result)
        if solve(result) is None:
            return None
        else:
            return result



def str_to_board(board_str):
    rows_str = board_str.strip().split('\n')
    rows = []
    for row_str in rows_str:
        row = []
        for cell in row_str.split(','):
            if cell == '_':
                row.append(None)
            else:
                row.append(int(cell))
        rows.append(row)
    return Board(rows)


def main():
    board = gen_board(54)
    print(board)
    solution = solve(board)
    print(solution)


if __name__ == "__main__":
    main()

