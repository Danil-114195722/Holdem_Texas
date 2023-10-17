from typing import List, Tuple


# сортировка микса карт
def sort_card_mix(card_mix: List[dict], column: str) -> Tuple[List[dict], List[int]]:
    # сортировка
    mix_sorted = sorted(card_mix, key=lambda elem: elem[column])
    column_sorted = list(map(lambda elem: elem[column], mix_sorted))

    return mix_sorted, column_sorted


def royal_flash(flash_list: List[dict], straight_flash_list: List[dict]) -> List[dict] | None:
    """Определение наличия роял флеша"""
    royal_flash_cards = None

    if not (flash_list and straight_flash_list):
        return royal_flash_cards

    # если среди флеша есть наивысший стрит
    if list(range(10, 15)) == list(map(lambda elem: elem['val'], straight_flash_list)):
        # список с картами роял флеша
        royal_flash_cards = list(filter(lambda elem: elem['val'] in range(10, 15), flash_list))

    return royal_flash_cards


def straight_flash(flash_list: List[dict]) -> List[dict] | None:
    """Определение наличия стрит флеша"""
    straight_flash_cards = None

    if not flash_list:
        return straight_flash_cards

    # разделяем значения флеша по 5 в каждый подсписок
    straight_flash_list = [
        list(map(lambda elem: elem['val'], flash_list))[i - 5:i]
        for i in range(len(flash_list), 0, -1)
        if len(flash_list[i - 5:i]) >= 5
    ]
    # выбираем тот подсписок, который содержит последовательность значений
    straight_in_flash = [elem for elem in straight_flash_list if elem == list(range(elem[0], elem[0] + 5))]

    # если среди флеша есть стрит
    if straight_in_flash:
        first_value = straight_in_flash[0][0]
        # список с картами стрит флеша
        straight_flash_cards = list(filter(
            lambda elem: elem['val'] in range(first_value, first_value + 5),
            flash_list))

    return straight_flash_cards


def flash(card_list: List[dict]) -> List[dict] | None:
    """Определение наличия флеша"""
    flash_cards = None

    # card_list = [
    #     {'val': 13, 'suit': 'A'},
    #     {'val': 14, 'suit': 'C'},
    #     {'val': 7, 'suit': 'C'},
    #     {'val': 6, 'suit': 'C'},
    #     {'val': 6, 'suit': 'B'},
    #     {'val': 5, 'suit': 'C'},
    #     {'val': 11, 'suit': 'C'},
    # ]

    mix_val_sorted, val_sorted = sort_card_mix(card_mix=card_list, column='val')
    mix_suit_sorted, suit_sorted = sort_card_mix(card_mix=card_list, column='suit')

    # разделяем масти с их кол-вом по спискам
    list_by_suit = [
        list(filter(lambda elem: elem == suit_letter, suit_sorted))
        for suit_letter in ['A', 'B', 'C', 'D']
        if suit_letter in suit_sorted
    ]
    # выбираем ту масть, которая содержится в наборе >=5 раз
    one_suit_to_flash = [elem[0] for elem in list_by_suit if len(elem) >= 5 and len(set(elem)) == 1]

    # если какая-то масть содержится в наборе >=5 раз
    if one_suit_to_flash:
        # список с картами флеша
        flash_cards = list(filter(lambda elem: elem['suit'] == one_suit_to_flash[0], mix_val_sorted))

    # print('AAA mix_val_sorted', mix_val_sorted)
    # print('AAA flash_cards', flash_cards)
    return flash_cards


def straight(card_list: List[dict]) -> List[dict] | None:
    """Определение наличия стрита"""
    straight_cards = None

    card_list = card_list.copy()
    # card_list = [
    #     {'val': 5, 'suit': 'C'},
    #     {'val': 6, 'suit': 'A'},
    #     {'val': 5, 'suit': 'B'},
    #     {'val': 5, 'suit': 'B'},
    #     {'val': 7, 'suit': 'B'},
    #     {'val': 4, 'suit': 'D'},
    #     {'val': 3, 'suit': 'B'},
    # ]

    # если есть туз (номер 14), то добавляем номер 1 (для 2 случая туза)
    unsorted_value_list = list(map(lambda elem: elem['val'], card_list))
    if 14 in unsorted_value_list:
        card_list.insert(0, {'val': 1, 'suit': card_list[unsorted_value_list.index(14)]['suit']})

    mix_val_sorted, val_sorted = sort_card_mix(card_mix=card_list, column='val')

    # определяем список без дубликатов и разделяем уникальные значения по 5 в каждый подсписок
    without_dupls = list(set(val_sorted))
    seq_list = [
        without_dupls[i - 5:i]
        for i in range(len(without_dupls), 0, -1)
        if len(without_dupls[i - 5:i]) >= 5
    ]
    # выбираем тот подсписок, который содержит последовательность значений
    straight_list = [elem for elem in seq_list if elem == list(range(elem[0], elem[0] + 5))]

    # если есть стрит
    if straight_list:
        first_value = straight_list[0][0]
        # список с картами стрита
        straight_cards = list(filter(
            lambda elem: elem['val'] in range(first_value, first_value + 5),
            mix_val_sorted))

        # если есть дублирующие карты стрита
        if len(straight_cards) > 5:
            straight_cards = [
                straight_cards[i]
                for i in range(len(straight_cards))
                if straight_cards[i]['val'] != straight_cards[i - 1]['val']
            ]

    return straight_cards


def four_of_a_kind(all_pairs: List[dict]) -> List[dict] | None:
    """Определение наличия каре"""
    four_of_a_kind_cards = None

    if not all_pairs:
        return four_of_a_kind_cards

    val_sorted = list(map(lambda elem: elem['val'], all_pairs))
    # словарь с кол-вом элемента и его индексом в списке val_sorted
    val_count_dict = {
        val_sorted.count(val_sorted[i]): i
        for i in range(len(val_sorted))
        if val_sorted[i] != val_sorted[i - 1]
    }

    # если есть 4 одинаковых значения
    if 4 in [val_sorted.count(uq_elem) for uq_elem in set(val_sorted)]:
        four_of_a_kind_cards = all_pairs[val_count_dict[4]:val_count_dict[4] + 4]

    return four_of_a_kind_cards


def full_house(all_pairs: List[dict]) -> List[dict] | None:
    """Определение наличия фулл хауса"""
    full_house_cards = None

    if not all_pairs:
        return full_house_cards

    # сортировка по кол-ву содержания элемента в списке
    all_pairs_cnt_sort = sorted(
        all_pairs,
        key=lambda elem: list(map(lambda x: x['val'], all_pairs)).count(elem['val'])
    )
    # только значения
    val_sorted = list(map(lambda elem: elem['val'], all_pairs_cnt_sort))

    val_count_list = [
        val_sorted.count(val_sorted[i])
        for i in range(len(val_sorted))
        if val_sorted[i] != val_sorted[i - 1]
    ]

    dict_for_full_house = {
        (2, 3): all_pairs,
        (2, 2, 3): all_pairs_cnt_sort[2:],
        (3, 3): all_pairs_cnt_sort[1:],
    }
    # определение карт фулл хауса по словарю
    full_house_cards = dict_for_full_house.get(tuple(val_count_list), None)

    return full_house_cards


def three_of_a_kind(all_pairs: List[dict]) -> List[dict] | None:
    """Определение наличия сета"""
    three_of_a_kind_cards = None

    if not all_pairs:
        return three_of_a_kind_cards

    # если есть только один сет
    if len(all_pairs) == 3:
        three_of_a_kind_cards = all_pairs

    return three_of_a_kind_cards


def two_pairs(all_pairs: List[dict]) -> List[dict] | None:
    """Определение наличия двух пар"""
    two_pairs_cards = None

    if not all_pairs:
        return two_pairs_cards

    val_sorted = list(map(lambda elem: elem['val'], all_pairs))

    # если есть две/три пары
    if len(all_pairs) >= 4 and set(val_sorted.count(uq_elem) for uq_elem in set(val_sorted)) == {2}:
        # если три пары, то выбираем две наибольшие из них
        if len(all_pairs) == 6:
            two_pairs_cards = all_pairs[2:]
        else:
            two_pairs_cards = all_pairs

    return two_pairs_cards


def one_pair(all_pairs: List[dict]) -> List[dict] | None:
    """Определение наличия пары"""
    one_pair_cards = None

    if not all_pairs:
        return one_pair_cards

    # если есть только одна пара
    if len(all_pairs) == 2:
        one_pair_cards = all_pairs

    return one_pair_cards


def pairs(card_list: List[dict]) -> List[dict] | None:
    """Определение наличия всех пар, сетов и каре"""
    pairs_cards = None

    # card_list = [
    #     {'val': 7, 'suit': 'C'},
    #     {'val': 6, 'suit': 'A'},
    #     {'val': 9, 'suit': 'B'},
    #     {'val': 7, 'suit': 'B'},
    #     {'val': 2, 'suit': 'B'},
    #     {'val': 7, 'suit': 'D'},
    #     {'val': 2, 'suit': 'B'},
    # ]

    mix_val_sorted, val_sorted = sort_card_mix(card_mix=card_list, column='val')

    # словарь "значение карты: кол-во в миксе"
    val_count_dict = {elem: val_sorted.count(elem) for elem in list(set(val_sorted))}

    # если пар нет
    if set(val_count_dict.values()) == {1}:
        return pairs_cards

    # выбираем все пары, сеты и каре
    pairs_cards = [mix_val_sorted[i] for i in range(len(mix_val_sorted)) if val_count_dict[val_sorted[i]] >= 2]

    return pairs_cards
