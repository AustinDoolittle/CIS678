import argparse as ap
from ttt import TTT, InvalidMoveException, PLAYER_1, PLAYER_2, CAT_GAME
from random import randint
import sys

PLAYER_VS_PLAYER = "PvP"
PLAYER_VS_COMPUTER = "PvC"
PLAYER_VS_LEARNER = "PvL"
LEARNER_VS_COMPUTER = "LvC"
LEARNER_VS_LEARNER = "LvL"

def get_player_move():
  while True:
    try:
      move = map(int, raw_input().split())
    except ValueError as e:
      print "Input could not be parsed to ints, should be two ints in range 0-2 seperated by a space"
      continue
    if len(move) != 2 or move[0] < 0 or move[0] > 2 or move[1] < 0 or move[1] > 2:
      print "Input must be two ints in range 0-2 seperated by a space"
      continue
    break
  return move

def get_random_move():
  return [randint(0,2), randint(0,2)]

def main(args):
  parser = ap.ArgumentParser(description="A Game of Tic Tac Toe that gradually learns how to play over time")
  parser.add_argument("-v", "--verbose", action="store_true", default=False, help="Increase verbosity")
  parser.add_argument("--gametype", default=PLAYER_VS_PLAYER, 
                      choices=[PLAYER_VS_PLAYER, PLAYER_VS_COMPUTER, PLAYER_VS_LEARNER, LEARNER_VS_COMPUTER, LEARNER_VS_LEARNER])
  args = parser.parse_args(args)

  if args.gametype in [PLAYER_VS_PLAYER, PLAYER_VS_COMPUTER]:
    game = TTT(args.verbose)
    
    curr_player = 1
    while True:

      while True:
        print
        print "Player " + ("1" if curr_player == PLAYER_1 else "2") + ", your move: "
        if args.gametype == PLAYER_VS_PLAYER or curr_player == PLAYER_1:
          move = get_player_move()
        else:
          move = get_random_move()
          print str(move[0]) + " " + str(move[1])
        try: 
          game.move(curr_player, move)
        except InvalidMoveException as e:
          print "That spot is already taken"
          continue
        break

      print
      game.draw_board()

      check = game.check_win()
      if check == PLAYER_1:
        print "Player 1 wins!"
        break
      elif check == PLAYER_2:
        print "Player 2 wins!"
        break
      elif check == CAT_GAME:
        print "It's a tie!"
        break

      curr_player = -curr_player
  else:
    raise NotImplementedError()
    



if __name__ == "__main__":
  main(sys.argv[1:])