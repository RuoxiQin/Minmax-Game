#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Project 3: Game in AI
Author: Ruoxi Qin & HUI HAO
Instruction: To test the code, use the command:
java AtroposGame 7 "python3 rxqinPlayer.py"
"""

import sys
from copy import deepcopy
import random
import math
inf = float("inf")
simulation_time = 2    # Number of simulation
search_num = 400       # Number of search time



def boardState():
    """
    Read the state of the current board
    """
    #### Step 1: board pre-process
    board = sys.argv[1].split("L")[0] 

    board_mat = [[int(x) for x in list(line[:-1])] for line in board.split("[")[1:]] 

    board_mat.insert(0, [])
    board_mat[len(board_mat)-1].insert(0, -1)

    for sub_list in board_mat:
        sub_list += [-1 for i in range(8-len(sub_list))]

    #### Step 2: last_play pre-process
    last_play = sys.argv[1].split("L")[1][8:-1] 

    if last_play[0] != "(":
        return board_mat, None, None, None
    else:
        color, height, left, right = last_play[1:-1].split(',',3)
        last_play_color = int(color)
        last_play_xcoordinate = len(board_mat)-1-int(height)
        last_play_ycoordinate = int(left)

        return board_mat, last_play_color, last_play_xcoordinate, last_play_ycoordinate



def modifyBoard(board_mat, color, xcoordinate, ycoordinate):
    """
    Modify the board based on the output of the algorithm
    """
    # print my move to stdout for AtroposGame in standard format.
    height = len(board_mat)-1-xcoordinate
    left = ycoordinate
    right = xcoordinate - ycoordinate

    myMove = "(" + str(color) + "," + str(height) + "," + str(left) + "," + str(right) + ")"
    sys.stdout.write(myMove)


#-----------------------------util--------------------------------
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
    """
    Return a list of next possible play
    """
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

#------------------------Evaluator----------------------------
class Evaluator:
    """
    Evaluate the board by playing against myself
    """
    def __init__(
        self, board, me, opponent, last_move, my_turn, empty_positions):
        self.board = board
        self.me = me
        self.opponent = opponent
        self.last_move = last_move
        self.my_turn = my_turn
        self.empty_positions = empty_positions

    def simulate_one_time(self, result=None):
        """
        Simulate one time
        """
        board = deepcopy(self.board)
        empty_positions = deepcopy(self.empty_positions)
        me_info = {}
        opponent_info = {}
        if self.my_turn:
            opponent_move = self.last_move
            while True:
                # My move
                me_color, me_move, me_info = self.me(
                    board, opponent_move, empty_positions, me_info)
                if me_info > 0:
                    board[me_move[0]][me_move[1]] = me_color
                    empty_positions -= set((me_move,))
                else:
                    return me_info
                # Opponent move
                opponent_color, opponent_move, opponent_info = self.opponent(
                    board, me_move, empty_positions, opponent_info)
                if opponent_info > 0:
                    board[opponent_move[0]][opponent_move[1]] = \
                    opponent_color
                    empty_positions -= set((opponent_move,))
                else:
                    return -opponent_info
        else:
            me_move = self.last_move
            while True:
                # Opponent move
                opponent_color, opponent_move, opponent_info = self.opponent(
                    board, me_move, empty_positions, opponent_info)
                if opponent_info > 0:
                    board[opponent_move[0]][opponent_move[1]] = \
                    opponent_color
                    empty_positions -= set((opponent_move,))
                else:
                    return -opponent_info
                # My move
                me_color, me_move, me_info = self.me(
                    board, opponent_move, empty_positions, me_info)
                if me_info > 0:
                    board[me_move[0]][me_move[1]] = me_color
                    empty_positions -= set((me_move,))
                else:
                    return me_info

    def simulate(self, time):
        """
        Simulate time times and return the average score
        """
        score = 0
        for i in range(time):
            score += self.simulate_one_time()
        return score / time
        

#------------------------Random Evaluation----------------------
def random_evaluation(board, last_move, is_me, empty_positions, times):
    """
    Evaluate the current situation for me using 2 random players
    Doesn't modify the board nor empty_positions
    """
    e = Evaluator(board, random_player, random_player, last_move, is_me, 
        empty_positions)
    return e.simulate(times)

#----------------------------------MCTS--------------------------
class TreeNode:
    """
    The Tree Node of the MC search tree
    """
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
    """
    The MCTS player
    """
    def __init__(self, search_time):
        self.search_time = search_time
        self.c = math.sqrt(2)
        self.gamma = 0.9

    def play(self, board, last_move, empty_positions, info=None):
        """
        Make the move based on current situation
        """
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
            best_color = 1
            best_move = get_next_positions(board, last_move)[0]
            sys.stderr.write("I MCTS lose the game")
        return best_color, best_move, None


    def _expand(self):
        """
        Expand the search tree to find the best move
        """
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
                    self.board, best_move, node.is_me, self.empty_positions, \
                    simulation_time)
        # Back Propagation
        node.visit += 1.0
        score = node.score * self.gamma
        while node.parent is not None:
            node = node.parent
            node.score = (node.visit * node.score + score) / (node.visit + 1.0)
            node.visit += 1.0
            score *= self.gamma
            

if __name__ == "__main__": 
    # Get the board state
    board_mat, last_play_color, last_play_xcoordinate, last_play_ycoordinate = \
        boardState()
    if last_play_xcoordinate is not None:
        last_move = (last_play_xcoordinate, last_play_ycoordinate)
    else:
        last_move = None
    board_copy = deepcopy(board_mat)

    # Decide how to play using MCTS algorithm
    player = MCTS(search_num)
    my_color, my_move, info = \
        player.play(board_mat, last_move, get_empty_positions(board_mat))

    my_x_coordinate = my_move[0]
    my_y_coordinate = my_move[1]

    # Output the result
    modifyBoard(board_mat, my_color, my_x_coordinate, my_y_coordinate)
