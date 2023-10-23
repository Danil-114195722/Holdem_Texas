from players.player import Player

from outputting.printing import print_invalid_bet


class Human(Player):
    def __init__(self):
        super().__init__()

    # сделать ставку
    def bet(self, comp_bet: int) -> int:
        # in_game/fold/all_in
        in_game_state = 'in_game'
        new_human_bet = self.cur_bet

        while True:
            try:
                # ставка человека (кроме числа может быть "пас" или "fold")
                new_human_bet_row = input('Ваша ставка: ')
                new_human_bet = int(new_human_bet_row)
                # если ставка человека меньше ставки компа или больше чем общее кол-во денег человека
                if not (comp_bet <= new_human_bet <= self.money):
                    raise ValueError('int not in range')
                break

            except ValueError:
                # если фолд
                if new_human_bet_row in ['пас', 'fold']:
                    in_game_state = 'fold'
                    break
                else:
                    print_invalid_bet()

        # если ставка равна кол-ву всех денег человека
        if new_human_bet == self.money:
            in_game_state = 'all_in'

        self.cur_bet = new_human_bet
        return new_human_bet, in_game_state
