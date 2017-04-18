import numpy as np

PLAYER_1 = 1
EMPTY = 0
PLAYER_2 = -1
PLAYER_1_TOKEN = 'X'
PLAYER_2_TOKEN = 'O'
EMPTY_TOKEN = ' '
CAT_GAME = -2
NO_WIN = 0


class TTT:

  def __init__(self, verbose):
    #create a 3x3 array for the board
    self.board = np.full((3,3), EMPTY)
    self.verbose = verbose

  def draw_board(self):
    temp_board = [[PLAYER_1_TOKEN if x == PLAYER_1 else PLAYER_2_TOKEN if x == PLAYER_2 else EMPTY_TOKEN for x in y] for y in self.board]
    print " " + temp_board[0][0] + " | " + temp_board[0][1] + " | "  + temp_board[0][2]
    print "----------"
    print " " + temp_board[1][0] + " | " + temp_board[1][1] + " | "  + temp_board[1][2]
    print "----------"
    print " " + temp_board[2][0] + " | " + temp_board[2][1] + " | "  + temp_board[2][2]

  def move(self, player, move):
    if self.board[move[0]][move[1]] != EMPTY:
      raise InvalidMoveException("Position already taken")

    self.board[move[0]][move[1]] = player

  def check_win(self):
    #check rows and for empty
    has_empty = False
    for row in self.board:
      temp_set = set(row)
      if len(temp_set) == 1 and row[0] != EMPTY:
        return row[0]
      if not has_empty and EMPTY in temp_set:
        has_empty = True

    #check columns
    for row in np.transpose(self.board):
      if len(set(row)) == 1 and row[0] != EMPTY:
        return row[0]

    #check diagonals
    if len(set([self.board[i][i] for i in xrange(len(self.board))])) == 1 and self.board[0][0] != EMPTY:
      return self.board[0][0]

    if len(set([self.board[i][len(self.board) - i - 1] for i in xrange(len(self.board))])) == 1 and self.board[0][len(self.board) - 1] != EMPTY:
      return self.board[0][len(self.board) - 1]

    if not has_empty:
      return CAT_GAME

    return NO_WIN



class InvalidMoveException(Exception):
  def __init__(self, message):
    self.message = message


