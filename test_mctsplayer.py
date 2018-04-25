from mcts_player import MCTS
from random_choice import get_empty_positions
from random_choice import check_loss
from copy import deepcopy
from random_choice import random_player
from random_choice import get_empty_neighboor


board_mat = [
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], 
    [1, 3, -1, -1, -1, -1, -1, -1, -1, -1], 
    [3, 0, 2, -1, -1, -1, -1, -1, -1, -1], 
    [1, 0, 0, 3, -1, -1, -1, -1, -1, -1], 
    [3, 0, 0, 0, 2, -1, -1, -1, -1, -1], 
    [1, 0, 0, 0, 0, 3, -1, -1, -1, -1], 
    [3, 0, 0, 0, 0, 0, 2, -1, -1, -1], 
    [1, 0, 0, 0, 0, 0, 0, 3, -1, -1], 
    [3, 0, 0, 0, 0, 0, 0, 0, 2, -1], 
    [-1, 1, 2, 1, 2, 1, 2, 1, 2, -1]]
last_move = None
# Decide how to play using random_Player
player = MCTS(300)
empty_positions = get_empty_positions(board_mat)
while len(empty_positions) > 0:
    board_copy = deepcopy(board_mat)
    my_color, my_move, info = \
        player.play(board_mat, last_move, get_empty_positions(board_mat))
    """
    my_color, my_move, info = \
		random_player(board_mat, my_move, get_empty_positions(board_mat))
    """
    print(my_move)
    if board_mat != board_copy:
        print("Board changed!")
        break
    if last_move is not None:
        if my_move not in get_empty_neighboor(board_copy, last_move):
            print("illegal move at " + str(my_move))
            break
    if check_loss(board_copy, my_move, my_color):
        print("One failed the game!")
        break
    board_mat[my_move[0]][my_move[1]] = my_color
    empty_positions = get_empty_positions(board_mat)
    last_move = my_move
print(board_mat)

