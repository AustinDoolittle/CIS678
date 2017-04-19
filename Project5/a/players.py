from ttt import EMPTY
from random import randint

class Player:

  def __init__(self, player_id):
    self.id = player_id

  def move(self, board):
    while True:
      temp_move = [randint(0,len(board) - 1), randint(0,len(board) - 1)]
      if board[temp_move[0]][temp_move[1]] == EMPTY:
        break

    print str(temp_move[0]) + " " + str(temp_move[1])
    return temp_move

  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False

    return self.id == other.id

  def __ne__(self, other):
    return not self.__eq__(other)

class HumanPlayer(Player):

  def move(self, board):
    while True:
      try:
        temp_move = map(int, raw_input().split())
      except ValueError as e:
        print "Input could not be parsed to ints, should be two ints in range 0-2 seperated by a space"
        continue
      if len(temp_move) != 2 or temp_move[0] < 0 or temp_move[0] > len(board) - 1 or temp_move[1] < 0 or temp_move[1] > len(board) - 1:
        print "Input must be two ints in range 0-2 seperated by a space"
        continue
      if board[temp_move[0]][temp_move[1]] != EMPTY:
        print "Invalid move, space already filled"
        continue
      break
    return temp_move


class LearningPlayer(Player):

  def move(self, board):
    raise NotImplementedError