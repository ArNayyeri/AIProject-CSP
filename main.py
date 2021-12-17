from Board import Board
from Magnet import Magnet

if __name__ == '__main__':

    row, col = list(map(int, input().split(' ')))
    row_limit_p = list(map(int, input().split(' ')))
    row_limit_n = list(map(int, input().split(' ')))
    col_limit_p = list(map(int, input().split(' ')))
    col_limit_n = list(map(int, input().split(' ')))
    mat = []
    for i in range(row):
        mat.append(list(map(int, input().split(' '))))
    m = []
    for i in range(row - 1):
        for j in range(col - 1):
            if mat[i][j] == mat[i + 1][j]:
                m.append(Magnet(i, j, i + 1, j))
            elif mat[i][j] == mat[i][j + 1]:
                m.append(Magnet(i, j, i, j + 1))

    board = Board(row, col, row_limit_p, col_limit_p, row_limit_n, col_limit_n, mat, m)
