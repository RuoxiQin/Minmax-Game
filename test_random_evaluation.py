#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unittest of random_evaluation
"""


import unittest
from copy import deepcopy
from random_evaluation import *
from random_choice import get_empty_positions

class RandomEvaluationTest(unittest.TestCase):
    def setUp(self):
        self.board = \
            [[-1, -1, -1, -1, -1],
            [1, 3, -1, -1, -1],
            [3, 0, 2, -1, -1],
            [1, 0, 0, 3, -1],
            [-1, 1, 2, 1, -1]]
        self.big_board = \
            [[-1, -1, -1, -1, -1, -1],
            [1, 3, -1, -1, -1, -1],
            [3, 0, 2, -1, -1, -1],
            [1, 2, 3, 3, -1, -1],
            [3, 1, 2, 0, 2, -1],
            [-1, 1, 2, 1, 2, -1]]


    def test_evaluation_1(self):
        board = deepcopy(self.board)
        board[3][1] = 1
        empty = get_empty_positions(board)
        self.assertEqual(random_evaluation(board, (3, 1), True, empty, 10), 10)

    def test_evaluation_0(self):
        board = deepcopy(self.board)
        board[3][1] = 1
        empty = get_empty_positions(board)
        self.assertEqual(random_evaluation(board, (3, 1), False, empty, 10), \
        -10)

    def test_evaluation_None(self):
        board = deepcopy(self.board)
        board[3][1] = 1
        empty = get_empty_positions(board)
        self.assertEqual(random_evaluation(board, None, True, empty, 10), 10)

    def test_evaluation_None0(self):
        board = deepcopy(self.board)
        board[3][1] = 1
        empty = get_empty_positions(board)
        self.assertEqual(random_evaluation(board, None, False, empty, 10), -10)

    def test_evaluation_no_moves_and_tie(self):
        board = deepcopy(self.big_board)
        empty = set([(2, 1), (4, 3)])
        self.assertEqual(random_evaluation(board, (1, 0), True, empty, 10), 0)

    def test_evaluation_no_moves_and_tie0(self):
        board = deepcopy(self.big_board)
        empty = set([(2, 1), (4, 3)])
        self.assertEqual(random_evaluation(board, (1, 0), False, empty, 10), 0)


if __name__ == "__main__":
    unittest.main()

