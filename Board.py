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
        return self.magnets[self.board[x][y]]

    def put_magnet(self, x1: int, y1: int, positive=True):
        m = self.get_magnet_pos(x1, y1)
        r = 1
        if m.position2 == [x1, y1]:
            r = 2
        if not positive:
            r = 3 - r
        m.put(r)

    def remove_magnet(self, x: int, y: int):
        self.get_magnet_pos(x, y).remove()
