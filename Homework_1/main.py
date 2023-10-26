from Board import Board


if __name__ == '__main__':
    rows = 3
    cols = 3
    initial_state = [
        [0, 2, 1],
        [3, 4, 6],
        [5, 7, 8]
    ]

    matrix = Board(rows, cols, initial_state)
