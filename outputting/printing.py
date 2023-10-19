from typing import List
from cards.card import Card

from outputting.text_styles import yellow_bold_text, clean_text, blue_bold_text, italic_text, red_italic_text


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
    print(f"{blue_bold_text}{'TABLE'.center(delimiter_count, '-')}\033[0m" + '\n')
    if table_beauty_cards:
        print(f"{italic_text}{' '.join(table_beauty_cards).center(delimiter_count, ' ')}{clean_text}" + '\n')
    else:
        print()

    # печать карт человека
    print(f"{blue_bold_text}{'HUMAN'.center(delimiter_count, '-')}\033[0m" + '\n')
    print(f"{italic_text}{' '.join(human_beauty_cards).center(delimiter_count, ' ')}{clean_text}" + '\n')
    print(f"\033[1m\033[34m{'-' * delimiter_count}\033[0m")


# печать названия раунда
def print_round(round_name: str) -> None:
    print('\n\n' + f'{yellow_bold_text}{round_name}{clean_text}' + '\n\n')


def print_money():
    pass
