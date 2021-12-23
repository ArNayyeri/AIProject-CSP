from Board import Board


class CSP:
    def __init__(self, board: Board):
        self.board = board
        self.x = 1

    def check_limitation_row(self):
        for i in range(self.board.row):
            s = self.board.sum_row(i, True)  # positive count
            if s > self.board.row_limit_p[i]:
                return False

            if self.board.row_all[i] == self.board.col and s != self.board.row_limit_p[i]:
                return False

            s = self.board.sum_row(i, False)  # negative count
            if s > self.board.row_limit_n[i]:
                return False

            if self.board.row_all[i] == self.board.col and s != self.board.row_limit_n[i]:
                return False

        return True

    def check_limitation_col(self):
        for i in range(self.board.col):
            s = self.board.sum_col(i, True)  # positive count
            if s > self.board.col_limit_p[i]:
                return False

            if self.board.col_all[i] == self.board.row and s != self.board.col_limit_p[i]:
                return False

            s = self.board.sum_col(i, False)  # negative count
            if s > self.board.col_limit_n[i]:
                return False

            if self.board.col_all[i] == self.board.row and s != self.board.col_limit_n[i]:
                return False

        return True

    def check_goal(self):
        is_goal = 1
        for i in range(self.board.row):
            s = self.board.sum_row(i, True)  # positive count
            if s < self.board.row_limit_p[i]:
                is_goal = 0

            s = self.board.sum_row(i, False)  # negative count
            if s < self.board.row_limit_n[i]:
                is_goal = 0

        for i in range(self.board.col):
            s = self.board.sum_col(i, True)  # positive count
            if s < self.board.col_limit_p[i]:
                is_goal = 0

            s = self.board.sum_col(i, False)  # negative count
            if s < self.board.col_limit_n[i]:
                is_goal = 0

        return is_goal

    def get_MRV(self):
        
        return

    def play(self, x: int, y: int):

        check = self.check_goal()
        if check == 1:
            return True

        selected_magnet = self.board.get_magnet_pos(x, y)
        domain = selected_magnet.get_domain()

        for d in domain:
            if d != 0:
                magnet = self.board.place_magnet(d[0], d[1], d[2])

                if magnet is not None:
                    limitation_col = self.check_limitation_col()
                    limitation_row = self.check_limitation_row()

                    if limitation_col and limitation_row:
                        next_magnet = self.board.get_next_magnet(x, y)

                        if next_magnet is not None:
                            position = next_magnet.get_position()
                            self.print()
                            if self.play(position[0], position[1]):
                                return True

            elif d == 0:
                self.x += 1
                self.board.put_empty(x, y)

                limitation_col = self.check_limitation_col()
                limitation_row = self.check_limitation_row()

                if limitation_col and limitation_row:
                    next_magnet = self.board.get_next_magnet(x, y)

                    if next_magnet is not None:
                        position = next_magnet.get_position()
                        self.print()
                        if self.play(position[0], position[1]):
                            return True

                self.board.remove_empty(x, y)

            check = self.check_goal()
            if check == 1:
                return True

            self.board.remove_magnet(x, y)
            magnet = None

        return False

    def print(self):
        print("-------------------------")

        with open('result.txt', 'a') as buffer:
            buffer.write(str(self.x) + "\n")
            self.x += 1
            for i in range(self.board.row):
                for j in range(self.board.col):
                    magnet = self.board.get_magnet_pos(i , j)

                    value = self.board.table[i][j]
                    if value == 1:
                        print('+', '', end='')
                    if value == -1:
                        print('-', '', end='')
                    if value == 0 and not magnet.isEmpty:
                        print('0', '', end='')
                    if value == 0 and magnet.isEmpty:
                        print('\u2610', '', end='')

                    buffer.write(str(j) + ' ')
                buffer.write("\n")
                print()
            buffer.write("------------------\n")
