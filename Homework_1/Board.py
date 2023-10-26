from Cell import Cell
import copy
import sys

sys.setrecursionlimit(24000)


class Board:
    def is_finished(self, matrix):
        before_value = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if matrix[i][j].get_value() != before_value + 1:
                    print("The game isn't done yet.")
                    return False
                if before_value != self.rows * self.cols - 2:
                    before_value += 1
                else:
                    before_value = -1
        print("The game is over!")
        self.display_matrix(matrix)
        exit(1)

    def is_equal(self, matrix, final_matrix):
        for i in range(self.rows):
            for j in range(self.cols):
                if matrix[i][j].get_value() != final_matrix[i][j]:
                    return False

        return True
    def count_steps(self, i, j, ij, ji):
        row_distance = abs(i - ij)
        column_distance = abs(j - ji)
        return row_distance + column_distance

    def calculate_manhattan_distance(self, current_state, final_state):
        sum = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if current_state[i][j].get_value() == 0:
                    continue

                steps = 0
                for ij in range(self.rows):
                    for ji in range(self.cols):
                        if current_state[i][j].get_value() == final_state[ij][ji]:
                            steps = self.count_steps(i, j, ij, ji)
                            sum += steps


        print(sum)

        return sum


    def find_final_state(self, matrix):
        new_matrix = []
        value = 0
        minim = 1000000
        final_state = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(value)
                value += 1
            new_matrix.append(row)

        distance = self.calculate_manhattan_distance(matrix, new_matrix)
        if minim > distance:
            minim = distance
            final_state = copy.deepcopy(new_matrix)

        for i in range(self.rows):
            for j in range(self.cols):
                if i == self.rows - 1 and j == self.cols - 1:
                    break
                if j + 1 == self.cols and i < self.rows - 1:
                    temp = new_matrix[i + 1][0]
                    new_matrix[i + 1][0] = new_matrix[i][j]
                    new_matrix[i][j] = temp
                else:
                    temp = new_matrix[i][j + 1]
                    new_matrix[i][j + 1] = new_matrix[i][j]
                    new_matrix[i][j] = temp

                distance = self.calculate_manhattan_distance(matrix, new_matrix)
                if minim > distance:
                    minim = distance
                    final_state = copy.deepcopy(new_matrix)

        return final_state

    def initialize_matrix(self, state):
        matrix = []
        frequency = [0] * (self.rows * self.cols)
        for i in range(self.rows):
            cell_row = []
            for j in range(self.cols):
                value = state[i][j]
                if value == 0:
                    poz_x_empty = i
                    poz_y_empty = j
                if value >= self.rows * self.cols or value < 0:
                    print("Incorrect values entered.")
                    exit(-1)

                frequency[value] += 1
                cell = Cell(i, j, value)
                cell_row.append(cell)

            matrix.append(cell_row)

        for i in range(self.rows * self.cols):
            if frequency[i] != 1:
                print("Values entered are not valid.")
                exit(-2)

        print("Initial board is:")
        self.display_matrix(matrix)
        return matrix, poz_x_empty, poz_y_empty

    def __init__(self, rows, cols, initial_state):
        self.rows = rows
        self.cols = cols
        self.dir = [[-1, 0], [0, -1], [1, 0], [0, 1]]
        matrix, poz_x_empty, poz_y_empty = self.initialize_matrix(initial_state)
        self.initial_matrix = copy.deepcopy(matrix)
        final_state = self.find_final_state(matrix)
        self.start_moving_Greedy(matrix, poz_x_empty, poz_y_empty, final_state)
        #self.start_moving(matrix, poz_x_empty, poz_y_empty, 1, 1) IDDFS

    def check_state(self, matrix):
        for i in range(self.rows):
            for j in range(self.cols):
                if matrix[i][j].get_value() != self.initial_matrix[i][j].get_value():
                    return False

        return True

    def start_moving(self, matrix, poz_x_empty, poz_y_empty, limit, backwards_limit):
        if not self.is_finished(matrix) and limit == 0:
            return
        for i in range(4):
            next_x = poz_x_empty + self.dir[i][0]
            next_y = poz_y_empty + self.dir[i][1]

            if self.verify_move(matrix, poz_x_empty, poz_y_empty, next_x, next_y):
                new_matrix = self.make_move(matrix, poz_x_empty, poz_y_empty, next_x, next_y)
                self.start_moving(new_matrix, next_x, next_y, limit - 1, backwards_limit + 1)

        if backwards_limit == 1:
            self.start_moving(matrix, poz_x_empty, poz_y_empty, limit + 1, 1)

    def display_matrix(self, matrix):
        for i in range(self.rows):
            for j in range(self.cols):
                print(matrix[i][j].get_value(), end=" ")
            print()

        print("-------")

    def refresh_recently_moved(self, matrix):
        for i in range(self.rows):
            for j in range(self.cols):
                matrix[i][j].set_recently_moved(False)

    def verify_move(self, matrix, x1, y1, x2, y2):
        if x2 < 0 or x2 >= self.rows or y2 < 0 or y2 >= self.cols:
            print("Invalid move, the cells are out of range.")
            return False
        first_cell = matrix[x1][y1]
        second_cell = matrix[x2][y2]
        if abs(x1 - x2) == 1 and y1 == y2:
            pass
        elif x1 == x2 and abs(y1 - y2) == 1:
            pass
        else:
            print("Invalid move, the cells must be next to each other.")
            return False

        if not first_cell.is_moveable() or not second_cell.is_moveable():
            print("Invalid move, the cell was moved 1 step before.")
            return False

        return True

    def make_move(self, matrix, x1, y1, x2, y2):
        new_matrix = copy.deepcopy(matrix)
        first_cell = new_matrix[x1][y1]
        second_cell = new_matrix[x2][y2]
        self.refresh_recently_moved(new_matrix)
        first_cell.set_recently_moved(True)

        temp_value = first_cell.get_value()
        first_cell.set_value(second_cell.get_value())
        second_cell.set_value(temp_value)

        self.display_matrix(new_matrix)
        return new_matrix


    def start_moving_Greedy(self, matrix, poz_x_empty, poz_y_empty, final_state):
        if self.is_equal(matrix, final_state):
            print("The game is over!")
            self.display_matrix(matrix)
            exit(1)

        minim = 1000000
        next_matrix = []
        for i in range(4):
            next_x = poz_x_empty + self.dir[i][0]
            next_y = poz_y_empty + self.dir[i][1]

            if self.verify_move(matrix, poz_x_empty, poz_y_empty, next_x, next_y):
                new_matrix = self.make_move(matrix, poz_x_empty, poz_y_empty, next_x, next_y)
                distance = self.calculate_manhattan_distance(new_matrix, final_state)
                if minim > distance:
                    minim = distance
                    next_matrix = copy.deepcopy(new_matrix)
                    final_x = next_x
                    final_y = next_y

        self.start_moving_Greedy(next_matrix, final_x, final_y, final_state)
