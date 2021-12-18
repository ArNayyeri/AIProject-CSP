from Board import Board


class CSP:
    def __init__(self, board: Board):
        self.board = board
        self.table = [[0 for i in range(board.col)] for j in range(board.row)]

    def place_magnet(self, x: int, y: int, isPositive: bool):
        magnet = self.board.get_magnet_pos(x, y)

        positive_pos = 0

        if magnet.position[1] == [x, y]:
            positive_pos = 1
        if not isPositive:
            positive_pos = 1 - positive_pos

        magnet.put(positive_pos)

        x1, y1 = magnet.get_positive_pos()
        self.table[x1][y1] = 1

        x1, y1 = magnet.get_negative_pos()
        self.table[x1][y1] = -1

        return magnet

    def remove_magnet(self, x: int, y: int):
        magnet = self.board.get_magnet_pos(x, y)

        x1, y1 = magnet.get_positive_pos()
        self.table[x1][y1] = 0

        x1, y1 = magnet.get_negative_pos()
        self.table[x1][y1] = 0

        magnet.remove()

    def sum_row(self, index: int, isPositive: bool):
        s = 0
        for i in self.table[index]:
            if (i == 1 and isPositive) or (i == -1 and not isPositive):
                s += 1
        return s

    def sum_col(self, index: int, isPositive: bool):
        s = 0
        for e in range(self.board.row):
            i = self.table[e][index]
            if (i == 1 and isPositive) or (i == -1 and not isPositive):
                s += 1
        return s

    def check_goal(self):
        isGoal = 1
        for i in range(self.board.row):
            s = self.sum_row(i, True)
            if s > self.board.row_limit_p[i]:
                return -1
            elif s < self.board.row_limit_p[i]:
                isGoal = 0

            s = self.sum_row(i, False)
            if s > self.board.row_limit_n[i]:
                return -1
            elif s < self.board.row_limit_n[i]:
                isGoal = 0

        for i in range(self.board.col):
            s = self.sum_col(i, True)
            if s > self.board.col_limit_p[i]:
                return -1
            elif s < self.board.col_limit_p[i]:
                isGoal = 0

            s = self.sum_col(i, False)
            if s > self.board.col_limit_n[i]:
                return -1
            elif s < self.board.col_limit_n[i]:
                isGoal = 0

        return isGoal

    def play(self, x: int, y: int):
        self.print()
        check = self.check_goal()

        if check == 1:
            return True

        magnet = self.place_magnet(x, y, True)
        check = self.check_goal()

        if check == 1:
            return True

        if check == 0:
            if magnet.position[0] != [x, y + 1] and magnet.position[1] != [x, y + 1] and y + 1 < self.board.col:
                if self.play(x, y + 1):
                    return True
            if magnet.position[0] != [x + 1, y] and magnet.position[1] != [x + 1, y] and x + 1 < self.board.row:
                if self.play(x + 1, y):
                    return True

        self.remove_magnet(x, y)

        magnet = self.place_magnet(x, y, False)
        check = self.check_goal()

        if check == 1:
            return True

        if check == 0:
            if magnet.position[0] != [x, y + 1] and magnet.position[1] != [x, y + 1] and y + 1 < self.board.col:
                if self.play(x, y + 1):
                    return True
            if magnet.position[0] != [x + 1, y] and magnet.position[1] != [x + 1, y] and x + 1 < self.board.row:
                if self.play(x + 1, y):
                    return True

        self.remove_magnet(x, y)

        if y + 1 < self.board.col:
            if self.play(x, y + 1):
                return True
        if x + 1 < self.board.row:
            if self.play(x + 1, y):
                return True

        return False

    def print(self):
        with open('result.txt', 'a') as buffer:
            for i in self.table:
                for j in i:
                    buffer.write(str(j) + ' ')
                buffer.write("\n")
            buffer.write("------------------\n")
