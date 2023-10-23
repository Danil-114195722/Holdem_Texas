from game import game
from outputting.printing import print_help


if __name__ == '__main__':
    # print_help()
    main_game = game.Game(first_stack='human')
    main_game.start()
