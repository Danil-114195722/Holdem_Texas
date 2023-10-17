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
        # список словарей карт
        mix_cards_vocab = [calc_card.get_to_calc() for calc_card in mix_cards]

        high_cards = sorted([calc_card.get_to_calc() for calc_card in self.cards], key=lambda elem: elem['val'])
        ps_cards = combo_define.pairs(card_list=mix_cards_vocab)
        op_cards = combo_define.one_pair(all_pairs=ps_cards)
        tp_cards = combo_define.two_pairs(all_pairs=ps_cards)
        st_cards = combo_define.three_of_a_kind(all_pairs=ps_cards)
        fh_cards = combo_define.full_house(all_pairs=ps_cards)
        fk_cards = combo_define.four_of_a_kind(all_pairs=ps_cards)
        s_cards = combo_define.straight(card_list=mix_cards_vocab)
        f_cards = combo_define.flash(card_list=mix_cards_vocab)
        sf_cards = combo_define.straight_flash(flash_list=f_cards)
        rf_cards = combo_define.royal_flash(flash_list=f_cards, straight_flash_list=sf_cards)

        print('high_card:', high_cards)
        print('one_pair:', op_cards)
        print('two_pairs:', tp_cards)
        print('three_of_a_kind:', st_cards)
        print('full_house:', fh_cards)
        print('four_of_a_kind:', fk_cards)
        print('straight:', s_cards)
        print('flash:', f_cards)
        print('straight_flash:', sf_cards)
        print('royal_flash:', rf_cards)
