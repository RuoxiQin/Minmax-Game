#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The MCTS algorithm
"""

from random_choice import *
from copy import deepcopy
import math


class TreeNode:
    def __init__(self, is_me, score=0, visit=1, children=None):
        self.is_me = is_me
        self.score = score
        self.visit = visit
        if children is None:
            self.children = {}
        else:
            self.children = children
        self.c = math.sqrt(2)


class MCTS:
    def __init__(self, search_time):
        self.search_time = search_time

    def play(self, board, last_move, empty_positions, info=None):
        self.root = TreeNode(True)
        for i in range(self.search_time):
            self.board = deepcopy(board)
            self.empty_positions = deepcopy(empty_positions)
            self._expand()

    def _expand(self):
        node = self.root
        # Selection
        while len(node.children) > 0:
            best_ucb1 = -float("inf")
            for move in node.children:
                child = node.children[move]
                if node.is_me:
                    ucb1 = child.score / node.visit + \
                        self.c * math.sqrt(math.log(node.visit) / child.visit)
                else:
                    ucb1 = -child.score / node.visit + \
                        self.c * math.sqrt(math.log(node.visit) / child.visit)
                if ucb1 > best_ucb1:
                    best_ucb1 = ucb1
                    best_child = child
                    best_move = (move[1], move[2])
                    best_color = move[0]
            node = child
            self.board[best_move[0]][best_move[1]] = best_color
            self.empty_positions -= set((best_move,))
        # Expantion
        for move in get_next_positions(\
            self.board, (best_move[1], best_move[2])):
            colors = 
        





            
