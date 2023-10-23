from random import randint
from typing import Tuple

from players.player import Player


class Comp(Player):
    def __init__(self):
        super().__init__()

    def bet(self, human_bet: int, winner: str, human_combo: Tuple[int, list], comp_combo: Tuple[int, list]) -> Tuple[int, str]:
        # in_game/fold/all_in
        in_game_state = 'in_game'
        adding_money = 0

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
                in_game_state = 'fold'

        if adding_money >= 10:
            # делаем разброс значений для добавления к ставке человека и берём рандомное число оттуда
            new_comp_bet = human_bet + abs(randint(adding_money - 10, adding_money + 10))
        else:
            new_comp_bet = human_bet + adding_money

        # если итоговая ставка компа превышает его кол-во денег, то снижаем ставку до его кол-ва денег
        if new_comp_bet >= self.money:
            in_game_state = 'all_in'
            new_comp_bet = self.money

        self.cur_bet = new_comp_bet
        return new_comp_bet, in_game_state
