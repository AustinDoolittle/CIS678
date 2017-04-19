import argparse as ap
from ttt import TTT, PLAYER_1, PLAYER_2, CAT_GAME
from random import randint
from players import Player, HumanPlayer, LearningPlayer
import sys

PLAYER_VS_PLAYER = "PvP"
PLAYER_VS_COMPUTER = "PvC"
PLAYER_VS_LEARNER = "PvL"
LEARNER_VS_COMPUTER = "LvC"
LEARNER_VS_LEARNER = "LvL"

def main(args):
  parser = ap.ArgumentParser(description="A Game of Tic Tac Toe that gradually learns how to play over time")
  parser.add_argument("-v", "--verbose", action="store_true", default=False, help="Increase verbosity")
  parser.add_argument("--gametype", default=PLAYER_VS_PLAYER, 
                      choices=[PLAYER_VS_PLAYER, PLAYER_VS_COMPUTER, PLAYER_VS_LEARNER, LEARNER_VS_COMPUTER, LEARNER_VS_LEARNER])
  args = parser.parse_args(args)

  if args.gametype in [PLAYER_VS_PLAYER, PLAYER_VS_COMPUTER]:
    game = TTT(args.verbose)
    
    p1 = HumanPlayer(PLAYER_1)
    if args.gametype == PLAYER_VS_PLAYER:
      p2 = HumanPlayer(PLAYER_2)
    else:
      p2 = Player(PLAYER_2)

    curr_player = p1
    while True:

      print "\nPlayer " + ("1" if curr_player.id == PLAYER_1 else "2") + ", your move: "
      move = curr_player.move(game.board)
      game.move(curr_player.id, move)

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

      curr_player = p1 if curr_player == p2 else p2
  else:
    raise NotImplementedError()
    



if __name__ == "__main__":
  main(sys.argv[1:])