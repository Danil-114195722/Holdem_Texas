from typing import List

from cards.card import Card
from combinations import combo_define


class Player:
    # список комбинаций
    combo_name_vocab = {
        0: 'high_card',
        1: 'one_pair',
        2: 'two_pairs',
        3: 'three_of_a_kind',
        4: 'straight',
        5: 'flash',
        6: 'full_house',
        7: 'four_of_a_kind',
        8: 'straight_flash',
        9: 'royal_flash',
    }

    def __init__(self):
        self.cards = []

    def add_card(self, new_card: object):
        self.cards.append(new_card)

    def get_money_info(self):
        pass

    # определение комбинации игрока
    def combo_definition(self, table: List[Card]):
        # список объектов
        mix_cards = self.cards + table
        # список словарей
        mix_cards_vocab = [calc_card.get_to_calc() for calc_card in mix_cards]

        combo_define.check_all_combo(mix_card=mix_cards_vocab)
