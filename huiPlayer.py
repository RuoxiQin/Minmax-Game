import sys
# print to stderr for debugging purposes
# remove all debugging statements before submitting your code

from random_choice import random_player
from random_choice import get_empty_positions
from minmax_player import MinmaxPlayer
from copy import deepcopy

def boardState():
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
	# modify the given board with target color and position
	board_mat[xcoordinate][ycoordinate] = color
	# print(board_mat)
	
	# print my move to stdout for AtroposGame in standard format.
	height = len(board_mat)-1-xcoordinate
	left = ycoordinate
	right = xcoordinate - ycoordinate

	myMove = "(" + str(color) + "," + str(height) + "," + str(left) + "," + str(right) + ")"
	sys.stdout.write(myMove)


if __name__ == "__main__": 
	# Get the board state
	board_mat, last_play_color, last_play_xcoordinate, last_play_ycoordinate = \
		boardState()
	if last_play_xcoordinate is not None:
		last_move = (last_play_xcoordinate, last_play_ycoordinate)
	else:
		last_move = None
	board_copy = deepcopy(board_mat)

	# Decide how to play using random_Player
	"""
	my_color, my_move, info = \
		random_player(board_mat, last_move, get_empty_positions(board_mat))
	"""
	player = MinmaxPlayer(3, 10)
	my_color, my_move, info = \
		player.play(board_mat, last_move, get_empty_positions(board_mat))

	assert board_mat == board_copy, "The board has changed!"
	assert my_move in get_empty_positions(board_copy), \
		"I interface detect an illegal move!!!"

	my_x_coordinate = my_move[0]
	my_y_coordinate = my_move[1]

	# Output the result
	modifyBoard(board_mat, my_color, my_x_coordinate, my_y_coordinate)


	"""
	boardState()

	board_mat = [[-1, -1, -1, -1, -1, -1, -1, -1], [1, 3, -1, -1, -1, -1, -1, -1], [3, 0, 2, -1, -1, -1, -1, -1], [1, 0, 0, 3, -1, -1, -1, -1], [3, 1, 0, 0, 2, -1, -1, -1], [1, 0, 0, 0, 0, 3, -1, -1], [3, 0, 0, 0, 0, 0, 2, -1], [-1, 1, 2, 1, 2, 1, 2, -1]]
	modifyBoard(board_mat, 7, 3, 1)
	"""
	# sys.argv[1] = "[13][302][1003][31002][100003][3000002][121212]LastPlay:(1,3,1,3)"
	# sys.argv[1] = "[13][302][1003][30002][100003][3000002][121212]LastPlay:null"



# sys.stderr.write(msg);

#parse the input string, i.e., argv[1]
 
#perform intelligent search to determine the next move

#print to stdout for AtroposGame
# sys.stdout.write("(3,2,2,2)");
# As you can see Zook's algorithm is not very intelligent. He 
# will be disqualified.

