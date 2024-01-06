import copy


class play_scrable:
    class player:
        def __init__(self, value, name, next_player=None):
            self.value = value
            self.name = name
            self.next_player = next_player

    def who_won(self, matrix):
        game_in_progress = False
        possible_lines = 8
        for i in range(possible_lines):
            flag = False
            if i < 3:
                x = matrix[i][0][1] # owner of the first cell each line
                if x != 0:
                    for j in range(1, len(matrix[i])):
                        if x != matrix[i][j][1]:
                            flag = True
                            break
                    if flag:
                        continue

                    return x
                else:
                    game_in_progress = True
            elif i < 6:
                x = matrix[0][i % 3][1]  # owner of the first cell each col
                if x != 0:
                    for j in range(1, len(matrix)):
                        if x != matrix[j][i % 3][1]:
                            flag = True
                            break
                    if flag:
                        continue
                    return x
                else:
                    game_in_progress = True
            else:
                if i == 6: # first diagonal
                    if x != 0:
                        x = matrix[0][0][1]
                        for j in range(1, len(matrix)):
                            if x != matrix[j][j][1]:
                                flag = True
                                break
                        if flag:
                            continue

                        return x
                else:   # second diagonal
                    if x != 0:
                        x = matrix[0][2][1]
                        for j in range(len(matrix) - 1, -1, -1):
                            if x != matrix[len(matrix) - 1 - j][j][1]:
                                flag = True
                                break
                        if flag:
                            continue

                        return x

        for i in range(1, 3):
            for j in range(1, 3):
                if matrix[i][j][1] == 0:
                    game_in_progress = True

        if game_in_progress:
            return 2
        else:
            return 0

    def initialize_magic_matrix(self):
        matrix = ([
            [[2, 0], [7, 0], [6, 0]],
            [[9, 0], [5, 0], [1, 0]],
            [[4, 0], [3, 0], [8, 0]]])
        return matrix

    def validate(self, matrix, i, j):
        if matrix[i][j][1] != 0:
            return False
        else:
            return True

    def make_move(self, matrix, i, j, player):
        matrix[i][j][1] = player.value
        return matrix

    def __init__(self):
        magic_matrix = self.initialize_magic_matrix()
        A = self.player(1, 'A')
        B = self.player(-1, 'B')
        A.next_player = B
        B.next_player = A
        self.start_playing(magic_matrix, A)

    def check_rows(self, matrix, player):
        for i in range(len(matrix)):
            counter = 0
            for j in range(len(matrix)):
                if player.next_player.value == matrix[i][j][1]:
                    counter = 0
                    break
                if player.value == matrix[i][j][1]:
                    counter += 1
                elif matrix[i][j][1] == 0:
                    x, y = i, j
            if counter == 2:
                return x, y
        return False

    def check_columns(self, matrix, player):
        for i in range(len(matrix)):
            counter = 0
            for j in range(len(matrix)):
                if player.next_player.value == matrix[j][i][1]:
                    counter = 0
                    break
                if player.value == matrix[j][i][1]:
                    counter += 1
                elif matrix[j][i][1] == 0:
                    x, y = j, i

            if counter == 2:
                return x, y
        return False

    def check_first_diag(self, matrix, player):
        counter = 0
        for i in range(len(matrix)):
            if player.next_player.value == matrix[i][i][1]:
                counter = 0
                break
            if player.value == matrix[i][i][1]:
                counter += 1
            elif matrix[i][i][1] == 0:
                x, y = i, i
        if counter == 2:
            return x, y
        return False

    def check_second_diag(self, matrix, player):
        i = 0
        counter = 0
        for j in range(len(matrix) - 1, -1, -1):
            if player.next_player.value == matrix[i][j][1]:
                counter = 0
                break
            if player.value == matrix[i][j][1]:
                counter += 1
            elif matrix[i][j][1] == 0:
                x, y = i, j
            i += 1
        if counter == 2:
            return x, y
        return False

    def find_one_move_end(self, matrix, player):
        move = self.check_rows(matrix, player)
        if move:
            return move

        move = self.check_columns(matrix, player)
        if move:
            return move

        move = self.check_first_diag(matrix, player)
        if move:
            return move

        move = self.check_second_diag(matrix, player)
        if move:
            return move

        return False

    def find_cell_value(self, matrix, player, x, y):
        value = 0
        local_sum = 0
        for j in range(len(matrix[x])):
            if matrix[x][j][1] == player.next_player.value:
                value -= local_sum
                break
            elif matrix[x][j][1] == player.value:
                local_sum += 2
            else:
                local_sum += 1

        value += local_sum
        local_sum = 0

        for i in range(len(matrix)):
            if matrix[i][y][1] == player.next_player.value:
                value -= local_sum
                break
            elif matrix[i][y][1] == player.value:
                local_sum += 2
            else:
                local_sum += 1

        value += local_sum
        local_sum = 0

        if x == y:
            for i in range(len(matrix)):
                if matrix[i][i][1] == player.next_player.value:
                    value -= local_sum
                    break
                elif matrix[i][i][1] == player.value:
                    local_sum += 2
                else:
                    local_sum += 1

            value += local_sum
            local_sum = 0

        if len(matrix) - 1 == x + y:
            for j in range(len(matrix) - 1, -1, -1):
                if matrix[len(matrix) - 1 - j][j][1] == player.next_player.value:
                    value -= local_sum
                    break
                elif matrix[len(matrix) - 1 - j][j][1] == player.value:
                    local_sum += 2
                else:
                    local_sum += 1

            value += local_sum

        return value

    def calculate_best_move(self, matrix, player):
        one_move_win = self.find_one_move_end(matrix, player)
        if one_move_win:
            return one_move_win

        one_move_lose = self.find_one_move_end(matrix, player.next_player)
        if one_move_lose:
            return one_move_lose

        maximum = -1
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if self.validate(matrix, i, j):
                    value = self.find_cell_value(matrix, player, i, j)
                    if maximum < value:
                        best_move = i, j
                        maximum = value

        return best_move

    def start_playing(self, matrix, player):
        end = self.who_won(matrix)
        if end != 2:
            print(end)
            self.display_board(matrix)
            return
        i, j = self.calculate_best_move(matrix, player)
        self.make_move(matrix, i, j, player)
        if player.name == 'B':
            self.start_playing(matrix, player.next_player)
        else:
            look_forward = self.minimax(matrix, player.next_player, 2)
            if look_forward[0] == 2:
                self.start_playing(matrix, player.next_player)
            else:
                self.make_move(matrix, look_forward[1], look_forward[2], player.next_player)
                self.start_playing(matrix, player)

    def minimax(self, matrix, player, limit):
        if limit < 0:
            return 2, 1, 1
        new_matrix = copy.deepcopy(matrix)
        minimum = 1
        for i in range(len(new_matrix)):
            for j in range(len(new_matrix[i])):
                if self.validate(new_matrix, i, j):
                    self.make_move(new_matrix, i, j, player)
                    score = self.who_won(new_matrix)
                    if score != 2:
                        if minimum > score:
                            minimum = score
                            x, y = i, j
                        if score == 1:
                            return 1, i, j
                    else:
                        final_score = self.minimax(new_matrix, player.next_player, limit - 1)
                        if minimum > final_score[0]:
                            minimum = final_score[0]
                            x, y = i, j
                        new_matrix[i][j][1] = 0

        if minimum != 1:
            return minimum, x, y
        else:
            return 2, 1, 1

    def display_board(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                print(matrix[i][j][1], end="")
            print()
        print("---------------")
