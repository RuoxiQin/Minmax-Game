#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The minmax search algorithm
"""

from copy import deepcopy
import random
from random_choice import *
from random_evaluation import random_evaluation
inf = float("inf")


class MinmaxPlayer:
    def __init__(self, depth, simulation_time):
        self.depth = depth
        self.simulation_time = simulation_time

    def play(self, board, last_move, empty_positions, info=None):
        self.board = deepcopy(board)
        self.last_move = last_move
        self.empty_positions = deepcopy(empty_positions)
        score, color, position = self._compute_score(self.board, 
            self.last_move, self.empty_positions, 0, inf, -inf, True)
        return color, position, info

    def _compute_score(self, board, last_move, empty_positions, depth, 
        parent_best, parent_worst, is_me):
        if depth >= self.depth:
            return random_evaluation(board, last_move, is_me, empty_positions, \
                self.simulation_time), None, None
        if last_move is not None:
            positions = get_empty_neighboor(board, last_move)
            if len(positions) == 0:
                positions = list(empty_positions)
        else:
            positions = list(empty_positions)
        if len(positions) == 0:
            assert False, "There is a tie!!!"
            return 0, None, None
        if len(positions) > 10:
            # If the search space is larger than 10, just pick a random one
            random.shuffle(positions)
            for position in positions:
                choices = solution(board, position)
                if len(choices) > 0:
                    return 0, random.choice(choices), position
            # Cannot put any color in any position
            if is_me:
                return -self.simulation_time, 1, positions[0]
            else:
                return self.simulation_time, 1, positions[0]
        if is_me:
            my_best = -inf
            for position in positions:
                choices = solution(board, position)
                if len(choices) == 0:
                    score = -self.simulation_time
                    if score > my_best:
                        my_best = score
                        my_color = 1
                        my_position = position
                    if my_best >= parent_best:
                        return my_best, my_color, my_position
                else:
                    empty_positions -= set((position,))
                    for color in choices:
                        board[position[0]][position[1]] = color
                        score, my_color, my_position = \
                            self._compute_score(\
                            board, position, empty_positions,\
                            depth+1, my_best, parent_worst, not is_me)
                        if score > my_best:
                            my_best = score
                            my_color = color
                            my_position = position
                        if my_best >= parent_best:
                            # Recover the board and the empty_positions
                            board[position[0]][position[1]] = 0
                            empty_positions.add(position)
                            return my_best, my_color, my_position
                    # Recover the board and the empty_positions
                    board[position[0]][position[1]] = 0
                    empty_positions.add(position)
            return my_best, my_color, my_position
        else:
            my_worst = inf
            for position in positions:
                choices = solution(board, position)
                if len(choices) == 0:
                    score = self.simulation_time
                    if score < my_worst:
                        my_worst = score
                        my_color = 1
                        my_position = position
                    if my_worst <= parent_worst:
                        return my_worst, my_color, my_position
                else:
                    empty_positions -= set((position,))
                    for color in choices:
                        board[position[0]][position[1]] = color
                        score, my_color, my_position = \
                            self._compute_score(\
                            board, position, empty_positions,\
                            depth+1, parent_best, my_worst, not is_me)
                        if score < my_worst:
                            my_worst = score
                            my_color = color
                            my_position = position
                        if my_worst <= parent_worst:
                            # Recover the board and the empty_positions
                            board[position[0]][position[1]] = 0
                            empty_positions.add(position)
                            return my_worst, my_color, my_position
                    # Recover the board and the empty_positions
                    board[position[0]][position[1]] = 0
                    empty_positions.add(position)
            return my_worst, my_color, my_position
