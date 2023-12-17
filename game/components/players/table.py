from game.components.players.player import Player


class Table(Player):
    def __init__(self, all_money: int):
        super().__init__(all_money=all_money)
