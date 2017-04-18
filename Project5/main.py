import argparse as ap
from ttt import TTT, InvalidMoveException, PLAYER_1, PLAYER_2
import sys



def get_move():
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

def main(args):
  parser = ap.ArgumentParser(description="A Game of Tic Tac Toe that gradually learns how to play over time")
  parser.add_argument("-v", "--verbose", action="store_true", default=False, help="Increase verbosity")
  args = parser.parse_args(args)

  game = TTT(args.verbose)
  
  curr_player = 1
  while True:
    print "Player " + ("1" if curr_player == PLAYER_1 else "2") + ", your move: "
    while True:
      move = get_move()
      try: 
        game.move(curr_player, move)
      except InvalidMoveException as e:
        print "That spot is already taken"
        continue
      break

    print
    game.draw_board()
    print

    check = game.check_win()
    if check == PLAYER_1:
      print "Player 1 wins!"
      break
    elif check == PLAYER_2:
      print "Player 2 wins!"
      break

    curr_player = -curr_player
  



if __name__ == "__main__":
  main(sys.argv[1:])