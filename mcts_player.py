#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The MCTS algorithm
"""

from random_choice import *
from copy import deepcopy
import math
import random
from random_evaluation import random_evaluation
inf = float("inf")


class TreeNode:
    def __init__(self, is_me, parent, score=0, visit=1, is_leaf=False, \
        children=None):
        self.is_me = is_me
        self.parent = parent
        self.score = score
        self.visit = visit
        self.is_leaf = is_leaf
        if children is None:
            self.children = {}
        else:
            self.children = children


class MCTS:
    def __init__(self, search_time):
        self.search_time = search_time
        self.c = math.sqrt(2)
        self.gamma = 0.9

    def play(self, board, last_move, empty_positions, info=None):
        self.root = TreeNode(True, None)
        self.last_move = last_move
        # Expand the tree
        for i in range(self.search_time):
            self.board = deepcopy(board)
            self.empty_positions = deepcopy(empty_positions)
            self._expand()
        # Choose the best move
        if len(self.root.children) > 0:
            highest_score = -inf
            for (color, x, y) in self.root.children.keys():
                score = self.root.children[(color, x, y)].score
                if score > highest_score:
                    highest_score = score
                    best_color = color
                    best_move = (x, y)
        else:
            # No solution under this situation. Lose the game
            #best_color = 1
            #best_move = get_next_positions(board, last_move)[0]
            sys.stderr.write("I MCTS lose the game")
        return best_color, best_move, None


    def _expand(self):
        node = self.root
        # Selection
        best_move = self.last_move
        while len(node.children) > 0:
            best_ucb1 = -inf
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
            node = best_child
            self.board[best_move[0]][best_move[1]] = best_color
            self.empty_positions -= set((best_move,))
        # Expantion
        if not node.is_leaf:
            for move in get_next_positions(self.board, best_move):
                colors = solution(self.board, move)
                for color in colors:
                    node.children[(color, move[0], move[1])] = \
                        TreeNode(not node.is_me, node)
            # Check whether this node is leaf
            if len(node.children) == 0:
                node.is_leaf = True
                if node.is_me:
                    node.score = -1.0
                else:
                    node.score = 1.0
            else:
                # Rollout
                node.score = random_evaluation(\
                    self.board, best_move, node.is_me, self.empty_positions, 1)
        # Back Propagation
        node.visit += 1.0
        score = node.score * self.gamma
        while node.parent is not None:
            node = node.parent
            node.score = (node.visit * node.score + score) / (node.visit + 1.0)
            node.visit += 1.0
            score *= self.gamma
            