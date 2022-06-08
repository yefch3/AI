#!/usr/bin/env python
# coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
from heapq import *
import numpy as np
import sys
import time

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def trace(solved_board, fill_r, fill_c, fill_a, fill, que):
    # if no need to fill, then succeed
    if len(fill) == 0:
        return True

    key = que.pop()

    row = key[0]
    col = key[1]
    area = (ord(row) - ord('A')) // 3 * 3 + (int(col) - 1) // 3

    # forward, reduce the key item from the unsolved list
    fill_r[row].remove(key)
    fill_c[col].remove(key)
    fill_a[area].remove(key)
    candidates = fill[key]
    fill.pop(key)

    # for each candidate in the possible solution set, choose one to try
    for num in candidates:
        solved_board[key] = num
        check, rm = check_and_reduce(solved_board, fill_r, fill_c, fill_a, fill, key)
        if check == "reduce":
            for grid in rm:
                fill[grid].remove(num)
                que.push(grid, len(fill[grid]))
            res = trace(solved_board, fill_r, fill_c, fill_a, fill, que)
            if res == True:
                return True
            for grid in rm:
                fill[grid].add(num)
                que.push(grid, len(fill[grid]))

    # trace back, add the original element, return False, meaning we fail to fill the number
    fill[key] = candidates
    fill_r[row].add(key)
    fill_c[col].add(key)
    fill_a[area].add(key)

    return False


def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this

    # initialization
    fill_r, fill_c, fill_a, fill = {}, {}, {}, {}
    # unassign_row: 这一行有哪些是空着的，范围是A-I，从ROW里面选，例如：{'A':{'A1', 'A2'}, ...}
    # fill_r = {}
    # # 这一列有哪些是空着的，范围是1-9，从COL里面选，例如：{'1':{'A1', 'B1'}, ...}
    # fill_c = {}
    # # 这一个九宫格是哪些空着的，范围0-9，例如：{0:{'A1', 'A2'}, ...}
    # fill_a = {}
    # # 每个格子可选的数字的数目，范围A1-I9，例如：{'A1':{1, 2, 3}, ...}
    # fill = {}
    solved_board = board
    # 初始化所有的都为空集合

    for row in ROW:
        fill_r[row] = set()
    for col in COL:
        fill_c[col] = set()
    for i in range(9):
        fill_a[i] = set()
    for key in board.keys():
        row = key[0]
        col = key[1]
        area = (ord(row) - ord('A')) // 3 * 3 + (int(col) - 1) // 3
        if board[key] == 0:
            # 如果这是个未知的框，那么就添加到下面各自的约束中去
            fill_r[row].add(key)
            fill_c[col].add(key)
            fill_a[area].add(key)
            fill[key] = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    for key in board.keys():
        if board[key] != 0:
            check, rm = check_and_reduce(board, fill_r, fill_c, fill_a, fill, key)
            for grid in rm:
                fill[grid].remove(board[key])

    que = PQ()

    for key in fill.keys():
        que.push(key, len(fill[key]))


    trace(solved_board, fill_r, fill_c, fill_a, fill, que)

    return solved_board

"""检查是否有已经可以去除的选择"""
def check_and_reduce(solved_board, fill_r, fill_c, fill_a, fill, key):
    row = key[0]
    col = key[1]
    area = (ord(row) - ord('A')) // 3 * 3 + (int(col) - 1) // 3
    rm = set()

    # {'A':{'A1', 'A2'}, ...}
    for grid in fill_r[row]:
        # {'A1':{1, 2, 3}, ...}
        if solved_board[key] in fill[grid]:
            if len(fill[grid]) <= 1:
                return "no reduce", None
            else:
                rm.add(grid)

    # {'1':{'A1', 'B1'}, ...}
    for grid in fill_c[col]:
        if solved_board[key] in fill[grid]:
            if len(fill[grid]) <= 1:
                return "no reduce", None
            else:
                rm.add(grid)

    # {0:{'A1', 'A2'}, ...}
    for grid in fill_a[area]:
        if solved_board[key] in fill[grid]:
            if len(fill[grid]) <= 1:
                return "no reduce", None
            else:
                rm.add(grid)

    return "reduce", rm


class PQ(object):
    def __init__(self):
        self.priorityqueue = []
        self.key_dict = {}

    def push(self, grid, length):
        # if the grid has in key_dict, then pop the original and add the new one, update
        if grid in self.key_dict.keys():
            self.key_dict.pop(grid)[1] = "None"
        key = list([length, grid])
        self.key_dict[grid] = key
        heappush(self.priorityqueue, key)

    def pop(self):
        while len(self.priorityqueue):
            length, grid = heappop(self.priorityqueue)
            if grid != "None":
                self.key_dict.pop(grid)
                return grid

# line = "800000000003600000070090200050007000000045700000100030001000068008500010090000400"
# board = {ROW[r] + COL[c]: int(line[9 * r + c])
#                      for r in range(9) for c in range(9)}
# solved_board = backtracking(board)
# print(print(type(solved_board)))

if __name__ == '__main__':
    # start_time = time.time()
    if len(sys.argv) > 1:

        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = {ROW[r] + COL[c]: int(sys.argv[1][9 * r + c])
                 for r in range(9) for c in range(9)}

        solved_board = backtracking(board)

        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'starter/sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        # Solve each board using backtracking
        # time_list = []
        for line in sudoku_list.split("\n"):
            # start_time = time.time()

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = {ROW[r] + COL[c]: int(line[9 * r + c])
                     for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            # print_board(board)

            # Solve with backtracking
            solved_board = backtracking(board)

            # Print solved board. TODO: Comment this out when timing runs.
            # print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')
            # end_time = time.time()
            # print(end_time - start_time)
            # time_list.append(end_time-start_time)

        print("Finishing all boards in file.")
        # print("min: ", min(time_list))
        # print("max: ", max(time_list))
        # print("sum: ", sum(time_list))
        # print("mean: ", np.mean(time_list))
        # print(sum(time_list) / len(time_list))
        # print("std: ", np.std(time_list))