from typing import List
from random import shuffle

from cards import card
from players import human, comp, table


class Game:
    def __init__(self):
        # игровые данные
        self.finished_games = 0
        self.game = True

        # объекты игроков и стола
        self.human = human.Human()
        self.comp = comp.Comp()
        self.table = table.Table()

        # создание колоды и её перемешивание
        self.card_deck = sum([[{'val': num, 'suit': suit} for num in range(2, 15)] for suit in ['A', 'B', 'C', 'D']], [])
        shuffle(self.card_deck)

    # возвращает текущую колоду карт
    def get_card_deck(self) -> List[dict]:
        return self.card_deck

    # удаление карты из колоды
    def remove_card_form_deck(self, dealt_card: dict):
        self.card_deck.remove(dealt_card)

    def print_table(self, show_comp: bool = False):
        # кол-во разделителя
        delimiter_count = 30

        human_beauty_cards = [card_obj.get_to_print() for card_obj in self.human.cards]
        table_beauty_cards = [card_obj.get_to_print() for card_obj in self.table.cards]

        # стили текста
        blue_bold_text = "\033[1m\033[34m"
        italic_text = "\033[3m"
        red_italic_text = "\033[3m\033[31m"
        clean_text = "\033[0m"

        # печать карт компа
        print(f"{blue_bold_text}{'COMP'.center(delimiter_count, '-')}{clean_text}" + '\n')
        if show_comp:
            comp_beauty_cards = [card_obj.get_to_print() for card_obj in self.comp.cards]
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

    def print_money(self):
        pass

    # раздача новой карты
    def dealing(self, whose_card: str):
        dict_whose_card = {
            'human': self.human,
            'comp': self.comp,
            'table': self.table,
        }

        # создание объекта, добавление его в нужный список
        new_card = card.Card(card_deck=self.card_deck)
        dict_whose_card[whose_card].add_card(new_card=new_card)
        # удаление разданной карты из колоды
        Game.remove_card_form_deck(self, dealt_card=new_card.get_to_calc())

    def preflop_round(self):
        Game.dealing(self, whose_card='human')
        Game.dealing(self, whose_card='comp')
        Game.dealing(self, whose_card='human')
        Game.dealing(self, whose_card='comp')

        # Game.print_table(self)

    def flop_round(self):
        Game.dealing(self, whose_card='table')
        Game.dealing(self, whose_card='table')
        Game.dealing(self, whose_card='table')

        # Game.print_table(self)

    def tern_round(self):
        Game.dealing(self, whose_card='table')

        # Game.print_table(self)

    def river_round(self):
        Game.dealing(self, whose_card='table')

        # Game.print_table(self)

    def showdown_round(self):
        Game.print_table(self, show_comp=True)
        self.human.combo_definition(table=self.table.cards)

    # запуск игры
    def start(self):
        if self.game:
            # стили текста
            yellow_bold_text = "\033[1m\033[33m"
            clean_text = "\033[0m"

            print('\n\n' + f'{yellow_bold_text}PREFLOP{clean_text}' + '\n\n')
            Game.preflop_round(self)
            print('\n\n' + f'{yellow_bold_text}FLOP{clean_text}' + '\n\n')
            Game.flop_round(self)
            print('\n\n' + f'{yellow_bold_text}TERN{clean_text}' + '\n\n')
            Game.tern_round(self)
            print('\n\n' + f'{yellow_bold_text}RIVER{clean_text}' + '\n\n')
            Game.river_round(self)
            print('\n\n' + f'{yellow_bold_text}SHOWDOWN{clean_text}' + '\n\n')
            Game.showdown_round(self)
