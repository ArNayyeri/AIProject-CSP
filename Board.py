from typing import List
from Magnet import Magnet


class Board:
    def __init__(self, row: int, col: int, row_limit_p, col_limit_p, row_limit_n, col_limit_n, board,
                 magnets: List[Magnet]):
        self.row = row
        self.col = col
        self.magnetpos = board

        self.table = [[0 for i in range(col)] for j in range(row)]

        self.row_limit_p = row_limit_p
        self.col_limit_p = col_limit_p

        self.row_limit_n = row_limit_n
        self.col_limit_n = col_limit_n

        self.magnets = magnets

        self.row_p = [0 for i in range(row)]
        self.row_n = [0 for i in range(row)]
        self.col_p = [0 for i in range(col)]
        self.col_n = [0 for i in range(col)]
        self.row_all = [0 for i in range(row)]
        self.col_all = [0 for i in range(col)]

    def get_magnet_pos(self, x: int, y: int):
        if x < 0 or y < 0 or x >= self.col or y >= self.row:
            return None
        else:
            return self.magnets[self.magnetpos[y][x] - 1]

    def update_domain(self, selected_magnet: Magnet, putmagnet: bool):
        magnets = list(filter(lambda x: not x.isExist, self.get_neighbour_magnets(selected_magnet)))

        if putmagnet:
            for magnet in magnets:
                temp = []

                removeddomains = magnet.check_domain([*selected_magnet.get_positive_pos(), True])
                if len(removeddomains) > 0:
                    for rdomain in removeddomains:
                        temp.append(rdomain)

                removeddomains = magnet.check_domain([*selected_magnet.get_negative_pos(), False])
                if len(removeddomains) > 0:
                    for rdomain in removeddomains:
                        temp.append(rdomain)

                selected_magnet.history[magnet] = temp
        else:
            while len(selected_magnet.history) != 0:
                key, val = selected_magnet.history.popitem()
                if len(val) > 0:
                    for value in val:
                        key.add_to_domain(value)

    def get_neighbour_magnets(self, magnet: Magnet) -> List[Magnet]:
        magnets = []

        pos1 = magnet.position[0]
        magnets.append(self.get_magnet_pos(pos1[0] + 1, pos1[1]))
        magnets.append(self.get_magnet_pos(pos1[0] - 1, pos1[1]))
        magnets.append(self.get_magnet_pos(pos1[0], pos1[1] + 1))
        magnets.append(self.get_magnet_pos(pos1[0], pos1[1] - 1))

        pos2 = magnet.position[1]
        magnets.append(self.get_magnet_pos(pos2[0] + 1, pos2[1]))
        magnets.append(self.get_magnet_pos(pos2[0] - 1, pos2[1]))
        magnets.append(self.get_magnet_pos(pos2[0], pos2[1] + 1))
        magnets.append(self.get_magnet_pos(pos2[0], pos2[1] - 1))

        magnets = list(dict.fromkeys(magnets))
        magnets.remove(magnet)
        magnets = list(filter(None, magnets))

        return magnets

    def place_magnet(self, x: int, y: int, isPositive: bool, empty: bool) -> Magnet:
        magnet = self.get_magnet_pos(x, y)

        if (not empty):
            magnet.put(x, y, isPositive)

            xp, yp = magnet.get_positive_pos()
            xn, yn = magnet.get_negative_pos()

            self.table[yp][xp] = 1
            self.table[yn][xn] = -1

            self.row_p[yp] += 1
            self.row_n[yn] += 1
            self.col_p[xp] += 1
            self.col_n[xn] += 1

            self.update_domain(magnet, True)
        else:
            magnet.isEmpty = True

        self.row_all[magnet.position[0][1]] += 1
        self.row_all[magnet.position[1][1]] += 1
        self.col_all[magnet.position[0][0]] += 1
        self.col_all[magnet.position[1][0]] += 1

        return magnet

    def remove_magnet(self, x: int, y: int, is_sum: bool = False) -> Magnet:
        magnet = self.get_magnet_pos(x, y)

        if magnet.isExist:
            x1, y1 = magnet.get_positive_pos()
            self.table[y1][x1] = 0

            if not is_sum:
                self.row_p[y1] -= 1
                self.col_p[x1] -= 1
                self.row_all[y1] -= 1
                self.col_all[x1] -= 1

            x1, y1 = magnet.get_negative_pos()
            self.table[y1][x1] = 0

            if not is_sum:
                self.row_n[y1] -= 1
                self.col_n[x1] -= 1
                self.row_all[y1] -= 1
                self.col_all[x1] -= 1

            magnet.remove()

            self.update_domain(magnet, False)

        elif magnet.isEmpty:
            magnet.isEmpty = False

            self.row_all[magnet.position[0][1]] -= 1
            self.row_all[magnet.position[1][1]] -= 1
            self.col_all[magnet.position[0][0]] -= 1
            self.col_all[magnet.position[1][0]] -= 1

        return magnet

    def sum_row(self, index: int, isPositive: bool):
        # s = 0
        # for i in self.table[index]:
        #     if (i == 1 and isPositive) or (i == -1 and not isPositive):
        #         s += 1
        # return s
        if isPositive:
            return self.row_p[index]
        else:
            return self.row_n[index]

    def sum_col(self, index: int, isPositive: bool):
        # s = 0
        # for e in range(self.row):
        #     i = self.table[e][index]
        #     if (i == 1 and isPositive) or (i == -1 and not isPositive):
        #         s += 1
        # return s
        if isPositive:
            return self.col_p[index]
        else:
            return self.col_n[index]
