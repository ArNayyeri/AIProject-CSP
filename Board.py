from typing import List
from Magnet import Magnet

class Board:
    def __init__(self, row: int, col: int, row_limit_p, col_limit_p, row_limit_n, col_limit_n, board , magnets : List[Magnet]):
        self.row = row
        self.col = col
        self.magnetpos = board

        self.table = [[0 for i in range(col)] for j in range(row)]

        self.row_limit_p = row_limit_p
        self.col_limit_p = col_limit_p
        
        self.row_limit_n = row_limit_n
        self.col_limit_n = col_limit_n

        self.magnets = magnets

    def get_magnet_pos(self, x: int, y: int) -> Magnet:
        return self.magnets[self.magnetpos[x][y] - 1]

    def get_next_magnet(self, x, y) -> Magnet :
        magnetId = self.magnetpos[x][y] - 1

        return (
            self.magnets[magnetId + 1]
            
            if(magnetId + 1 < len(self.magnets))
            else None
        )

    def checkNeighbour(self , magnet : Magnet):
            
        #Positive Check

        xp , yp = magnet.get_positive_pos()

        if(xp - 1 >= 0):
            temp = self.get_magnet_pos(xp - 1, yp)
            if(temp != magnet and temp.isExist and temp.get_positive_pos() == [xp - 1 , yp]):
                return False

        if(yp - 1 >= 0):
            temp = self.get_magnet_pos(xp, yp - 1)
            if(temp != magnet and temp.isExist and temp.get_positive_pos() == [xp , yp - 1]):
                return False

        if(xp + 1 < self.col):
            temp = self.get_magnet_pos(xp + 1, yp)
            if(temp != magnet and temp.isExist and temp.get_positive_pos() == [xp + 1, yp]):
                return False

        if(yp + 1 < self.row):
            temp = self.get_magnet_pos(xp , yp + 1)
            if(temp != magnet and temp.isExist and temp.get_positive_pos() == [xp , yp + 1]):
                return False

        # Negative Check

        xn , yn = magnet.get_negative_pos()

        if(xn - 1 >= 0):
            temp = self.get_magnet_pos(xn - 1, yn)
            if(temp != magnet and temp.isExist and temp.get_negative_pos() == [xn - 1, yn]):
                return False

        if(yn - 1 >= 0):
            temp = self.get_magnet_pos(xn, yn - 1)
            if(temp != magnet and temp.isExist and temp.get_negative_pos() == [xn, yn - 1]):
                return False

        if(xn + 1 < self.col):
            temp = self.get_magnet_pos(xn + 1, yn)
            if(temp != magnet and temp.isExist and temp.get_negative_pos() == [xn + 1, yn]):
                return False

        if(yn + 1 < self.row):
            temp = self.get_magnet_pos(xn , yn + 1)
            if(temp != magnet and temp.isExist and temp.get_negative_pos() == [xn , yn + 1]):
                return False

        return True

    def place_magnet(self, x: int, y: int, isPositive: bool):
        magnet = self.get_magnet_pos(x, y)

        magnet.put(x , y , isPositive)

        if not self.checkNeighbour(magnet):
            self.remove_magnet(x , y)
            return None

        xp, yp = magnet.get_positive_pos()
        xn, yn = magnet.get_negative_pos()

        self.table[xp][yp] = 1
        self.table[xn][yn] = -1

        return magnet

    def remove_magnet(self, x: int, y: int):
        magnet = self.get_magnet_pos(x, y)

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
        for e in range(self.row):
            i = self.table[e][index]
            if (i == 1 and isPositive) or (i == -1 and not isPositive):
                s += 1
        return s
