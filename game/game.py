from typing import List, Tuple
from random import shuffle as random_shuffle

from cards import card
from players import human, comp, table

from outputting.printing import print_table, print_round, print_money


class Game:
    def __init__(self):
        # игровые данные
        self.finished_games = 0
        self.game = True
        self.first_stack = 'human'
        self.general_bet = 0

        # объекты игроков и стола
        self.human = human.Human()
        self.comp = comp.Comp(sleep_time=0.5)
        self.table = table.Table()

        # создание колоды и её перемешивание
        self.card_deck = sum([[{'val': num, 'suit': suit} for num in range(2, 15)] for suit in ['A', 'B', 'C', 'D']], [])
        random_shuffle(self.card_deck)

    # возвращает текущую колоду карт
    def get_card_deck(self) -> List[dict]:
        return self.card_deck

    # удаление карты из колоды
    def remove_card_form_deck(self, dealt_card: dict) -> None:
        self.card_deck.remove(dealt_card)

    # раздача новой карты
    def dealing(self, whose_card: str) -> None:
        dict_whose_card = {
            'human': self.human,
            'comp': self.comp,
            'table': self.table,
        }

        first_card_from_deck = self.card_deck[0]
        # создание объекта, добавление его в нужный список
        new_card = card.Card(first_card_from_deck=first_card_from_deck)
        dict_whose_card[whose_card].add_card(new_card=new_card)
        # удаление разданной карты из колоды
        Game.remove_card_form_deck(self, dealt_card=first_card_from_deck)

    def do_bets(self, winner, human_cards, comp_cards) -> None:
        if self.first_stack == 'human':
            # ставка человека
            self.human.bet(comp=self.comp)

        # ставка компа
        self.comp.bet(human=self.human, winner=winner, human_combo=human_cards, comp_combo=comp_cards)

        if self.first_stack == 'comp':
            # ставка человека
            self.human.bet(comp=self.comp)

        # пока не выполняется равенство ставок или фолд
        while not (self.comp.cur_bet == self.human.cur_bet or 'fold' in [self.human.bet_status, self.comp.bet_status]):
            if self.first_stack == 'human':
                # ставка человека
                self.human.bet(comp=self.comp)

            # проверка на равенство ставок или фолд
            if self.comp.cur_bet == self.human.cur_bet or 'fold' in [self.human.bet_status, self.comp.bet_status]:
                break
            # ставка компа
            self.comp.bet(human=self.human, winner=winner, human_combo=human_cards, comp_combo=comp_cards)

            if self.first_stack == 'comp':
                # ставка человека
                self.human.bet(comp=self.comp)

    def winner_definition(self) -> Tuple[str, Tuple[int, list], Tuple[int, list]]:
        best_human = None
        best_comp = None
        # human/comp/draw
        winner = None

        # словари со всеми комбинациями
        human_combo = self.human.combo_definition(table=self.table.cards)
        comp_combo = self.comp.combo_definition(table=self.table.cards)

        # собираем в списки все найденные комбинации
        human_combos = [(num, human_combo[num]) for num in range(9, -1, -1) if human_combo[num]]
        comp_combos = [(num, comp_combo[num]) for num in range(9, -1, -1) if comp_combo[num]]

        for i in range(min(len(human_combos), len(comp_combos))):
            # для выхода из внешнего цикла через внутренний
            outer_break = False

            cur_human_combo, cur_comp_combo = human_combos[i], comp_combos[i]
            # проверка разницы комбинаций
            if cur_human_combo[0] != cur_comp_combo[0]:
                best_human, best_comp = cur_human_combo, cur_comp_combo
                winner = 'human' if cur_human_combo[0] > cur_comp_combo[0] else 'comp'
                break

            # проверка разницы карт в одинаковых комбинациях
            for inner_i in range(len(cur_human_combo[1]) - 1, -1, -1):
                human_card_val, comp_card_val = cur_human_combo[1][inner_i]['val'], cur_comp_combo[1][inner_i]['val']
                if human_card_val != comp_card_val:
                    best_human, best_comp = cur_human_combo, cur_comp_combo
                    winner = 'human' if human_card_val > comp_card_val else 'comp'
                    outer_break = True
                    break

            if outer_break:
                break

        # если победитель не определился
        if not winner:
            winner = 'draw'
            best_human, best_comp = human_combos[-1], comp_combos[-1]

        return winner, best_human, best_comp

    def preflop_round(self):
        # раздача карт
        Game.dealing(self, whose_card='human')
        Game.dealing(self, whose_card='comp')
        Game.dealing(self, whose_card='human')
        Game.dealing(self, whose_card='comp')

        # печать стола и рук игроков
        print_table(human_cards=self.human.cards, table_cards=self.table.cards)

        # определение комбинаций и победителя на данном этапе
        winner, human_cards, comp_cards = Game.winner_definition(self)

        # ставки
        Game.do_bets(self, winner=winner, human_cards=human_cards, comp_cards=comp_cards)

        print('\nHuman', self.human.cur_bet, self.human.bet_status)
        print('Comp', self.comp.cur_bet, self.comp.bet_status)

        # общий банк ставок
        self.general_bet += self.comp.cur_bet + self.human.cur_bet
        # вычет текущих ставок игроков из их кол-ва денег и обнуление их текущих ставок
        self.human.del_bet_from_money()
        self.comp.del_bet_from_money()
        # печать денег и ставок
        print_money(human_money=self.human.money, comp_money=self.comp.money, bet_money=self.general_bet)

    def flop_round(self):
        Game.dealing(self, whose_card='table')
        Game.dealing(self, whose_card='table')
        Game.dealing(self, whose_card='table')

    def tern_round(self):
        Game.dealing(self, whose_card='table')

    def river_round(self):
        Game.dealing(self, whose_card='table')

    def showdown_round(self):
        pass

    # запуск игры
    def start(self):
        if self.game:
            print_round(round_name='PREFLOP')
            Game.preflop_round(self)
            # print_round(round_name='FLOP')
            # Game.flop_round(self)
            # print_round(round_name='TERN')
            # Game.tern_round(self)
            # print_round(round_name='RIVER')
            # Game.river_round(self)
            # print_round(round_name='SHOWDOWN')
            # Game.showdown_round(self)
