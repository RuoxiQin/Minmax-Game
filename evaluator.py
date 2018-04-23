#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The evaluator class
"""


from copy import deepcopy
import multiprocessing as mp


class Evaluator:
    def __init__(
        self, board, me, opponent, last_move, my_turn, empty_positions, \
        mt=False):
        self.board = board
        self.me = me
        self.opponent = opponent
        self.last_move = last_move
        self.my_turn = my_turn
        self.empty_positions = empty_positions
        self.mt = mt

    def simulate_one_time(self, result=None):
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
                elif me_info == 0:
                    if result is not None:
                        result.put(0)
                    return 0
                elif me_info == -1:
                    if result is not None:
                        result.put(-1)
                    return -1
                # Opponent move
                opponent_color, opponent_move, opponent_info = self.opponent(
                    board, me_move, empty_positions, opponent_info)
                if opponent_info > 0:
                    board[opponent_move[0]][opponent_move[1]] = \
                    opponent_color
                    empty_positions -= set((opponent_move,))
                elif opponent_info == 0:
                    if result is not None:
                        result.put(0)
                    return 0
                elif opponent_info == -1:
                    if result is not None:
                        result.put(-1)
                    return 1
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
                elif opponent_info == 0:
                    if result is not None:
                        result.put(0)
                    return 0
                elif opponent_info == -1:
                    if result is not None:
                        result.put(1)
                    return 1
                # My move
                me_color, me_move, me_info = self.me(
                    board, opponent_move, empty_positions, me_info)
                if me_info > 0:
                    board[me_move[0]][me_move[1]] = me_color
                    empty_positions -= set((me_move,))
                elif me_info == 0:
                    if result is not None:
                        result.put(0)
                    return 0
                elif me_info == -1:
                    if result is not None:
                        result.put(-1)
                    return -1

    def simulate(self, time):
        if not self.mt:
            """
            score = 0
            for i in range(time):
                score += self.simulate_one_time()
            return score
            """
            pool = mp.Pool()
            results = [pool.apply(self.simulate_one_time, args=(None,)) for i in range(time)]
            return sum(results)
        else:
            score = 0
            cpu_core = mp.cpu_count() - 1
            pip = mp.Queue()
            pool = []
            for i in range(time // cpu_core):
                pool = []
                for j in range(cpu_core):
                    pool.append(
                        mp.Process(target=self.simulate_one_time, args=(pip,)))
                for p in pool:
                    p.start()
                for j in range(cpu_core):
                    score += pip.get()
                for p in pool:
                    p.join()
            rest = time % cpu_core
            pool = []
            for j in range(rest):
                pool.append(
                    mp.Process(target=self.simulate_one_time, args=(pip,)))
            for p in pool:
                p.start()
            for j in range(rest):
                score += pip.get()
            for p in pool:
                p.join()
            return score
