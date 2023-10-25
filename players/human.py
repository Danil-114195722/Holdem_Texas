from players.player import Player

from outputting.printing import print_invalid_bet
from outputting.text_styles import yellow_bold_text, clean_text


class Human(Player):
    def __init__(self):
        super().__init__()

    # сделать ставку (comp: object players.comp.Comp)
    def bet(self, comp) -> None:
        # in_game/fold/all_in
        self.bet_status = 'in_game'

        # если у компа фолд, то не повышаем ставку человека
        if comp.bet_status == 'fold':
            return {'bet': self.cur_bet, 'status': 'in_game'}

        while True:
            try:
                # ставка человека (кроме числа может быть "пас" или "fold")
                new_human_bet_row = input(f'{yellow_bold_text}Ваша ставка: {clean_text}')
                self.cur_bet = int(new_human_bet_row)
                # если ставка человека меньше ставки компа или больше чем общее кол-во денег человека
                if not (comp.cur_bet <= self.cur_bet <= self.money or comp.bet_status == 'all_in'):
                    raise ValueError('int not in range')
                break

            except ValueError:
                # если фолд
                if new_human_bet_row.lower() in ['пас', 'фолд', 'fold']:
                    self.bet_status = 'fold'
                    break
                else:
                    print_invalid_bet()

        # если ставка равна кол-ву всех денег человека
        if self.cur_bet == self.money:
            self.bet_status = 'all_in'

        return {'bet': self.cur_bet, 'status': self.bet_status}
