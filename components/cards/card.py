class Card:
    to_print = {
        11: 'J',
        12: 'Q',
        13: 'K',
        14: 'A',
        1: 'A',
        'A': '♦️',
        'B': '♥️',
        'C': '♠️',
        'D': '♣️',
    }

    def __init__(self, card_code: dict):
        self.card_code = card_code

    # возвращает карту в красивом виде для вывода
    def get_to_print(self) -> str:
        card_value = self.card_code['val']
        card_suit = self.card_code['suit']
        # использование словаря для замены кода карты на красивый вид
        beauty_view = Card.to_print.get(card_value, str(card_value)) + ' ' + Card.to_print.get(card_suit)

        return beauty_view

    # возвращает карту в виде её кода
    def get_to_calc(self) -> dict:
        return self.card_code
