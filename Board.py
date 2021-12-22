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

    def get_magnet_pos(self, x: int, y: int) -> Magnet:
        if(x < 0 or y < 0 or x >= self.col or y >= self.row):
            return None
        else :
            return self.magnets[self.magnetpos[x][y] - 1]

    def get_next_magnet(self, x, y) -> Magnet:
        magnetId = self.magnetpos[x][y] - 1

        return (
            self.magnets[magnetId + 1]

            if (magnetId + 1 < len(self.magnets))
            else None
        )

    def update_domain(self , board):
        return

    def get_neighbour_magnets(self , magnet : Magnet) -> List[Magnet] :
        magnets = []

        pos1 = magnet.position[0]
        magnets.append(self.get_magnet_pos(pos1[0] + 1 , pos1[1]))
        magnets.append(self.get_magnet_pos(pos1[0] - 1 , pos1[1]))
        magnets.append(self.get_magnet_pos(pos1[0] , pos1[1] + 1))
        magnets.append(self.get_magnet_pos(pos1[0] , pos1[1] - 1))

        pos2 = magnet.position[1]
        magnets.append(self.get_magnet_pos(pos2[0] + 1 , pos2[1]))
        magnets.append(self.get_magnet_pos(pos2[0] - 1 , pos2[1]))
        magnets.append(self.get_magnet_pos(pos2[0] , pos2[1] + 1))
        magnets.append(self.get_magnet_pos(pos2[0] , pos2[1] - 1))
        
        magnets = list(dict.fromkeys(magnets))
        magnets.remove(magnet)
        magnets = list(filter(None, magnets))

        return magnets

    def check_neighbour(self, magnet: Magnet):

        # Positive Check
        xp, yp = magnet.get_positive_pos()

        if xp - 1 >= 0:
            if self.table[xp - 1][yp] == 1:
                return False

        if yp - 1 >= 0:
            if self.table[xp][yp - 1] == 1:
                return False

        if xp + 1 < self.row:
            if self.table[xp + 1][yp] == 1:
                return False

        if yp + 1 < self.col:
            if self.table[xp][yp + 1] == 1:
                return False

        # Negative Check

        xn, yn = magnet.get_negative_pos()

        if xn - 1 >= 0:
            if self.table[xn - 1][yn] == -1:
                return False

        if yn - 1 >= 0:
            if self.table[xn][yn - 1] == -1:
                return False

        if xn + 1 < self.row:
            if self.table[xn + 1][yn] == -1:
                return False

        if yn + 1 < self.col:
            if self.table[xn][yn + 1] == -1:
                return False

        return True

    def place_magnet(self, x: int, y: int, isPositive: bool):
        magnet = self.get_magnet_pos(x, y)

        magnet.put(x, y, isPositive)

        if not self.check_neighbour(magnet):
            self.remove_magnet(x, y, is_sum=True)
            return None

        xp, yp = magnet.get_positive_pos()
        xn, yn = magnet.get_negative_pos()

        self.table[xp][yp] = 1
        self.table[xn][yn] = -1

        self.row_p[xp] += 1
        self.row_n[xn] += 1
        self.col_p[yp] += 1
        self.col_n[yn] += 1

        self.row_all[xp] += 1
        self.col_all[yp] += 1
        self.row_all[xn] += 1
        self.col_all[yn] += 1

        return magnet

    def remove_magnet(self, x: int, y: int, is_sum: bool = False):
        magnet = self.get_magnet_pos(x, y)

        if magnet.isExist:
            x1, y1 = magnet.get_positive_pos()
            self.table[x1][y1] = 0

            if not is_sum:
                self.row_p[x1] -= 1
                self.col_p[y1] -= 1
                self.row_all[x1] -= 1
                self.col_all[y1] -= 1

            x1, y1 = magnet.get_negative_pos()
            self.table[x1][y1] = 0

            if not is_sum:
                self.row_n[x1] -= 1
                self.col_n[y1] -= 1
                self.row_all[x1] -= 1
                self.col_all[y1] -= 1

            magnet.remove()

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

    def put_empty(self, x, y):
        magnet = self.get_magnet_pos(x, y)
        self.row_all[magnet.position[0][0]] += 1
        self.row_all[magnet.position[1][0]] += 1
        self.col_all[magnet.position[0][1]] += 1
        self.col_all[magnet.position[1][1]] += 1

    def remove_empty(self, x, y):
        magnet = self.get_magnet_pos(x, y)
        self.row_all[magnet.position[0][0]] -= 1
        self.row_all[magnet.position[1][0]] -= 1
        self.col_all[magnet.position[0][1]] -= 1
        self.col_all[magnet.position[1][1]] -= 1
