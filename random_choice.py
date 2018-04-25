#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Random choice and evaluation
"""


import random
from copy import deepcopy


def get_neighboor(position):
    """
    Return the neighboors surrounding the position. 
    Postion cannot be on the edge
    """
    x = position[0]
    y = position[1]
    return [(x, y-1), (x+1, y), (x+1, y+1), (x, y+1), (x-1, y), (x-1, y-1)]


def get_empty_positions(board):
    """
    Return a set of all empty positions. 
    """
    result = set()
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] == 0:
                result.add((x, y))
    return result

def get_next_positions(board, position):
    if position is not None:
        positions = get_empty_neighboor(board, position)
        if len(positions) == 0:
            positions = list(get_empty_positions(board))
    else:
        positions = list(get_empty_positions(board))
    return positions


def get_empty_neighboor(board, position):
    """
    Return a list of uncolored neighboors. Postion cannot be on the edge
    """
    result = []
    for point in get_neighboor(position):
        if board[point[0]][point[1]] == 0:
            result.append(point)
    return result


def check_loss(board, position, color):
    """
    Check whether this move does not lead to loss
    :param board: 2-dim python list
    :param position: the position of the last move. Python tuple
    :param color: The color of that position
    :return: If this leads to loss, return True
    """
    x = position[0]
    y = position[1]
    illegal = set([1, 2, 3])
    neighboors = get_neighboor(position)
    for i in range(len(neighboors) - 1):
        if set((color, board[neighboors[i][0]][neighboors[i][1]], 
            board[neighboors[i+1][0]][neighboors[i+1][1]])) == illegal:
            return True
    if set((color, board[neighboors[0][0]][neighboors[0][1]], 
        board[neighboors[-1][0]][neighboors[-1][1]])) == illegal:
        return True
    return False


def solution(board, position):
    """
    Return the solution for the given position
    :param board: 2-dim python list
    :param position: the position of the last move. Python tuple
    :return: a list of possible solutions (colors)
    """
    assert(board[position[0]][position[1]] == 0)
    result = []
    for color in range(1, 4):
        if not check_loss(board, position, color):
            result.append(color)
    return result

def random_player(board, last_move, empty_positions, info=None):
    """
    The random player
    """
    if last_move is not None:
        positions = get_empty_neighboor(board, last_move)
        if len(positions) == 0:
            positions = list(empty_positions)
    else:
        positions = list(empty_positions)
    if len(positions) == 0:
        # No place to play. Tie
        return 0, (-1, -1), 0
    random.shuffle(positions)
    for position in positions:
        moves = solution(board, position)
        if len(moves) == 0:
            continue
        return random.choice(moves), position, 1
    # Lose the game
    return 1, positions[0], -1
