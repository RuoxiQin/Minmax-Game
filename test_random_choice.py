#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unittest of random_choice
"""


import unittest
from copy import deepcopy
from random_choice import *

class RandomChocieTest(unittest.TestCase):
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

    def test_get_neighboor(self):
        correct = [(2, 0), (3, 1), (3, 2), (2, 2), (1, 1), (1, 0)]
        self.assertEqual(correct, get_neighboor((2, 1)))

    def test_get_empty_positions(self):
        correct = set([(2, 1), (3, 1), (3, 2)])
        self.assertEqual(get_empty_positions(self.board), correct)

    def test_get_empty_neighboor(self):
        correct = [(3, 1), (3, 2)]
        self.assertEqual(correct, get_empty_neighboor(self.board, (2, 1)))

    def test_check_loss_true(self):
        self.assertTrue(check_loss(self.board, (2, 1), 2))

    def test_check_loss_true2(self):
        self.assertTrue(check_loss(self.board, (2, 1), 1))

    def test_check_loss_false(self):
        self.assertFalse(check_loss(self.board, (2, 1), 3))

    def test_solution(self):
        correct = [3]
        self.assertEqual(solution(self.board, (2, 1)), correct)


if __name__ == "__main__":
    unittest.main()

