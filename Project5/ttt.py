import numpy as np

PLAYER_1 = 1
PLAYER_2 = -1
PLAYER_1_TOKEN = 'X'
PLAYER_2_TOKEN = 'O'
EMPTY_TOKEN = ' '


class TTT:

  def __init__(self, verbose):
    #create a 3x3 array for the board
    self.board = np.full((3,3), EMPTY_TOKEN)
    self.verbose = verbose

  def draw_board(self):
    print " " + self.board[0][0] + " | " + self.board[0][1] + " | "  + self.board[0][2]
    print "----------"
    print " " + self.board[1][0] + " | " + self.board[1][1] + " | "  + self.board[1][2]
    print "----------"
    print " " + self.board[2][0] + " | " + self.board[2][1] + " | "  + self.board[2][2]

  def move(self, player, move):
    if self.board[move[0]][move[1]] != EMPTY_TOKEN:
      raise InvalidMoveException("Position already taken by token " + self.board[move[0]][move[1]])

    self.board[move[0]][move[1]] = PLAYER_1_TOKEN if player == PLAYER_1 else PLAYER_2_TOKEN

  def check_win(self):
    #check rows
    for board in [self.board, np.transpose(self.board)]:
      for row in board:
        if len(set(row)) == 1 and row[0] != EMPTY_TOKEN:
          return PLAYER_1 if row[0] == PLAYER_1_TOKEN else PLAYER_2

    if len(set([board[i][i] for i in xrange(len(board))])) == 1 and board[0][0] != EMPTY_TOKEN:
      return PLAYER_1 if board[0][0] == PLAYER_1_TOKEN else PLAYER_2

    if len(set([board[i][len(board) - i - 1] for i in xrange(len(board))])) == 1 and board[0][len(board) - 1] != EMPTY_TOKEN:
      return PLAYER_1 if board[0][len(board) - 1] == PLAYER_1_TOKEN else PLAYER_2



class InvalidMoveException(Exception):
  def __init__(self, message):
    self.message = message


