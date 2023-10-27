import time

from Board import Board


if __name__ == '__main__':
    rows = 3
    cols = 3
    initial_state_0 = [
        [8, 6, 7],
        [2, 5, 4],
        [0, 3, 1]
    ]
    initial_state_1 = [
        [2, 5, 3],
        [1, 0, 6],
        [4, 7, 8]
    ]
    initial_state_2 = [
        [2, 7, 5],
        [0, 8, 4],
        [3, 1, 6]
    ]
    strings = ["IDDFS", "manhattan", "hamming", "euclidean"]

    #matrix_iddfs_0 = Board(rows, cols, initial_state_0, strings[0])
    #matrix_manhattan_0 = Board(rows, cols, initial_state_0, strings[1])
    #matrix_hamming_0 = Board(rows, cols, initial_state_0, strings[2])
    #matrix_euclidean = Board(rows, cols, initial_state_0, strings[3])

    matrix_iddfs_1 = Board(rows, cols, initial_state_1, strings[0])
    time.sleep(3)
    matrix_manhattan_1 = Board(rows, cols, initial_state_1, strings[1])
    time.sleep(3)
    matrix_hamming_1 = Board(rows, cols, initial_state_1, strings[2])
    time.sleep(3)
    matrix_euclidean = Board(rows, cols, initial_state_1, strings[3])

    #matrix_iddfs_2 = Board(rows, cols, initial_state_2, strings[0])
    #matrix_manhattan_2 = Board(rows, cols, initial_state_2, strings[1])
    #matrix_hamming_2 = Board(rows, cols, initial_state_2, strings[2])
    #matrix_euclidean = Board(rows, cols, initial_state_2, strings[3])
