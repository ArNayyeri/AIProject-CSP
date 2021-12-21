from typing import List
from Magnet import Magnet

class Board:
    def __init__(self, row: int, col: int, row_limit_p, col_limit_p, row_limit_n, col_limit_n, board , magnets : List[Magnet]):
        self.row = row
        self.col = col
        self.board = board
        self.row_limit_p = row_limit_p
        self.col_limit_p = col_limit_p
        
        self.row_limit_n = row_limit_n
        self.col_limit_n = col_limit_n

        self.magnets = magnets

    def get_magnet_pos(self, x: int, y: int) -> Magnet:
        return self.magnets[self.board[x][y] - 1]

    def get_next_magnet(self, x, y) -> Magnet :
        magnetId = self.board[x][y] - 1

        return (
            self.magnets[magnetId + 1]
            
            if(magnetId + 1 < len(self.magnets))
            else None
        )
