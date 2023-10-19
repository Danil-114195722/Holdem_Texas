from typing import List

from cards.card import Card
from combinations import combo_define


class Player:
    def __init__(self):
        self.cards = []

    def add_card(self, new_card: object):
        self.cards.append(new_card)

    def get_money_info(self):
        pass

    # определение комбинации игрока
    def combo_definition(self, table: List[Card]) -> dict:
        # список объектов
        mix_cards = self.cards + table
        # отсортированный список словарей карт
        mix_cards_vocab = sorted([calc_card.get_to_calc() for calc_card in mix_cards], key=lambda elem: elem['val'])

        # mix_cards_vocab = [
        #     {'val': 2, 'suit': 'C'},
        #     {'val': 9, 'suit': 'C'},
        #     {'val': 10, 'suit': 'C'},
        #     {'val': 11, 'suit': 'C'},
        #     {'val': 12, 'suit': 'C'},
        #     {'val': 13, 'suit': 'C'},
        #     {'val': 14, 'suit': 'C'},
        # ]

        all_same_cards = combo_define.pairs(card_list=mix_cards_vocab)
        flash_cards = combo_define.flash(card_list=mix_cards_vocab)
        straight_flash_cards = combo_define.straight_flash(flash_list=flash_cards)

        combo_dict = {
            0: sorted([calc_card.get_to_calc() for calc_card in self.cards], key=lambda elem: elem['val']),
            1: combo_define.one_pair(all_pairs=all_same_cards),
            2: combo_define.two_pairs(all_pairs=all_same_cards),
            3: combo_define.three_of_a_kind(all_pairs=all_same_cards),
            4: combo_define.straight(card_list=mix_cards_vocab),
            5: flash_cards,
            6: combo_define.full_house(all_pairs=all_same_cards),
            7: combo_define.four_of_a_kind(all_pairs=all_same_cards),
            8: straight_flash_cards,
            9: combo_define.royal_flash(straight_flash_list=straight_flash_cards),
        }

        return combo_dict
