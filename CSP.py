from Board import Board
from Magnet import Magnet


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

    def get_MRV(self) -> Magnet:
        magnet_score = {}
        
        magnets = list(filter(lambda x: not x.isExist and not x.isEmpty , self.board.magnets ))

        for magnet in magnets:
            neighbours = self.board.get_neighbour_magnets(magnet)
            neighbours = list(filter(lambda x: not x.isExist and not x.isEmpty , neighbours ))

            magnet_score[magnet] = len(neighbours)

            magnet_score[magnet] += self.board.col_limit_n[magnet.position[0][1]]
            magnet_score[magnet] += self.board.col_limit_p[magnet.position[0][1]]
            magnet_score[magnet] += self.board.row_limit_n[magnet.position[0][0]]
            magnet_score[magnet] += self.board.row_limit_p[magnet.position[0][0]]

            magnet_score[magnet] += self.board.col_limit_n[magnet.position[1][1]]
            magnet_score[magnet] += self.board.col_limit_p[magnet.position[1][1]]
            magnet_score[magnet] += self.board.row_limit_n[magnet.position[1][0]]
            magnet_score[magnet] += self.board.row_limit_p[magnet.position[1][0]]

        if magnet_score == {}:
            return None

        max_key = max(magnet_score, key=magnet_score.get)
        max_value = magnet_score[max_key]
        return max_key

    def play(self):

        check = self.check_goal()
        if check == 1:
            return True

        selected_magnet = self.get_MRV()
        if selected_magnet is None:
            return False

        x , y = selected_magnet.get_position()
        domain = selected_magnet.get_domain()


        for d in domain:
            if d != 0:
                self.board.place_magnet(d[0], d[1], d[2])

                limitation_col = self.check_limitation_col()
                limitation_row = self.check_limitation_row()

                if limitation_col and limitation_row:
                    self.print(selected_magnet)
                    if self.play():
                        return True


            elif d == 0:
                self.x += 1
                self.board.put_empty(x, y)

                limitation_col = self.check_limitation_col()
                limitation_row = self.check_limitation_row()

                if limitation_col and limitation_row:
                    self.print(selected_magnet)
                    if self.play():
                        return True

                self.board.remove_empty(x, y)

            check = self.check_goal()
            if check == 1:
                return True

            self.board.remove_magnet(x, y)

        return False

    def print(self , _magnet : Magnet ):
        print("-------------------------")

        with open('result.txt', 'a') as buffer:
            buffer.write(str(self.x) + "\n")
            self.x += 1

            print('+  ' , self.board.col_limit_p)
            print('  -' , self.board.col_limit_n)
            for i in range(self.board.row):
                print(self.board.row_limit_p[i] , self.board.row_limit_n[i]  , sep=',' , end=' ')

                for j in range(self.board.col):
                    magnet = self.board.get_magnet_pos(i , j)

                    boldchar = '\033[0m'
                    if magnet == _magnet:
                        boldchar = '\x1b[6;30;42m'
                        
                    value = self.board.table[i][j]
                    if value == 1:
                        print(boldchar , '+', '\033[0m', end='')
                    if value == -1:
                        print(boldchar , '-', '\033[0m', end='')
                    if value == 0 and not magnet.isEmpty:
                        print(boldchar , '0', '\033[0m', end='')
                    if value == 0 and magnet.isEmpty:
                        print(boldchar , '\u2610', '\033[0m', end='')

                    buffer.write(str(j) + ' ')

                print(' |' , self.board.row_p[i] , ' ', self.board.row_n[i]  , sep='' , end=' ')

                buffer.write("\n")
                print()

            print('    '  , self.board.col_limit_p , '+  ')
            print('    '  , self.board.col_limit_n , '  -')

            buffer.write("------------------\n")
