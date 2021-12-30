from Board import Board
from CSP import CSP
from Magnet import Magnet
import time

if __name__ == '__main__':

    data = open('input1.txt', 'r').readlines()

    mat = []
    m = []

    if data is not None:
        row, col = list(map(int, data[0].split(' ')))
        row_limit_p = list(map(int, data[1].split(' ')))
        row_limit_n = list(map(int, data[2].split(' ')))
        col_limit_p = list(map(int, data[3].split(' ')))
        col_limit_n = list(map(int, data[4].split(' ')))

        for i in range(row):
            mat.append(list(map(int, data[5 + i].split(' '))))

    else:
        row, col = list(map(int, input().split(' ')))
        row_limit_p = list(map(int, input().split(' ')))
        row_limit_n = list(map(int, input().split(' ')))
        col_limit_p = list(map(int, input().split(' ')))
        col_limit_n = list(map(int, input().split(' ')))

        for i in range(row):
            mat.append(list(map(int, input().split(' '))))

    for i in range(row):
        for j in range(col):
            if i + 1 != row:
                if mat[i][j] == mat[i + 1][j]:
                    m.append(Magnet(j, i, j, i + 1))
            if j + 1 != col:
                if mat[i][j] == mat[i][j + 1]:
                    m.append(Magnet(j, i, j + 1, i))

    board = Board(row, col, row_limit_p, col_limit_p, row_limit_n, col_limit_n, mat, m)

    open('result.txt', 'w').close()

    start = time.time()

    csp = CSP(board)
    csp.play()

    csp.print(None)

    end = time.time()

    print("\nElapsed Time ", round(end - start, 2), " s with ", csp.x, " moves", sep='', end='')
