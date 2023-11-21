from typing import List


def royal_flash(straight_flash_list: List[dict]) -> List[dict] | None:
    """Определение наличия роял флеша"""
    royal_flash_cards = None

    if not straight_flash_list:
        return royal_flash_cards

    # если среди флеша есть наивысший стрит
    if list(range(10, 15)) == list(map(lambda elem: elem['val'], straight_flash_list)):
        # список с картами роял флеша
        royal_flash_cards = straight_flash_list

    return royal_flash_cards


def straight_flash(flash_list: List[dict]) -> List[dict] | None:
    """Определение наличия стрит флеша"""
    straight_flash_cards = straight(card_list=flash_list)

    return straight_flash_cards


def flash(card_list: List[dict]) -> List[dict] | None:
    """Определение наличия флеша"""
    flash_cards = None

    mix_val_sorted = sorted(card_list, key=lambda elem: elem['val'])
    card_suits = list(map(lambda elem: elem['suit'], card_list))

    # выбираем ту масть, которая содержится в наборе >=5 раз
    suit_to_flash = [
        suit_letter
        for suit_letter in ['A', 'B', 'C', 'D']
        if card_suits.count(suit_letter) >= 5
    ]

    # если какая-то масть содержится в наборе >=5 раз, то выбираем список с картами флеша
    if suit_to_flash:
        flash_cards = list(filter(lambda elem: elem['suit'] == suit_to_flash[0], mix_val_sorted))

    return flash_cards


def straight(card_list: List[dict]) -> List[dict] | None:
    """Определение наличия стрита"""
    straight_cards = None

    if not card_list:
        return straight_cards

    # явное копирование списка, чтобы в главном ничего не поменялось при добавлении номера 1
    card_list = card_list.copy()
    # если есть туз (номер 14), то добавляем номер 1 (для второго случая туза)
    if card_list[-1]['val'] == 14:
        card_list.insert(0, {'val': 1, 'suit': card_list[-1]['suit']})

    without_dupls = [card_list[i] for i in range(len(card_list)) if card_list[i]['val'] != card_list[i - 1]['val']]
    val_sorted = list(map(lambda elem: elem['val'], without_dupls))

    # определяем список без дубликатов и разделяем уникальные значения по 5 в каждый подсписок
    seq_list = [val_sorted[i - 5:i] for i in range(len(val_sorted), 4, -1)]
    # выбираем тот подсписок, который содержит последовательность значений
    straight_list = [elem for elem in seq_list if elem == list(range(elem[0], elem[0] + 5))]

    # если есть стрит
    if straight_list:
        first_value = straight_list[0][0]
        # список с картами стрита
        straight_cards = [elem for elem in without_dupls if elem['val'] in range(first_value, first_value + 5)]

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

    val_sorted = list(map(lambda elem: elem['val'], card_list))
    # словарь "значение карты: кол-во в миксе"
    val_count_dict = {elem: val_sorted.count(elem) for elem in list(set(val_sorted))}

    # если пар нет
    if set(val_count_dict.values()) == {1}:
        return pairs_cards

    # выбираем все пары, сеты и каре
    pairs_cards = [card_list[i] for i in range(len(card_list)) if val_count_dict[val_sorted[i]] >= 2]

    return pairs_cards
