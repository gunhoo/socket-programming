#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import time

ROW = 10
COL = 10

def print_board(b):

    print("   ", end="")
    for j in range(0, COL):
        print("%2d" % j, end="")

    print()
    print("  ", end="")
    for j in range(0, 2*COL+3):
        print("-", end="")
    
    print()
    for i in range(0, ROW):
        print("%d |" % i, end="")
        for j in range(0, COL):
            c = b[i][j]
            if c == 0:
                print(" +", end="")
            elif c == 1:
                print(" 0", end="")
            elif c == 2:
                print(" @", end="")
            else:
                print("ERROR", end="")
        print(" |")

    print("  ", end="")
    for j in range(0, 2*COL+3):
        print("-", end="")
    
    print()

def check_win(b, x, y):
    last_stone = b[x][y]
    start_x, start_y, end_x, end_y = x, y, x, y

    # check x
    while (start_x - 1 >= 0 and
            b[start_x - 1][y]  == last_stone):
        start_x -= 1
    while (end_x + 1 < ROW and
            b[(end_x + 1)][y] == last_stone):
        end_x += 1
    if end_x - start_x + 1 >= 5:
        return last_stone

    # check y
    start_x, start_y, end_x, end_y = x, y, x, y
    while (start_y - 1 >= 0 and
            b[x][start_y - 1] == last_stone):
        start_y -= 1
    while (end_y + 1 < COL and
            b[x][end_y + 1] == last_stone):
        end_y += 1
    if end_y - start_y + 1 >= 5:
        return last_stone
    
    # check diag 1
    start_x, start_y, end_x, end_y = x, y, x, y
    while (start_x - 1 >= 0 and start_y - 1 >= 0 and
            b[start_x - 1][start_y - 1] == last_stone):
        start_x -= 1
        start_y -= 1
    while (end_x + 1 < ROW and end_y + 1 < COL and
            b[end_x + 1][end_y + 1] == last_stone):
        end_x += 1
        end_y += 1
    if end_y - start_y + 1 >= 5:
        return last_stone
    
    # check diag 2
    start_x, start_y, end_x, end_y = x, y, x, y
    while (start_x - 1 >= 0 and end_y + 1 < COL and
            b[start_x - 1][end_y + 1] == last_stone):
        start_x -= 1
        end_y += 1
    while (end_x + 1 < ROW and start_y - 1 >= 0 and
            b[end_x + 1][start_y - 1] == last_stone):
        end_x += 1
        start_y -= 1
    if end_y - start_y + 1 >= 5:
        return last_stone
    
    return 0

def main():
    board = [[0 for row in range(ROW)] for col in range(COL)]
    x, y, turn, count, win = None, None, 0, 0, 0

    os.system('clear')
    print_board(board)

    while True:
        x, y = [int(x) for x in input("please enter \"x y\" coordinate >> ").split()]

        if x < 0 or y < 0 or x >= ROW or y >= COL:
            print("error, out of bound!")
            time.sleep(2)
            continue
        elif board[x][y] != 0:
            print("error, already used!")
            time.sleep(2)
            continue
        if turn == 0:
            board[x][y] = 1
        else:
            board[x][y] = 2

        # os.system("clear")
        print_board(board)

        win = check_win(board, x, y)
        if win != 0:
            print("player %d wins!" % win)
            break
        
        count += 1
        if count == ROW*COL:
            break
        
        turn = (turn + 1) % 2
    
    return 0

if __name__ == "__main__":
    main()
