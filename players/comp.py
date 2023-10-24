from time import sleep
from random import randint
from typing import Tuple

from players.player import Player
from outputting.printing import print_comp_fold


class Comp(Player):
    def __init__(self, sleep_time):
        super().__init__()
        # время сна перед ставкой компа
        self.sleep_time = sleep_time

    # сделать ставку компа (human: object players.human.Human)
    def bet(self, human, winner: str, human_combo: Tuple[int, list], comp_combo: Tuple[int, list]) -> None:
        sleep(self.sleep_time)
        adding_money = 0

        # если у человека фолд, то не повышаем ставку компа
        if human.bet_status == 'fold':
            self.bet_status = 'in_game'
            return
        # если у человека олл ин
        elif human.bet_status == 'all_in':
            self.cur_bet = self.money if human.cur_bet > self.money else human.cur_bet
            self.bet_status = 'in_game'
            return

        # номер комбинации человека и компа
        num_com_h, num_com_c = human_combo[0], comp_combo[0]

        # прямо пропорц. разнице номеров комбинаций, ЕСЛИ номер комбинации компа больше номера комбинации человека
        if num_com_c > num_com_h:
            adding_money += 10 * (num_com_c - num_com_h)
        # блеф (70% всех денег) с вероятностью 5%, ЕСЛИ номер комбинации человека больше номера комбинации компа
        elif num_com_h > num_com_c and randint(0, 99) >= 95:
            adding_money += self.money * 0.7
        # номер комбинации компа равен номеру комбинации человека
        else:
            if winner == 'comp' and randint(0, 1):
                adding_money += 10
            elif winner == 'draw' and randint(0, 9) >= 8:
                adding_money += 5
            elif winner == 'human' and randint(0, 9) >= 8:
                self.bet_status = 'fold'
                # печать фолда компа
                print_comp_fold()
                return

        if adding_money >= 10:
            # делаем разброс значений для добавления к ставке человека и берём рандомное число оттуда
            self.cur_bet = human.cur_bet + abs(randint(adding_money - 10, adding_money + 10))
        else:
            self.cur_bet = human.cur_bet + adding_money

        # если итоговая ставка компа превышает его кол-во денег, то снижаем ставку до его кол-ва денег
        if self.cur_bet >= self.money and self.bet_status != 'fold':
            self.bet_status = 'all_in'
            self.cur_bet = self.money

        # печать ставки компа
        print(f'Ставка компьютера: {self.cur_bet}')
