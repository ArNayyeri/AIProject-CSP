from Board import Board
from Magnet import Magnet
import ast


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

    def LCV(self, magnet: Magnet):
        domain = magnet.get_domain()
        l = {}
        for i in domain:
            if i != 0:
                l[str(i)] = 0
                self.board.place_magnet(i[0], i[1], i[2])
                for j in self.board.get_neighbour_magnets(magnet):
                    l[str(i)] += len(j.get_domain())
                self.board.remove_magnet(i[0], i[1])
        l = dict(sorted(l.items(), key=lambda item: item[1], reverse=True))
        return l.keys()

    def MRV(self):
        magnet_score = {}

        magnets = list(filter(lambda x: not x.isExist and not x.isEmpty, self.board.magnets))

        for magnet in magnets:
            magnet_score[magnet] = len(magnet.get_domain())

        if magnet_score == {}:
            return None

        max_key = min(magnet_score, key=magnet_score.get)
        max_value = magnet_score[max_key]
        return max_key

    def play(self):
        self.AC3()
        selected_magnet = self.MRV()
        if selected_magnet is None:

            check = self.check_goal()
            if check == 1:
                return True

            return False

        x, y = selected_magnet.get_position()
        domain = self.LCV(selected_magnet)

        for i in domain:
            d = ast.literal_eval(i)
            self.board.place_magnet(d[0], d[1], d[2])

            limitation_col = self.check_limitation_col()
            limitation_row = self.check_limitation_row()

            if limitation_col and limitation_row:
                self.print(selected_magnet)
                if self.play():
                    return True
            self.board.remove_magnet(x, y)

        if selected_magnet.get_domain().__contains__(0):
            self.board.put_empty(x, y)

            limitation_col = self.check_limitation_col()
            limitation_row = self.check_limitation_row()

            if limitation_col and limitation_row:
                self.print(selected_magnet)
                if self.play():
                    return True

            self.board.remove_empty(x, y)

        return False

    def print(self, _magnet: Magnet):
        print("-------------------------")

        with open('result.txt', 'a') as buffer:
            buffer.write(str(self.x) + "\n")
            self.x += 1

            print('+  ', self.board.col_limit_p)
            print('  -', self.board.col_limit_n)
            for i in range(self.board.row):
                print(self.board.row_limit_p[i], self.board.row_limit_n[i], sep=',', end=' ')

                for j in range(self.board.col):
                    magnet = self.board.get_magnet_pos(j, i)

                    boldchar = '\033[0m'
                    if magnet == _magnet:
                        boldchar = '\x1b[6;30;42m'

                    value = self.board.table[i][j]
                    if value == 1:
                        print(boldchar, '+', '\033[0m', end='')
                    if value == -1:
                        print(boldchar, '-', '\033[0m', end='')
                    if value == 0 and not magnet.isEmpty:
                        print(boldchar, '0', '\033[0m', end='')
                    if value == 0 and magnet.isEmpty:
                        print(boldchar, '\u2610', '\033[0m', end='')

                    buffer.write(str(j) + ' ')

                print(' |', self.board.row_p[i], ' ', self.board.row_n[i], sep='', end=' ')

                buffer.write("\n")
                print()

            seperator = ''
            for i in range(self.board.col * 3):
                seperator += '_'

            print('   ', seperator)
            print('   ', self.board.col_p, ' +  ')
            print('   ', self.board.col_n, '   -')

            buffer.write("------------------\n")

    def AC3(self):
        contradiction = False
        Q = list(filter(lambda x: not x.isExist and not x.isEmpty, self.board.magnets))
        while len(Q) > 0 and not contradiction:
            magnet = Q.pop(0)
            for i in list(filter(lambda x: not x.isExist and not x.isEmpty, self.board.get_neighbour_magnets(magnet))):
                if self.remove_values(magnet, i):
                    if len(i.domain) == 0:
                        contradiction = True
                    Q.append(i)

    def remove_values(self, x: Magnet, y: Magnet):
        removed = False
        for i in y.get_domain():
            if i == 0:
                self.board.put_empty(y.position[0][0], y.position[0][1])
                if len(x.get_domain()) == 0:
                    self.board.remove_empty(y.position[0][0], y.position[0][1])
                    y.get_domain().remove(i)
                    removed = True
                else:
                    self.board.remove_empty(y.position[0][0], y.position[0][1])

            elif not i[2]:
                self.board.place_magnet(y.position[0][0], y.position[0][1], False)
                if len(x.get_domain()) == 0:
                    self.board.remove_magnet(y.position[0][0], y.position[0][1])
                    y.get_domain().remove(i)
                    removed = True
                else:
                    self.board.remove_magnet(y.position[0][0], y.position[0][1])

            else:
                self.board.place_magnet(y.position[0][0], y.position[0][1], True)
                if len(x.get_domain()) == 0:
                    self.board.remove_magnet(y.position[0][0], y.position[0][1])
                    y.get_domain().remove(i)
                    removed = True
                else:
                    self.board.remove_magnet(y.position[0][0], y.position[0][1])

        return removed
