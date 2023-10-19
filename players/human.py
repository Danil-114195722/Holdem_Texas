from players.player import Player

from outputting.printing import print_invalid_bet


class Human(Player):
    def __init__(self):
        super().__init__()

    # сделать ставку
    def bet(self, comp_bet: int) -> int:
        while True:
            try:
                cur_human_bet = int(input('Ваша ставка: '))
                if not (comp_bet <= cur_human_bet <= self.money):
                    raise ValueError('int not in range')
                break
            except ValueError:
                print_invalid_bet()

        return cur_human_bet
