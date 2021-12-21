from Board import Board
from Magnet import Magnet


class CSP:
    def __init__(self, board: Board):
        self.board = board
        self.table = [[0 for i in range(board.col)] for j in range(board.row)]
        self.x = 1

    def checkNeighbour(self , magnet : Magnet):
            
        #Positive Check

        xp , yp = magnet.get_positive_pos()

        if(xp - 1 >= 0):
            temp = self.board.get_magnet_pos(xp - 1, yp)
            if(temp != magnet and temp.isExist and temp.get_positive_pos() == [xp - 1 , yp]):
                return False

        if(yp - 1 >= 0):
            temp = self.board.get_magnet_pos(xp, yp - 1)
            if(temp != magnet and temp.isExist and temp.get_positive_pos() == [xp , yp - 1]):
                return False

        if(xp + 1 < self.board.col):
            temp = self.board.get_magnet_pos(xp + 1, yp)
            if(temp != magnet and temp.isExist and temp.get_positive_pos() == [xp + 1, yp]):
                return False

        if(yp + 1 < self.board.row):
            temp = self.board.get_magnet_pos(xp , yp + 1)
            if(temp != magnet and temp.isExist and temp.get_positive_pos() == [xp , yp + 1]):
                return False

        # Negative Check

        xn , yn = magnet.get_negative_pos()

        if(xn - 1 >= 0):
            temp = self.board.get_magnet_pos(xn - 1, yn)
            if(temp != magnet and temp.isExist and temp.get_negative_pos() == [xn - 1, yn]):
                return False

        if(yn - 1 >= 0):
            temp = self.board.get_magnet_pos(xn, yn - 1)
            if(temp != magnet and temp.isExist and temp.get_negative_pos() == [xn, yn - 1]):
                return False

        if(xn + 1 < self.board.col):
            temp = self.board.get_magnet_pos(xn + 1, yn)
            if(temp != magnet and temp.isExist and temp.get_negative_pos() == [xn + 1, yn]):
                return False

        if(yn + 1 < self.board.row):
            temp = self.board.get_magnet_pos(xn , yn + 1)
            if(temp != magnet and temp.isExist and temp.get_negative_pos() == [xn , yn + 1]):
                return False

        return True

    def place_magnet(self, x: int, y: int, isPositive: bool):
        magnet = self.board.get_magnet_pos(x, y)

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

    def checklimitation(self) :
        for i in range(self.board.row):
            s = self.sum_row(i, True)   # positive count
            if s > self.board.row_limit_p[i]:
                return False

            s = self.sum_row(i, False)  # negative count
            if s > self.board.row_limit_n[i]:
                return False

        for i in range(self.board.col):
            s = self.sum_col(i, True)   # positive count
            if s > self.board.col_limit_p[i]:
                return False

            s = self.sum_col(i, False)  # negative count
            if s > self.board.col_limit_n[i]:
                return False

        return True

    def check_goal(self):
        isGoal = 1
        for i in range(self.board.row):
            s = self.sum_row(i, True)   # positive count
            if s < self.board.row_limit_p[i]:
                isGoal = 0

            s = self.sum_row(i, False)  # negative count
            if s < self.board.row_limit_n[i]:
                isGoal = 0

        for i in range(self.board.col):
            s = self.sum_col(i, True)   # positive count
            if s < self.board.col_limit_p[i]:
                isGoal = 0

            s = self.sum_col(i, False)  # negative count
            if s < self.board.col_limit_n[i]:
                isGoal = 0

        return isGoal

    def play(self, x: int, y: int):
        
        check = self.check_goal()

        if check == 1:
            return True

        magnet = self.place_magnet(x, y, True)
        if(magnet == None):
            magnet = self.place_magnet(x, y, False)
        
        if(magnet != None):
            self.print()

        limitation = self.checklimitation()

        if(not limitation):
            self.remove_magnet(x, y)
        
        next_magnet = self.board.get_next_magnet(x, y)

        if(next_magnet != None):
            position = next_magnet.get_postition()
            self.play(position[0] , position[1])

        check = self.check_goal()

        if check == 1:
            return True
        elif magnet != None and magnet.isExist:
            self.remove_magnet(x , y)

        return False

    def print(self):
        print("-------------------------")

        with open('result.txt', 'a') as buffer:
            buffer.write(str(self.x) + "\n")
            self.x += 1
            for i in self.table:
                for j in i:
                    if j == 1:
                        print('+' , '' , end='')
                    if j == -1:
                        print('-' , '' , end='')
                    else :
                        print('0' , '' , end='')

                    buffer.write(str(j) + ' ')
                buffer.write("\n")
                print()
            buffer.write("------------------\n")
