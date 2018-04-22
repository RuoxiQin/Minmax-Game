from minmax_player import MinmaxPlayer
from random_choice import get_empty_positions
from random_choice import check_loss


board_mat = [[-1, -1, -1, -1, -1, -1, -1, -1], [1, 3, -1, -1, -1, -1, -1, -1], [3, 0, 2, -1, -1, -1, -1, -1], [1, 0, 0, 3, -1, -1, -1, -1], [3, 1, 0, 0, 2, -1, -1, -1], [1, 0, 0, 0, 0, 3, -1, -1], [3, 0, 0, 0, 0, 0, 2, -1], [-1, 1, 2, 1, 2, 1, 2, -1]]
my_move = None
# Decide how to play using random_Player
player = MinmaxPlayer(4, 10)
empty_positions = get_empty_positions(board_mat)
while len(empty_positions) > 0:
    my_color, my_move, info = \
        player.play(board_mat, my_move, get_empty_positions(board_mat))
    if my_move not in empty_positions:
        print("illegal move!")
        break
    if check_loss(board_mat, my_move, my_color):
        print("One failed the game!")
        break
    board_mat[my_move[0]][my_move[1]] = my_color
    empty_positions = get_empty_positions(board_mat)
print(board_mat)
