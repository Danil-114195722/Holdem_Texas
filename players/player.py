from typing import List

from cards.card import Card
from combinations import combo_define


class Player:
    def __init__(self):
        self.cards = []
        self.money = 1000
        self.cur_bet = 0
        # in_game/fold/all_in
        self.bet_status = 'in_game'

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

        # все пары, сеты и каре
        all_same_cards = combo_define.pairs(card_list=mix_cards_vocab)
        # все карты одинаковой масти
        flash_cards = combo_define.flash(card_list=mix_cards_vocab)
        # все карты одинаковой масти по порядку
        straight_flash_cards = combo_define.straight_flash(flash_list=flash_cards)

        combo_dict = {
            # старшая карта
            0: sorted([calc_card.get_to_calc() for calc_card in self.cards], key=lambda elem: elem['val']),
            # одна пара
            1: combo_define.one_pair(all_pairs=all_same_cards),
            # две пары
            2: combo_define.two_pairs(all_pairs=all_same_cards),
            # сет
            3: combo_define.three_of_a_kind(all_pairs=all_same_cards),
            # стрит
            4: combo_define.straight(card_list=mix_cards_vocab),
            # флеш
            5: flash_cards,
            # фулл хаус
            6: combo_define.full_house(all_pairs=all_same_cards),
            # каре
            7: combo_define.four_of_a_kind(all_pairs=all_same_cards),
            # стрит флеш
            8: straight_flash_cards,
            # роял флеш
            9: combo_define.royal_flash(straight_flash_list=straight_flash_cards),
        }

        return combo_dict
