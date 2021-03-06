#!/usr/bin/python3
import sys


def read_file(filename):
    with open(filename) as f:
        return f.read()


def write_file(filename, s):
    with open(filename, 'w') as f:
        return f.write(s)


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
                result += ','
            result = result[:-1]
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
    for n in range(1, 10):
        new_board.set_cell(x, y, n)
        if not new_board.valid_cell(x, y):
            continue
        result = solve(new_board)
        if result is None:
            continue
        else:
            return result
    return None


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
    _, board_list_file, out_file, board_header = sys.argv
    board_str_list = read_file(board_list_file).strip().split('\n\n')
    boards = {}
    for board_data in board_str_list:
        header = board_data.split('\n')[0]
        board_str = '\n'.join(board_data.split('\n')[1:])  # Strip header
        board = str_to_board(board_str)
        boards[header] = board
    puzzle = boards[board_header]
    solution = solve(puzzle)
    start, name, _ = board_header.split(',')
    result_header = '{start},{name},solved'.format(start=start, name=name)
    output_str = result_header + '\n' + str(solution)
    write_file(out_file, output_str)


if __name__ == "__main__":
    main()

