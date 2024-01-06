import copy
import time


class SudokuCSP:
    def initialize_domains(self, *domains):
        for domain in domains:
            for i in range(9):
                list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                domain.append(list)

    def initialize_instance(self, matrix_values, row_domains, col_domains, region_domains):
        for i in range(len(matrix_values)):
            for j in range(len(matrix_values[i])):
                if matrix_values[i][j] in row_domains[i]:
                    row_domains[i].remove(matrix_values[i][j])
                if matrix_values[i][j] in col_domains[j]:
                    col_domains[j].remove(matrix_values[i][j])
                if matrix_values[i][j] in region_domains[(i // 3) * 3 + j // 3]:
                    region_domains[(i // 3) * 3 + j // 3].remove(matrix_values[i][j])

    def forwardchecking_sudoku(self, matrix_values, row_domains, col_domains, region_domains, i, j):
        #self.display_matrix(matrix_values)
        #print("-----------")
        # time.sleep(5)

        if i == len(matrix_values):
            return matrix_values

        if matrix_values[i][j] <= 0:
            set_row = set(row_domains[i])
            set_col = set(col_domains[j])
            set_reg = set(region_domains[(i // 3) * 3 + j // 3])

            value_domain = list(set_row & set_col & set_reg)

            if matrix_values[i][j] == -1:
                for element in value_domain:
                    if element % 2 == 0:
                        matrix_values[i][j] = element

                        next_row_domains = copy.deepcopy(row_domains)
                        next_col_domains = copy.deepcopy(col_domains)
                        next_reg_domains = copy.deepcopy(region_domains)
                        next_row_domains[i].remove(element)
                        next_col_domains[j].remove(element)
                        next_reg_domains[(i // 3) * 3 + j // 3].remove(element)

                        next_i = i
                        next_j = j + 1
                        if next_j == len(matrix_values[i]):  # final pos on row
                            next_j = 0
                            next_i = i + 1

                        is_finished = self.forwardchecking_sudoku(matrix_values, next_row_domains, next_col_domains, next_reg_domains,
                                                    next_i, next_j)
                        if is_finished:
                            return is_finished

                matrix_values[i][j] = -1
            elif matrix_values[i][j] == 0:
                for element in value_domain:
                    matrix_values[i][j] = element

                    next_row_domains = copy.deepcopy(row_domains)
                    next_col_domains = copy.deepcopy(col_domains)
                    next_reg_domains = copy.deepcopy(region_domains)
                    next_row_domains[i].remove(element)
                    next_col_domains[j].remove(element)
                    next_reg_domains[(i // 3) * 3 + j // 3].remove(element)

                    next_i = i
                    next_j = j + 1
                    if next_j == len(matrix_values[i]):  # final pos on row
                        next_j = 0
                        next_i = i + 1

                    is_finished = self.forwardchecking_sudoku(matrix_values, next_row_domains, next_col_domains, next_reg_domains,
                                                next_i, next_j)
                    if is_finished:
                        return is_finished
                matrix_values[i][j] = 0

        else:
            next_i = i
            next_j = j + 1
            if next_j == len(matrix_values[i]):  # final pos on row
                next_j = 0
                next_i = i + 1

            is_finished = self.forwardchecking_sudoku(matrix_values, row_domains, col_domains, region_domains, next_i, next_j)

            if is_finished:
                return is_finished

        return False


    def __init__(self, matrix):
        matrix_values = matrix
        row_domains = []
        col_domains = []
        region_domains = []
        initial_i = 0
        initial_j = 0
        self.flag = False
        self.initialize_domains(row_domains, col_domains, region_domains)
        self.initialize_instance(matrix_values, row_domains, col_domains, region_domains)
        final_matrix = self.forwardchecking_sudoku(matrix_values, row_domains, col_domains, region_domains, initial_i, initial_j)
        if final_matrix:
            print("There is the solution for our sudoku:")
            self.display_matrix(final_matrix)
            print()
        else:
            print("There is no solution for this sudoku.")
            print()

    def display_matrix(self, matrix):
        for row in matrix:
            print(row)


if __name__ == '__main__':
    instance = SudokuCSP([
        [0, -1, 0, 0, -1, 6, 0, 2, 0],
        [-1, -1, 9, 0, 1, 0, 0, -1, -1],
        [-1, 0, 0, -1, 0, -1, 9, -1, 5],
        [0, 0, -1, 4, 0, 0, -1, 5, 8],
        [7, -1, 8, -1, 0, 5, -1, 0, 0],
        [0, -1, 3, 0, -1, -1, 2, 0, 0],
        [-1, 7, -1, 0, 2, 1, 5, 0, -1],
        [0, 3, 0, 0, 0, 4, -1, 6, 2],
        [-1, 5, -1, -1, -1, 0, 7, 0, 1]])

    instance_false = SudokuCSP([
        [-1, -1, -1, -1, -1, 6, -1, 2, 0],
        [-1, -1, 9, 0, 1, 0, 0, -1, -1],
        [-1, 0, 0, -1, 0, -1, 9, -1, 5],
        [0, 0, -1, 4, 0, 0, -1, 5, 8],
        [7, -1, 8, -1, 0, 5, -1, 0, 0],
        [0, -1, 3, 0, -1, -1, 2, 0, 0],
        [-1, 7, -1, 0, 2, 1, 5, 0, -1],
        [0, 3, 0, 0, 0, 4, -1, 6, 2],
        [-1, 5, -1, -1, -1, 0, 7, 0, 1]])

    instance_problem = SudokuCSP([
        [8, 4, 0, 0, 5, 0, -1, 0, 0],
        [3, 0, 0, 6, 0, 8, 0, 4, 0],
        [0, 0, -1, 4, 0, 9, 0, 0, -1],
        [0, 2, 3, 0, -1, 0, 9, 8, 0],
        [1, 0, 0, -1, 0, -1, 0, 0, 4],
        [0, 9, 8, 0, -1, 0, 1, 6, 0],
        [-1, 0, 0, 5, 0, 3, -1, 0, 0],
        [0, 3, 0, 1, 0, 6, 0, 0, 7],
        [0, 0, -1, 0, 2, 0, 0, 1, 3]])
