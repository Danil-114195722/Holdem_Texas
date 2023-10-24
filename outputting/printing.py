from typing import List
from random import choice as random_choice

from cards.card import Card
from outputting.text_styles import yellow_bold_text, clean_text, blue_bold_text, italic_text, red_italic_text, red_bold_text


# печать подсказки с правилами игры при запуске проги
def print_help() -> None:
    print('ЗДЕСЬ БУДУТ ПРАВИЛА!!!')
    input('Continue? [type something] ')


# печать карт игроков и стола
def print_table(human_cards: List[Card], table_cards: List[Card], comp_cards: List[Card] = None) -> None:
    # кол-во разделителя
    delimiter_count = 30

    human_beauty_cards = [card_obj.get_to_print() for card_obj in human_cards]
    table_beauty_cards = [card_obj.get_to_print() for card_obj in table_cards]

    # печать карт компа
    print(f"{blue_bold_text}{'COMP'.center(delimiter_count, '-')}{clean_text}" + '\n')
    if comp_cards:
        comp_beauty_cards = [card_obj.get_to_print() for card_obj in comp_cards]
        print(f"{italic_text}{' '.join(comp_beauty_cards).center(delimiter_count, ' ')}{clean_text}" + '\n')
    else:
        print(f"{red_italic_text}{'$$$ $$$'.center(delimiter_count, ' ')}{clean_text}" + '\n')

    # печать карт стола
    print(f"{blue_bold_text}{'TABLE'.center(delimiter_count, '-')}{clean_text}" + '\n')
    if table_beauty_cards:
        print(f"{italic_text}{' '.join(table_beauty_cards).center(delimiter_count, ' ')}{clean_text}" + '\n')
    else:
        print()

    # печать карт человека
    print(f"{blue_bold_text}{'HUMAN'.center(delimiter_count, '-')}{clean_text}" + '\n')
    print(f"{italic_text}{' '.join(human_beauty_cards).center(delimiter_count, ' ')}{clean_text}" + '\n')
    print(f"{blue_bold_text}{'-' * delimiter_count}{clean_text}")


# печать названия раунда
def print_round(round_name: str) -> None:
    print('\n\n' + f'{yellow_bold_text}{round_name}{clean_text}' + '\n\n')


def print_invalid_bet() -> None:
    print(f'{red_italic_text}НЕВЕРНАЯ СТАВКА!!!{clean_text}')


# печать фолда компа
def print_comp_fold():
    # печать фолда компа
    fold_message = random_choice(['ПАС', 'ФОЛД', 'СКИДЫВАЮ КАРТЫ'])
    print(f'Ставка компьютера: {red_italic_text}{fold_message}{clean_text}')


def print_money(human_money: int, comp_money: int, bet_money: int):
    print('-' * 65)
    print(
        '|  ' + f'{blue_bold_text}Банк:{clean_text} {str(bet_money).rjust(4, " ")}',
        f'{yellow_bold_text}Мои деньги:{clean_text} {str(human_money).rjust(4, " ")}',
        f'{red_bold_text}Деньги компьютера:{clean_text} {str(comp_money).rjust(4, " ")}' + '  |',
        sep='  |  '
    )
    print('-' * 65)


# def print_winner(human_money: int, comp_money: int, bet_money: int):
#     # список комбинаций
#     combo_name_vocab = {
#         0: 'HIGH CARD',
#         1: 'ONE PAIR',
#         2: 'TWO PAIRS',
#         3: 'THREE OF A KIND',
#         4: 'STRAIGHT',
#         5: 'FLASH',
#         6: 'FULL HOUSE',
#         7: 'FOUR OF A KIND',
#         8: 'STRAIGHT FLASH',
#         9: 'ROYAL FLASH',
#     }
#     print(
#         f'{blue_bold_text}Банк:{clean_text} {str(bet_money)}',
#         f'{yellow_bold_text}мои деньги:{clean_text} {str(human_money)},'
#         f'{red_bold_text}деньги компьютера:{clean_text} {str(comp_money)}',
#         sep=' --- '
#     )
