from math import floor as round_down
from time import sleep
from random import shuffle as random_shuffle

from cards import card
from players import human, comp, table

from outputting.printing import print_table, print_round, print_money, print_winner, print_winner_if_fold
from outputting.text_styles import yellow_bold_text, clean_text


class Game:
    def __init__(self):
        # игровые данные
        self.finished_games = 0
        self.continue_game = 'yes'
        self.first_stack = 'human'
        self.general_bet = 0

        # объекты игроков и стола
        self.human = human.Human()
        self.comp = comp.Comp(sleep_time=0.25)
        self.table = table.Table()

        # создание колоды и её перемешивание
        self.card_deck = sum([[{'val': num, 'suit': suit} for num in range(2, 15)] for suit in ['A', 'B', 'C', 'D']], [])
        random_shuffle(self.card_deck)

    # возвращает текущую колоду карт
    def get_card_deck(self) -> list[dict]:
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
        new_card = card.Card(card_code=first_card_from_deck)
        dict_whose_card[whose_card].add_card(new_card=new_card)
        # удаление разданной карты из колоды
        Game.remove_card_form_deck(self, dealt_card=first_card_from_deck)

    def do_bets(self, winner: str, human_cards:  tuple[int, list], comp_cards:  tuple[int, list]) -> None:
        if self.first_stack == 'human':
            # ставка человека
            self.human.bet(comp=self.comp)
            # проверка на фолд
            if 'fold' in [self.human.bet_status, self.comp.bet_status]:
                return

            # ставка компа
            self.comp.bet(human=self.human, winner=winner, human_combo=human_cards, comp_combo=comp_cards)
            # проверка на равенство ставок/фолд и олл ин
            if (self.comp.cur_bet == self.human.cur_bet or
                    'fold' in [self.human.bet_status, self.comp.bet_status]):
                return
            elif self.comp.bet_status == 'all_in':
                if self.human.cur_bet < self.comp.cur_bet:
                    # ставка человека
                    self.human.bet(comp=self.comp)
                return

        else:
            # ставка компа
            self.comp.bet(human=self.human, winner=winner, human_combo=human_cards, comp_combo=comp_cards)
            # проверка на фолд
            if 'fold' in [self.human.bet_status, self.comp.bet_status]:
                return

            # ставка человека
            self.human.bet(comp=self.comp)
            # проверка на равенство ставок/фолд и олл ин
            if (self.comp.cur_bet == self.human.cur_bet or
                    'fold' in [self.human.bet_status, self.comp.bet_status]):
                return
            elif self.human.bet_status == 'all_in':
                if self.human.cur_bet > self.comp.cur_bet:
                    # ставка компа
                    self.comp.bet(human=self.human, winner=winner, human_combo=human_cards, comp_combo=comp_cards)
                return

        # пока не выполняется равенство ставок или фолд
        while True:

            # if 0 in [(self.human.money - self.human.cur_bet), (self.comp.money - self.comp.cur_bet)]:
            #     break

            if self.first_stack == 'human':
                # ставка человека
                self.human.bet(comp=self.comp)
                # проверка на равенство ставок/фолд и олл ин
                if (self.comp.cur_bet == self.human.cur_bet or
                        'fold' in [self.human.bet_status, self.comp.bet_status]):
                    break
                elif self.human.bet_status == 'all_in':
                    if self.human.cur_bet > self.comp.cur_bet:
                        # ставка компа
                        self.comp.bet(human=self.human, winner=winner, human_combo=human_cards, comp_combo=comp_cards)
                    break

                # ставка компа
                self.comp.bet(human=self.human, winner=winner, human_combo=human_cards, comp_combo=comp_cards)
                # проверка на равенство ставок/фолд и олл ин
                if (self.comp.cur_bet == self.human.cur_bet or
                        'fold' in [self.human.bet_status, self.comp.bet_status]):
                    break
                elif self.comp.bet_status == 'all_in':
                    if self.human.cur_bet < self.comp.cur_bet:
                        # ставка человека
                        self.human.bet(comp=self.comp)
                    break
            else:
                # ставка компа
                self.comp.bet(human=self.human, winner=winner, human_combo=human_cards, comp_combo=comp_cards)
                # проверка на равенство ставок/фолд и олл ин
                if (self.comp.cur_bet == self.human.cur_bet or
                        'fold' in [self.human.bet_status, self.comp.bet_status]):
                    break
                elif self.comp.bet_status == 'all_in':
                    if self.human.cur_bet < self.comp.cur_bet:
                        # ставка человека
                        self.human.bet(comp=self.comp)
                    break

                # ставка человека
                self.human.bet(comp=self.comp)
                # проверка на равенство ставок/фолд и олл ин
                if (self.comp.cur_bet == self.human.cur_bet or
                        'fold' in [self.human.bet_status, self.comp.bet_status]):
                    break
                elif self.human.bet_status == 'all_in':
                    if self.human.cur_bet > self.comp.cur_bet:
                        # ставка компа
                        self.comp.bet(human=self.human, winner=winner, human_combo=human_cards, comp_combo=comp_cards)
                    break

    def winner_definition(self) -> tuple[str, tuple[int, list], tuple[int, list]]:
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
        # раздача карт игрокам
        Game.dealing(self, whose_card='human')
        Game.dealing(self, whose_card='comp')
        Game.dealing(self, whose_card='human')
        Game.dealing(self, whose_card='comp')

        # печать названия раунда
        print_round(round_name='PREFLOP')

        # печать стола и рук игроков
        print_table(human_cards=self.human.cards, table_cards=self.table.cards)
        sleep(0.5)

        # определение комбинаций и победителя на данном этапе
        winner, human_cards, comp_cards = Game.winner_definition(self)

        # малый и большой блайнд
        if self.first_stack == 'human':
            self.human.cur_bet = 3
            print(f'{yellow_bold_text}Малый блайнд (ВЫ): {clean_text}{self.human.cur_bet}')
            sleep(0.25)
            self.comp.cur_bet = 6
            print(f'Большой блайнд (компьютер): {self.comp.cur_bet}')
        else:
            self.comp.cur_bet = 3
            print(f'Малый блайнд (компьютер): {self.comp.cur_bet}')
            sleep(0.25)
            self.human.cur_bet = 6
            print(f'{yellow_bold_text}Большой блайнд (ВЫ): {clean_text}{self.human.cur_bet}')
        sleep(0.25)
        # ставки
        Game.do_bets(self, winner=winner, human_cards=human_cards, comp_cards=comp_cards)
        print()
        sleep(0.5)

        # общий банк ставок
        self.general_bet += self.comp.cur_bet + self.human.cur_bet
        # вычет текущих ставок игроков из их кол-ва денег и обнуление их текущих ставок
        self.human.del_bet_from_money()
        self.comp.del_bet_from_money()
        # печать денег игроков и банка
        print_money(human_money=self.human.money, comp_money=self.comp.money, bet_money=self.general_bet)

    def flop_round(self):
        # раздача карт на стол
        Game.dealing(self, whose_card='table')
        Game.dealing(self, whose_card='table')
        Game.dealing(self, whose_card='table')

        if ('fold' in [self.human.bet_status, self.comp.bet_status] or
                'all_in' in [self.human.bet_status, self.comp.bet_status]):
            return

        # печать названия раунда
        print_round(round_name='FLOP')

        # печать стола и рук игроков
        print_table(human_cards=self.human.cards, table_cards=self.table.cards)
        sleep(0.5)

        # определение комбинаций и победителя на данном этапе
        winner, human_cards, comp_cards = Game.winner_definition(self)

        # ставки
        Game.do_bets(self, winner=winner, human_cards=human_cards, comp_cards=comp_cards)
        print()
        sleep(0.5)

        # общий банк ставок
        self.general_bet += self.comp.cur_bet + self.human.cur_bet
        # вычет текущих ставок игроков из их кол-ва денег и обнуление их текущих ставок
        self.human.del_bet_from_money()
        self.comp.del_bet_from_money()
        # печать денег игроков и банка
        print_money(human_money=self.human.money, comp_money=self.comp.money, bet_money=self.general_bet)

    def tern_round(self):
        # раздача карты на стол
        Game.dealing(self, whose_card='table')

        if ('fold' in [self.human.bet_status, self.comp.bet_status] or
                'all_in' in [self.human.bet_status, self.comp.bet_status]):
            return

        # печать названия раунда
        print_round(round_name='TERN')

        # печать стола и рук игроков
        print_table(human_cards=self.human.cards, table_cards=self.table.cards)
        sleep(0.5)

        # определение комбинаций и победителя на данном этапе
        winner, human_cards, comp_cards = Game.winner_definition(self)

        # ставки
        Game.do_bets(self, winner=winner, human_cards=human_cards, comp_cards=comp_cards)
        print()
        sleep(0.5)

        # общий банк ставок
        self.general_bet += self.comp.cur_bet + self.human.cur_bet
        # вычет текущих ставок игроков из их кол-ва денег и обнуление их текущих ставок
        self.human.del_bet_from_money()
        self.comp.del_bet_from_money()
        # печать денег игроков и банка
        print_money(human_money=self.human.money, comp_money=self.comp.money, bet_money=self.general_bet)

    def river_round(self):
        # раздача карты на стол
        Game.dealing(self, whose_card='table')

        if ('fold' in [self.human.bet_status, self.comp.bet_status] or
                'all_in' in [self.human.bet_status, self.comp.bet_status]):
            return

        # печать названия раунда
        print_round(round_name='RIVER')

        # печать стола и рук игроков
        print_table(human_cards=self.human.cards, table_cards=self.table.cards)
        sleep(0.5)

        # определение комбинаций и победителя на данном этапе
        winner, human_cards, comp_cards = Game.winner_definition(self)

        # ставки
        Game.do_bets(self, winner=winner, human_cards=human_cards, comp_cards=comp_cards)
        print()
        sleep(0.5)

        # общий банк ставок
        self.general_bet += self.comp.cur_bet + self.human.cur_bet
        # вычет текущих ставок игроков из их кол-ва денег и обнуление их текущих ставок
        self.human.del_bet_from_money()
        self.comp.del_bet_from_money()
        # печать денег игроков и банка
        print_money(human_money=self.human.money, comp_money=self.comp.money, bet_money=self.general_bet)

    def showdown_round(self):
        # печать названия раунда
        print_round(round_name='SHOWDOWN')
        sleep(0.5)

        # определение комбинаций и победителя на данном этапе
        winner, human_cards, comp_cards = Game.winner_definition(self)

        # если человек пас
        if self.human.bet_status == 'fold':
            winner = 'comp'
            # печать победителя
            print_winner_if_fold(winner=winner, human_status=self.human.bet_status, comp_status=self.comp.bet_status)
        # если комп пас
        elif self.comp.bet_status == 'fold':
            winner = 'human'
            # печать победителя
            print_winner_if_fold(winner=winner, human_status=self.human.bet_status, comp_status=self.comp.bet_status)
        else:
            # печать стола и рук игроков
            print_table(human_cards=self.human.cards, table_cards=self.table.cards, comp_cards=self.comp.cards)
            # печать победителя
            print_winner(winner=winner, human_cards=human_cards, comp_cards=comp_cards)

        # добавляем деньги из банка победителю, обнуляем банк
        if winner == 'human':
            self.human.money += self.general_bet
            self.general_bet = 0
        elif winner == 'comp':
            self.comp.money += self.general_bet
            self.general_bet = 0
        else:
            self.human.money += round_down(self.general_bet / 2)
            self.comp.money += round_down(self.general_bet / 2)
            self.general_bet = 0

        # печать денег игроков
        sleep(1)
        print()
        print_money(human_money=self.human.money, comp_money=self.comp.money, bet_money=self.general_bet)

    # запуск игры

    def start(self) -> int:
        # печать денег игроков
        print()
        print_money(human_money=self.human.money, comp_money=self.comp.money, bet_money=self.general_bet)

        while self.continue_game in ['y', 'yes', 'да', 'д', '']:
            # если есть хотя бы одна завершённая игра
            if self.finished_games:
                # пересоздание колоды и её перемешивание
                self.card_deck = sum(
                    [[{'val': num, 'suit': suit} for num in range(2, 15)] for suit in ['A', 'B', 'C', 'D']], [])
                random_shuffle(self.card_deck)

                # обнуление карт игроков и стола
                self.human.cards = []
                self.comp.cards = []
                self.table.cards = []

                # обнуление статуса ставки игрока
                self.human.bet_status = 'in_game'
                self.comp.bet_status = 'in_game'

            Game.preflop_round(self)
            Game.flop_round(self)
            Game.tern_round(self)
            Game.river_round(self)
            Game.showdown_round(self)

            self.finished_games += 1
            # если у одного из игроков закончились деньги, то завершаем игру
            if not (self.human.money and self.comp.money):
                print('\nИГРА ОКОНЧЕНА')
                break

            sleep(1.5)
            self.continue_game = input('\nПродолжить игру? [y, n] ')
            self.first_stack = 'comp' if self.first_stack == 'human' else 'human'

        return self.finished_games
