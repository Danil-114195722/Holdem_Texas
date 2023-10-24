from random import choice as random_choice

from cards.card import Card
from outputting.text_styles import yellow_bold_text, clean_text, blue_bold_text, italic_text, red_italic_text, red_bold_text


# печать подсказки с правилами игры при запуске проги
def print_help() -> None:
    help_text = f'''
{yellow_bold_text}Игра - Техасский Холдем (классический покер){clean_text}

Раздаётся по 2 карты ВАМ и компьютеру.
На стол в общем выкладывается 5 карт.

В первый раунд выкладывается 3 карты.
Делаются начальные ставки (малый и большой блайнд), 
от них нельзя отказаться.

В последующих трёх раундах выкладывается по 1 карте и делаются ставки.

В последнем раунде открываются карты,
определяется победитель и распределяются деньги из банка

{yellow_bold_text}!!!{clean_text}
Чтобы выйти из раунда досрочно (фолд),
введите "пас" "фолд" или "fold" (не зависит от регистра).

{yellow_bold_text}!!!{clean_text}
Игра длится до того момента (если её принудительно не закончить раньше),
пока у одного из игроков не останется денег
'''

    print(help_text)
    input('Continue? [Enter] ')


# печать карт игроков и стола
def print_table(human_cards: list[Card], table_cards: list[Card], comp_cards: list[Card] = None) -> None:
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
    print()


# печать названия раунда
def print_round(round_name: str) -> None:
    print('\n' + f'{yellow_bold_text}{round_name}{clean_text}' + '\n')


def print_invalid_bet() -> None:
    print(f'{red_italic_text}НЕВЕРНАЯ СТАВКА!!!{clean_text}')


# печать фолда компа
def print_comp_fold() -> None:
    # печать фолда компа
    fold_message = random_choice(['ПАС', 'ФОЛД', 'СКИДЫВАЮ КАРТЫ'])
    print(f'Ставка компьютера: {red_italic_text}{fold_message}{clean_text}')


def print_money(human_money: int, comp_money: int, bet_money: int) -> None:
    print('-' * 65)
    print(
        '|  ' + f'{blue_bold_text}Банк:{clean_text} {str(bet_money).rjust(4, " ")}',
        f'{yellow_bold_text}Мои деньги:{clean_text} {str(human_money).rjust(4, " ")}',
        f'{red_bold_text}Деньги компьютера:{clean_text} {str(comp_money).rjust(4, " ")}' + '  |',
        sep='  |  '
    )
    print('-' * 65)


def print_winner(winner: str, human_cards: tuple[int, list], comp_cards: tuple[int, list]) -> None:
    # список комбинаций
    combo_name_vocab = {
        0: 'HIGH CARD',
        1: 'ONE PAIR',
        2: 'TWO PAIRS',
        3: 'THREE OF A KIND',
        4: 'STRAIGHT',
        5: 'FLASH',
        6: 'FULL HOUSE',
        7: 'FOUR OF A KIND',
        8: 'STRAIGHT FLASH',
        9: 'ROYAL FLASH',
    }

    # подготовка названия комбинации и карт человека к выводу
    human_combo_name = combo_name_vocab[human_cards[0]]
    human_combo_cards_to_print = [Card(card_code=card_code).get_to_print() for card_code in human_cards[1]]

    # подготовка названия комбинации и карт компа к выводу
    comp_combo_name = combo_name_vocab[comp_cards[0]]
    comp_combo_cards_to_print = [Card(card_code=card_code).get_to_print() for card_code in comp_cards[1]]

    print()
    print(
        f'{blue_bold_text}WINNER:',
        f'{yellow_bold_text if winner == "human" else red_bold_text}{winner.upper()}{clean_text}'
    )
    print('-' * 66)
    print(
        '|  ' + f'{yellow_bold_text}HUMAN{clean_text}',
        f'{yellow_bold_text}{human_combo_name.center(15, " ")}{clean_text}',
        " ".join(human_combo_cards_to_print).center(30, ' ') + '  |',
        sep='  |  '
    )
    print('-' * 66)
    print(
        f'|  {red_bold_text}' + f'{red_bold_text}COMP {clean_text}',
        f'{red_bold_text}{comp_combo_name.center(15, " ")}{clean_text}',
        " ".join(comp_combo_cards_to_print).center(30, ' ') + '  |',
        sep='  |  '
    )
    print('-' * 66)


def print_winner_if_fold(winner: str, human_status: str, comp_status: str) -> None:
    human_status_too_print = 'IN GAME' if human_status in ['in_game', 'all_in'] else 'FOLD'
    comp_status_too_print = 'IN GAME' if comp_status in ['in_game', 'all_in'] else 'FOLD'

    print()
    print(
        f'{blue_bold_text}WINNER:',
        f'{yellow_bold_text if winner == "human" else red_bold_text}{winner.upper()}{clean_text}'
    )
    print('-' * 24)
    print(
        '|  ' + f'{yellow_bold_text}HUMAN{clean_text}',
        f'{yellow_bold_text}{human_status_too_print.center(8, " ")}{clean_text}' + '  |',
        sep='  |  '
    )
    print('-' * 24)
    print(
        f'|  {red_bold_text}' + f'{red_bold_text}COMP {clean_text}',
        f'{red_bold_text}{comp_status_too_print.center(8, " ")}{clean_text}' + '  |',
        sep='  |  '
    )
    print('-' * 24)
