from Board import Board
from CSP import CSP
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
    for i in range(row):
        for j in range(col):
            if i + 1 != row:
                if mat[i][j] == mat[i + 1][j]:
                    m.append(Magnet(i, j, i + 1, j))
            if j + 1 != col:
                if mat[i][j] == mat[i][j + 1]:
                    m.append(Magnet(i, j, i, j + 1))

    board = Board(row, col, row_limit_p, col_limit_p, row_limit_n, col_limit_n, mat, m)

    open('result.txt', 'w').close()
            
    csp = CSP(board)
    csp.play(0, 0)

