'''
Sha Lai
Last Modified: 04/24/2018

This is an AI program implemented to play the Atropos game for course
CS640. The execution must follow the instruction on the project page
strictly.
'''

import sys
import random

#============================ Constants ============================#
SPLITTERS = ("LastPlay:", "][") # used to read input
MAX_LEVEL = 3 # the maximum level for min-max algorithm
NULL_MOVE = [-1, -1, -1, -1] # used when initial LastPlay = null
EVALUATOR_WEIGHT = [2, 1] # used to compute the evaluation score
#=========================== End of Section ========================#
#=========================== Misc Functions ========================#
# Just for debugging purpose.
def write(messages):
   if messages is list:
      for message in messages:
         sys.stderr.write(str(message) + "\n")
         outputFile.write(str(message) + "\n")
   else:
      sys.stderr.write(str(messages) + "\n")
      outputFile.write(str(messages) + "\n")

def output(move):
   """Outputs the next move.
   Parameters
   ----------
   move : [int, int, int, int]
      Must in the format (color, coor1, coor2, coor3).
   Returns
   -------
   None
   """
   moveString = "(" + str(move[0]) + "," +\
                     str(move[1]) + "," +\
                     str(move[2]) + "," +\
                     str(move[3]) + ")"
   sys.stdout.write(moveString)

def convert(inputString):
   """Converts the input string representations to certain data
   structures.
   Parameters
   ----------
   inputString : string
   Returns
   -------
   board : List[List[int]]
   lastMove : [int, int, int, int]
   """
   inputStringSplit = inputString.split(SPLITTERS[0])
   boardString = inputStringSplit[0]
   boardString = boardString[1 : len(boardString) - 1]
   boardStringSplit = boardString.split(SPLITTERS[1])
   board = []
   for s in boardStringSplit:
      row = []
      for n in s:
         row.append(int(n))
      board.append(row)
   lastMove = NULL_MOVE
   if inputStringSplit[1] != "null":
      lastMove = list(eval(inputStringSplit[1]))
   return board, lastMove

#=========================== End of Section ========================#
#========================== Helper Functions =======================#
def getNextMoves(board, lastMove):
   """Finds the set of next possible moves.
   Parameters
   ----------
   board : List[List[int]]
   lastMove : [int, int, int, int]
   Returns
   -------
   nextMoves : List[[int, int, int, int]]
   """
   nextMoves = []
   size = lastMove[1] + lastMove[2] + lastMove[3] - 2
   # first check the neighbors if possible
   if lastMove != NULL_MOVE:
      neighbors = getNeighbors(lastMove[1:])
      for neighbor in neighbors:
         nextMove = [0] + neighbor
         if isValidMove(board, nextMove, size):
            for color in (1, 2, 3):
               nextMove[0] = color
               nextMoves.append(nextMove[:])

   # if no neighbor available, then check the entire board
   if len(nextMoves) == 0:
      for i in range(1, len(board) - 1):
         for j in range(1, len(board[i]) - 1):
            if board[i][j] == 0:
               nextMove = [0, len(board) - 1 - i, j, len(board[i]) - 1 - j]
               for color in (1, 2, 3):
                  nextMove[0] = color
                  nextMoves.append(nextMove[:])
   return nextMoves

def getNeighbors(coordinate):
   """Returns the 6 neighbors of the current coordinate. Note that
   the results may be invalid on the given board.
   Parameters
   ----------
   coordinate : [int, int, int]
   Returns
   -------
   neighbors : List[[int, int, int]]
   """
   x, y, z = coordinate[0], coordinate[1], coordinate[2]
   '''
   Convention:
   
      6  1
      
   5        2
   
      4  3
   '''
   neighbors = [[x + 1, y, z - 1], [x, y + 1, z - 1], [x - 1, y + 1, z],\
               [x - 1, y, z + 1], [x, y - 1, z + 1], [x + 1, y - 1, z]]
   return neighbors

def isValidMove(board, move, size):
   """Checks if the move is valid.
   Parameters
   ----------
   board : List[List[int]]
   move : [int, int, int, int]
   size : int
   Returns
   -------
   boolean
   """
   return isValidPlace(board, move[1:], size) and\
         getColor(board, move[1:], size) == 0

def isValidPlace(board, coordinate, size):
   """Checks if the coordinate is valid.
   Parameters
   ----------
   board : List[List[int]]
   coordinate : [int, int, int, int]
   size : int
   Returns
   -------
   boolean
   """
   height = size + 1 - coordinate[0]
   left = coordinate[1]
   # print("[ivp]height, left = " + str(height) + ", " + str(left))
   return 0 <= height < len(board) and\
         0 <= left < len(board[height]) and\
         0 <= coordinate[2]

def getColor(board, coordinate, size):
   """Takes a coordinate in the form [x, y, z] and returns the color
   piece on the board.
   Parameters
   ----------
   board : List[List[int]]
   coordinate : [int, int, int]
      The coordinate must be a valid one.
   size : int
      The game size.
   Returns
   -------
   color : int
   """
   height = size + 1 - coordinate[0]
   left = coordinate[1]
   # print("[gc]height, left = " + str(height) + ", " + str(left))
   return board[height][left]

def countBadTriangles(board, move):
   """Counts the number of bad triangles resulted from the move,
   assuming that the move is valid. A bad triangle is a triangle of
   3 different colors.
   Parameters
   ----------
   board : List[List[int]]
   move : [int, int, int, int]
   Returns
   -------
   badCount : int
      This is the number of bad triangles is the move is made.
   """
   neighbors = getNeighbors(move[1:])
   neighborColors = []
   size = move[1] + move[2] + move[3] - 2
   for i in range(len(neighbors)):
      if isValidPlace(board, neighbors[i], size):
         neighborColors.append(getColor(board, neighbors[i], size))
   badCount = 0
   for i in range(len(neighborColors)):
      j = 0
      if i < len(neighborColors) - 1:
         j = i + 1
      colorTuple = [move[0], neighborColors[i], neighborColors[j]]
      colorTuple.sort()
      if colorTuple == [1, 2, 3]:
         badCount += 1
   return badCount

def countGoodNeighbors(board, move):
   """Counts the number of good neighbors resulted from the move,
   assuming that the move is valid. A good neighbor is a neighbor of
   the same color as the current piece.
   Parameters
   ----------
   board : List[List[int]]
   move : [int, int, int, int]
   Returns
   -------
   goodCount : int
      This is the number of good neighbors if the move is made.
   """
   neighbors = getNeighbors(move[1:])
   neighborColors = []
   size = move[1] + move[2] + move[3] - 2
   for i in range(len(neighbors)):
      if isValidPlace(board, neighbors[i], size):
         neighborColors.append(getColor(board, neighbors[i], size))
   goodCount = 0
   for i in range(len(neighborColors)):
      if neighborColors[i] == move[0]:
         goodCount += 1
   return goodCount

def makeMove(board, move):
   """Makes a move on the current board, assuming that the move is
   valid.
   Parameters
   ----------
   board : List[List[ing]]
   move : [int, int, int, int]
   Returns
   -------
   None
   """
   size = move[1] + move[2] + move[3] - 2
   board[len(board) - 1 - move[1]][move[2]] = move[0]
   
def undoMove(board, move):
   """Undoes a move on the current board, assuming that the move
   is valid.
   Parameters
   ----------
   board : List[List[ing]]
   move : [int, int, int, int]
   Returns
   -------
   None
   """
   makeMove(board, [0] + move[1 :])
      
#=========================== End of Section ========================#
#=========================== Main Functions ========================#

def evaluate(board, lastMove):
   """Evaluates the current board and returns the score of the move,
   assuming that the move has been made. A high score means more
   benefits to the player being considered.
   board : List[List[ing]]
   lastMove : [int, int, int, int]
   Returns
   -------
   score : int
   """
   scores = [0] * len(EVALUATOR_WEIGHT)
   
   # first compute the bad traingle ratio for the opponent and this
   # shoulbe be high to benefit self ratio
   nextMoves = getNextMoves(board, lastMove)
   for nextMove in nextMoves:
      scores[0] += countBadTriangles(board, nextMove)
   if len(nextMoves) > 0:
      scores[0] /= len(nextMoves)
   
   # then, compute the good triangle ratio for self
   scores[1] = countGoodNeighbors(board, lastMove) / 6
   
   finalScore = 0
   for i in range(len(scores)):
      finalScore += EVALUATOR_WEIGHT[i] * scores[i]
   return finalScore

def miniMax(board, lastMove, state, level, alpha, beta):
   """Performs the minimax algorithm and returns the optimal result.
   This alogrithm also uses alpha-beta pruning to speed up the
   process.
   Parameters
   ----------
   board : List[List[int]]
   nextMoves : List[(int, int, int, int)]
   state : int
      1 means max while -1 means min.
   level : int
      Indicates the current level of the tree.
   alpha, beta : int
      The variables that are used in alpha-beta pruning.
   Returns
   -------
   [int, int, int, int]
   """
   score, move = 0, None
   nextMoves = getNextMoves(board, lastMove)
   scores = []
   if level == 0 or len(nextMoves) == 0:
      '''
      Score is calculated based on the evaluation of the next set
      of possible moves.
      '''
      score = evaluate(board, lastMove)
   else:
      bestScore = 0
      if state == 1:
         bestScore = -sys.maxsize
      else:
         bestScore = sys.maxsize
      bestMove = None
      for nextMove in nextMoves:
         makeMove(board, nextMove)
         tempScore, tempMove =\
            miniMax(board, nextMove, -state, level - 1, alpha, beta)
         tempScore -= countBadTriangles(board, nextMove) * level * 10
         scores.append(tempScore)
         undoMove(board, nextMove)
         if state == 1:
            if bestScore < tempScore:
               bestScore = tempScore
               bestMove = nextMove
               if bestScore > alpha:
                  return bestScore, bestMove
               else:
                  beta = bestScore
         else:
            if bestScore > tempScore:
               bestScore = tempScore
               bestMove = nextMove
               if bestScore < beta:
                  return bestScore, bestMove
               else:
                  alpha = bestScore
      score, move = bestScore, bestMove
   return score, move

#=========================== End of Section ========================#
#=========================== Execution Codes =======================#

def makeDecision(board, lastMove):
   """Make a decision for the next move using minimax search.
   Parameters
   ----------
   board : List[List[int]]
   lastMove : [int, int, int, int]
   Returns
   -------
   nextMove : [int, int, int, int]
   """
   maxLevel = 1
   if lastMove != NULL_MOVE:
      maxLevel = MAX_LEVEL
   dummy, nextMove = miniMax(board, lastMove, 1, maxLevel,\
                              sys.maxsize, -sys.maxsize)
   return nextMove

if __name__ == '__main__':
   exampleInput = "[13][302][1023][30002][100003][3000002][10000003][300000002][12121212]LastPlay:null"
   board, lastMove = convert(exampleInput)
   outputFile = open("log.txt", 'w')
   if len(sys.argv) > 1:
      board, lastMove = convert(sys.argv[1])
      # outputFile.write(sys.argv[1] + "\n")
      # write("sys.argv = " + str(sys.argv))
   nextMove = makeDecision(board, lastMove)
   outputFile.close()
   output(nextMove)