#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The MCTS algorithm
"""



class MCTS:
    def __init__(self, search_time):
        self.search_time = search_time

    def play(self, board, last_move, empty_positions, info=None):
