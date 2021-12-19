class Board:
    def __init__(self, row: int, col: int, row_limit_p, col_limit_p, row_limit_n, col_limit_n, board, magnets):
        self.row = row
        self.col = col
        self.board = board
        self.row_limit_p = row_limit_p
        self.col_limit_p = col_limit_p
        self.row_limit_n = row_limit_n
        self.col_limit_n = col_limit_n
        self.magnets = magnets

    def get_magnet_pos(self, x: int, y: int):
        return self.magnets[self.board[x][y] - 1]

    def get_next_magnet(self, x, y):
        if self.board[x][y] == len(self.magnets):
            return -1
        return self.magnets[self.board[x][y]].position[0]
