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
            return self.magnets[self.magnetpos[y][x] - 1]

    def get_next_magnet(self, x, y) -> Magnet:
        magnetId = self.magnetpos[y][x] - 1

        return (
            self.magnets[magnetId + 1]

            if (magnetId + 1 < len(self.magnets))
            else None
        )

    def update_domain(self):
        magnets = list(filter(lambda x: not x.isExist , self.magnets))

        for magnet in magnets:

            neighbours = self.get_neighbour_magnets(magnet)
            neighbours = list(filter(lambda x: x.isExist , neighbours))
            
            x1 , y1 = magnet.position[0]
            x2 , y2 = magnet.position[1]

            result = magnet.init_domain.copy()

            for neighbour in neighbours :
                
                n_x1 , n_y1 = neighbour.position[0]
                n_x2 , n_y2 = neighbour.position[1]

                n_xp , n_yp = neighbour.get_positive_pos()
                n_xn , n_yn = neighbour.get_negative_pos()

                result = list(filter(lambda x: x != [n_xp , n_yp + 1 , True], result))
                result = list(filter(lambda x: x != [n_xp , n_yp - 1 , True], result))
                result = list(filter(lambda x: x != [n_xp + 1 , n_yp , True], result))
                result = list(filter(lambda x: x != [n_xp - 1 , n_yp , True], result))

                result = list(filter(lambda x: x != [n_xn , n_yn + 1 , False], result))
                result = list(filter(lambda x: x != [n_xn , n_yn - 1 , False], result))
                result = list(filter(lambda x: x != [n_xn + 1 , n_yn , False], result))
                result = list(filter(lambda x: x != [n_xn - 1 , n_yn , False], result))

                temp_result = result.copy()
                
                for res in result:
                    if res == [x1 , y1 , True] and [x2 , y2] == [n_xn + 1 , n_yn]:
                        temp_result = list(filter(lambda x: x != res, temp_result))
                    if res == [x1 , y1 , True] and [x2 , y2] == [n_xn - 1 , n_yn]:
                        temp_result = list(filter(lambda x: x != res, temp_result))
                    if res == [x1 , y1 , True] and [x2 , y2] == [n_xn , n_yn + 1]:
                        temp_result = list(filter(lambda x: x != res, temp_result))
                    if res == [x1 , y1 , True] and [x2 , y2] == [n_xn , n_yn - 1]:
                        temp_result = list(filter(lambda x: x != res, temp_result))

                    if res == [x1 , y1 , False] and [x2 , y2] == [n_xp + 1 , n_yp]:
                        temp_result = list(filter(lambda x: x != res, temp_result))
                    if res == [x1 , y1 , False] and [x2 , y2] == [n_xp - 1 , n_yp]:
                        temp_result = list(filter(lambda x: x != res, temp_result))
                    if res == [x1 , y1 , False] and [x2 , y2] == [n_xp , n_yp + 1]:
                        temp_result = list(filter(lambda x: x != res, temp_result))
                    if res == [x1 , y1 , False] and [x2 , y2] == [n_xp , n_yp - 1]:
                        temp_result = list(filter(lambda x: x != res, temp_result))

                result = temp_result
            
            magnet.domain = result

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

    def place_magnet(self, x: int, y: int, isPositive: bool) -> Magnet:
        magnet = self.get_magnet_pos(x, y)

        magnet.put(x, y, isPositive)

        xp, yp = magnet.get_positive_pos()
        xn, yn = magnet.get_negative_pos()

        self.table[yp][xp] = 1
        self.table[yn][xn] = -1

        self.row_p[yp] += 1
        self.row_n[yn] += 1
        self.col_p[xp] += 1
        self.col_n[xn] += 1

        self.row_all[yp] += 1
        self.col_all[xp] += 1
        self.row_all[yn] += 1
        self.col_all[xn] += 1

        self.update_domain()

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

            self.update_domain()

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

    def put_empty(self, x, y) -> Magnet:
        magnet = self.get_magnet_pos(x, y)
        magnet.isEmpty = True

        self.row_all[magnet.position[0][1]] += 1
        self.row_all[magnet.position[1][1]] += 1
        self.col_all[magnet.position[0][0]] += 1
        self.col_all[magnet.position[1][0]] += 1

        self.update_domain()

        return magnet

    def remove_empty(self, x, y) -> Magnet:
        magnet = self.get_magnet_pos(x, y)
        magnet.isEmpty = False

        self.row_all[magnet.position[0][1]] -= 1
        self.row_all[magnet.position[1][1]] -= 1
        self.col_all[magnet.position[0][0]] -= 1
        self.col_all[magnet.position[1][0]] -= 1

        self.update_domain()

        return magnet
