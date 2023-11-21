from game import game

from outputting.printing import print_help
from outputting.text_styles import red_bold_text


if __name__ == '__main__':
    try:
        print_help()
        main_game = game.Game()
        count_games = main_game.start()
        print(f'Сыграно игр: {count_games}')
        print(f'\n{red_bold_text}Goodbye!')
    except KeyboardInterrupt:
        print(f'\n{red_bold_text}Goodbye!')
