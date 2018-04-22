from minmax_player import MinmaxPlayer
from random_choice import get_empty_positions


board_mat = [[-1, -1, -1, -1, -1, -1, -1, -1], [1, 3, -1, -1, -1, -1, -1, -1], [3, 0, 2, -1, -1, -1, -1, -1], [1, 0, 0, 3, -1, -1, -1, -1], [3, 1, 0, 0, 2, -1, -1, -1], [1, 0, 0, 0, 0, 3, -1, -1], [3, 0, 0, 0, 0, 0, 2, -1], [-1, 1, 2, 1, 2, 1, 2, -1]]
last_move = None
# Decide how to play using random_Player
player = MinmaxPlayer(3, 1)
my_color, my_move, info = \
    player.play(board_mat, last_move, get_empty_positions(board_mat))
my_x_coordinate = my_move[0]
my_y_coordinate = my_move[1]
print(my_color)
print(my_move)
