#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unittest of Evaluator
"""


import unittest
from copy import deepcopy
from evaluator import *
from random_choice import *

class EvaluatorTest(unittest.TestCase):
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

    def test_one_evaluation_1(self):
        board = deepcopy(self.board)
        board[3][1] = 1
        e = Evaluator(board, random_player, random_player, (3, 1), True, 
            set([(2, 1), (3, 2)]))
        self.assertEqual(e.simulate_one_time(), 1)

    def test_evaluation_1(self):
        board = deepcopy(self.board)
        board[3][1] = 1
        e = Evaluator(board, random_player, random_player, (3, 1), True, 
            set([(2, 1), (3, 2)]))
        self.assertEqual(e.simulate(10), 10)

    def test_one_evaluation_None(self):
        board = deepcopy(self.board)
        board[3][1] = 1
        e = Evaluator(board, random_player, random_player, None, True, 
            set([(2, 1), (3, 2)]))
        self.assertEqual(e.simulate_one_time(), 1)

    def test_evaluation_None(self):
        board = deepcopy(self.board)
        board[3][1] = 1
        e = Evaluator(board, random_player, random_player, None, True, 
            set([(2, 1), (3, 2)]))
        self.assertEqual(e.simulate(10), 10)
    
    def test_one_evaluation_minus1(self):
        board = deepcopy(self.board)
        board[3][1] = 1
        e = Evaluator(board, random_player, random_player, (3, 1), False, 
            set([(2, 1), (3, 2)]))
        self.assertEqual(e.simulate_one_time(), -1)

    def test_evaluation_minus1(self):
        board = deepcopy(self.board)
        board[3][1] = 1
        e = Evaluator(board, random_player, random_player, (3, 1), False, 
            set([(2, 1), (3, 2)]))
        self.assertEqual(e.simulate(10), -10)

    def test_one_evaluation_3positions_1(self):
        board = deepcopy(self.board)
        board[3][1] = 1
        e = Evaluator(board, random_player, random_player, (3, 1), True, 
            set([(2, 1), (3, 2)]))
        self.assertEqual(e.simulate_one_time(), 1)

    def test_evaluation_3positions_1(self):
        board = deepcopy(self.board)
        board[3][1] = 1
        e = Evaluator(board, random_player, random_player, (3, 1), True, 
            set([(2, 1), (3, 2)]))
        self.assertEqual(e.simulate(10), 10)

    def test_one_evaluation_no_moves_and_tie(self):
        board = deepcopy(self.big_board)
        empty = set([(2, 1), (4, 3)])
        e = Evaluator(board, random_player, random_player, (1, 0), True, empty)
        self.assertEqual(e.simulate_one_time(), 0)

    def test_evaluation_no_moves_and_tie(self):
        board = deepcopy(self.big_board)
        empty = set([(2, 1), (4, 3)])
        e = Evaluator(board, random_player, random_player, (1, 0), True, empty)
        self.assertEqual(e.simulate(10), 0)

    def test_random_choice_evaluation_no_moves_and_tie2(self):
        board = deepcopy(self.big_board)
        empty = set([(2, 1), (4, 3)])
        e = Evaluator(board, random_player, random_player, (1, 0), False, empty)
        self.assertEqual(e.simulate_one_time(), 0)

    def test_evaluation_no_moves_and_tie2(self):
        board = deepcopy(self.big_board)
        empty = set([(2, 1), (4, 3)])
        e = Evaluator(board, random_player, random_player, (1, 0), False, empty)
        self.assertEqual(e.simulate(10), 0)


if __name__ == "__main__":
    unittest.main()

