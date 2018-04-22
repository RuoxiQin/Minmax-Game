#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The random evaluation function
"""


from evaluator import Evaluator
from random_choice import random_player

def random_evaluation(board, last_move, is_me, empty_positions, times):
    """
    Evaluate the current situation for me
    Doesn't modify the board nor empty_positions
    """
    e = Evaluator(board, random_player, random_player, last_move, is_me, 
        empty_positions)
    return e.simulate(times)
