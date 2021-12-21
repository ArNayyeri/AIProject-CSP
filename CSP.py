from Board import Board
from Magnet import Magnet


class CSP:
    def __init__(self, board: Board):
        self.board = board
        self.x = 1

    def checklimitation_row(self) :
        for i in range(self.board.row):
            s = self.board.sum_row(i, True)   # positive count
            if s > self.board.row_limit_p[i]:
                return False

            s = self.board.sum_row(i, False)  # negative count
            if s > self.board.row_limit_n[i]:
                return False

        return True
    
    def checklimitation_col(self) :
        for i in range(self.board.col):
            s = self.board.sum_col(i, True)   # positive count
            if s > self.board.col_limit_p[i]:
                return False

            s = self.board.sum_col(i, False)  # negative count
            if s > self.board.col_limit_n[i]:
                return False

        return True

    def check_goal(self):
        isGoal = 1
        for i in range(self.board.row):
            s = self.board.sum_row(i, True)   # positive count
            if s < self.board.row_limit_p[i]:
                isGoal = 0

            s = self.board.sum_row(i, False)  # negative count
            if s < self.board.row_limit_n[i]:
                isGoal = 0

        for i in range(self.board.col):
            s = self.board.sum_col(i, True)   # positive count
            if s < self.board.col_limit_p[i]:
                isGoal = 0

            s = self.board.sum_col(i, False)  # negative count
            if s < self.board.col_limit_n[i]:
                isGoal = 0

        return isGoal

    def get_domain(self , x: int, y: int ) :
        return [1 , -1 , 0]

    def play(self, x: int, y: int):
        domain = self.get_domain(x , y)

        check = self.check_goal()
        if check == 1:
            self.print()
            return True

        for d in domain:
            if(d != 0):
                polarity = True
                if d == -1:
                    polarity = False
                
                magnet = self.board.place_magnet(x, y, polarity)

                if(magnet != None):
                    self.print()

                    limitation_col = self.checklimitation_col()
                    limitation_row = self.checklimitation_row()

                    if(limitation_col and limitation_row):
                        next_magnet = self.board.get_next_magnet(x, y)

                        if(next_magnet != None):
                            position = next_magnet.get_postition()
                            if(self.play(position[0] , position[1])):
                                return True

            elif d == 0:
                next_magnet = self.board.get_next_magnet(x, y)
                if(next_magnet != None):
                    position = next_magnet.get_postition()
                    if(self.play(position[0] , position[1])):
                        return True

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
            for i in self.board.table:
                for j in i:
                    if j == 1:
                        print('+' , '' , end='')
                    if j == -1:
                        print('-' , '' , end='')
                    if j == 0 :
                        print('0' , '' , end='')

                    buffer.write(str(j) + ' ')
                buffer.write("\n")
                print()
            buffer.write("------------------\n")
