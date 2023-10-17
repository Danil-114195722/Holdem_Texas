import random
import time


# раздача
def distribution_kards(num, the_object):
    for _ in range(num):
        kard = random.choice(kards)
        del kards[kards.index(kard)]
        if the_object == 'human':
            human.append(kard)
        elif the_object == 'comp':
            comp.append(kard)
        elif the_object == 'tabble':
            tabble.append(kard)


# печать стола
def print_tabble(num_tabble_kards):
    print("\033[3m\033[31m{}".format('MY KARDS'), end='')
    print('TABBLE'.rjust(19, '_'), end='')
    print('OPPONENT KARDS'.rjust(25, '_'))
    print("\033[1m\033[33m")

    if num_tabble_kards == 0:
        print(human[0].ljust(40, ' '), end='')
    else:
        print(human[0].ljust(20, ' '), end='')
        print("\033[1m\033[34m", tabble[0].ljust(19, ' '), end='')
    print("\033[1m\033[33m", '%%%%%%%')

    if num_tabble_kards == 0:
        print(human[1].ljust(40, ' '), end='')
    else:
        print(human[1].ljust(20, ' '), end='')
        print("\033[1m\033[34m", tabble[1].ljust(19, ' '), end='')
    print("\033[1m\033[33m", '%%%%%%%')

    if num_tabble_kards >= 3:
        print("\033[1m\033[34m", ' '.ljust(20, ' '), end='')
        print(tabble[2])
    if num_tabble_kards >= 4:
        print(' '.ljust(21, ' '), end='')
        print(tabble[3])
    if num_tabble_kards == 5:
        print(' '.ljust(21, ' '), end='')
        print(tabble[4])
    print("\033[0m")


# комбинации
def combo(num, the_object):
    global combination_human, combination_comp, Kiker1_Human, Kiker2_Human, One_Pair_Human, Two_Pairs_Human, \
        Three_Of_A_Kind_Human, Strit_Human, Flash_Human, Full_House_Human, Four_Of_A_Kind_Human, Strit_Flash_Human, \
        Kiker1_Comp, Kiker2_Comp, One_Pair_Comp, Two_Pairs_Comp, Three_Of_A_Kind_Comp, \
        Strit_Comp, Flash_Comp, Full_House_Comp, Four_Of_A_Kind_Comp, Strit_Flash_Comp
    combination = ['high_kard']
    # распределение карт
    kard1 = human[0].split()
    kard2 = human[1].split()
    if the_object == 'comp':
        kard1 = comp[0].split()
        kard2 = comp[1].split()

    tabble_kard1 = tabble[0].split()
    tabble_kard2 = tabble[1].split()
    tabble_kard3 = tabble[2].split()

    # масти
    masty = [kard1[1], kard2[1], tabble_kard1[1], tabble_kard2[1], tabble_kard3[1]]
    if num == 4 or num == 5:
        tabble_kard4 = tabble[3].split()
        masty.append(tabble_kard4[1])
    if num == 5:
        tabble_kard5 = tabble[4].split()
        masty.append(tabble_kard5[1])

    # значения
    value = [kard1[0], kard2[0], tabble_kard1[0], tabble_kard2[0], tabble_kard3[0]]
    if num == 4 or num == 5:
        tabble_kard4 = tabble[3].split()
        value.append(tabble_kard4[0])
    if num == 5:
        tabble_kard5 = tabble[4].split()
        value.append(tabble_kard5[0])

    # если валет/дама/король
    for x in range(0, num + 2):
        if value[x] == 'J':
            value[x] = '11'
        elif value[x] == 'Q':
            value[x] = '12'
        elif value[x] == 'K':
            value[x] = '13'
        elif value[x] == 'A':
            value[x] = '14'

    # список комбинаций
    vocabulary_combo = {
        'high_kard': '1',
        'one_pair': '2',
        'two_pairs': '3',
        'three_of_a_kind': '4',
        'strit': '5',
        'flash': '6',
        'full_house': '7',
        'four_of_a_kind': '8',
        'strit_flash': '9',
        'royal_flash': '10'
    }

    # ________________________________________________________________________________________________________________
    # одна пара/две пары/сет/фулл хаус/каре
    four_of_a_kind = '0'
    three_of_a_kind = '0'
    one_pair = '0'
    full_house = []
    two_pairs = []
    list_two_pairs = []
    for x in range(14, 1, -1):
        if value.count(str(x)) == 4:
            combination.append('four_of_a_kind')
            four_of_a_kind = str(x)

        elif value.count(str(x)) == 3:
            combination.append('three_of_a_kind')
            if x > int(three_of_a_kind):
                if int(three_of_a_kind) > int(one_pair):
                    one_pair = three_of_a_kind
                three_of_a_kind = str(x)
            elif int(three_of_a_kind) > x > int(one_pair):
                one_pair = str(x)

        elif value.count(str(x)) == 2:
            combination.append('one_pair')
            list_two_pairs.append(str(x))
            if x > int(one_pair):
                one_pair = str(x)

    if len(list_two_pairs) == 2:
        combination.append('two_pairs')
        two_pairs.append(list_two_pairs[0])
        two_pairs.append(list_two_pairs[1])
    elif len(list_two_pairs) == 3:
        combination.append('two_pairs')
        max1 = list_two_pairs[0]
        if int(list_two_pairs[1]) > int(max1):
            max1 = list_two_pairs[1]
        elif int(list_two_pairs[2]) > int(max1):
            max1 = list_two_pairs[2]
        two_pairs.append(max1)
        del list_two_pairs[list_two_pairs.index(max1)]
        max2 = list_two_pairs[0]

        if int(list_two_pairs[1]) > int(max2):
            max2 = list_two_pairs[1]
        two_pairs.append(max2)

    if int(one_pair) != 0 and int(three_of_a_kind) != 0:
        combination.append('full_house')
        full_house.append(three_of_a_kind)
        full_house.append(one_pair)

    # __________________________________________________________________________________________________________
    # стрит
    strit = '0'
    list_strit = []
    for i in range(1, 11):
        for j in range(i, i + 5):
            if str(j) in value:
                list_strit.append(str(j))
            else:
                list_strit = []
                break
        if len(list_strit) >= 5:
            combination.append('strit')
            strit = list_strit[-1]
            break

    # ___________________________________________________________________________________________________________
    # флеш/стрит флеш/роял флеш
    flash = []
    strit_flash = []
    list_mastys = ['черви', 'буби', 'крести', 'пики']
    for x in range(0, 4):
        if masty.count(list_mastys[x]) >= 5:
            combination.append('flash')
            list_mastys = list_mastys[x]
            for y in range(0, num + 2):
                if masty[y] == list_mastys:
                    flash.append(value[y])

    for x in range(0, len(flash)):
        flash[x] = int(flash[x])
    flash.sort(reverse=True)
    for x in range(0, len(flash)):
        flash[x] = str(flash[x])

    for x in range(0, len(list_strit)):
        if list_strit[x] not in flash:
            break
        if x == len(list_strit) - 1:
            combination.append('strit_flash')
            strit_flash = list_strit
    if strit_flash == ['10', '11', '12', '13', '14']:
        combination.append('royal_flash')

    # ____________________________________________________________________________________________________________
    # присваивание важных значений в комбинациях
    if the_object == 'human':
        if int(value[0]) >= int(value[1]):
            Kiker1_Human = value[0]
            Kiker2_Human = value[1]
        else:
            Kiker1_Human = value[1]
            Kiker2_Human = value[0]

        One_Pair_Human = one_pair
        Two_Pairs_Human = two_pairs
        Three_Of_A_Kind_Human = three_of_a_kind
        Strit_Human = strit
        Flash_Human = flash
        Full_House_Human = full_house
        Four_Of_A_Kind_Human = four_of_a_kind
        Strit_Flash_Human = strit_flash

    elif the_object == 'comp':
        if int(value[0]) >= int(value[1]):
            Kiker1_Comp = value[0]
            Kiker2_Comp = value[1]
        else:
            Kiker1_Comp = value[1]
            Kiker2_Comp = value[0]

        One_Pair_Comp = one_pair
        Two_Pairs_Comp = two_pairs
        Three_Of_A_Kind_Comp = three_of_a_kind
        Strit_Comp = strit
        Flash_Comp = flash
        Full_House_Comp = full_house
        Four_Of_A_Kind_Comp = four_of_a_kind
        Strit_Flash_Comp = strit_flash

    # определение выгрышной комбинации
    for x in range(0, len(combination)):
        if the_object == 'human':
            if int(vocabulary_combo[combination[x]]) > int(vocabulary_combo[combination_human]):
                combination_human = combination[x]

        elif the_object == 'comp':
            if int(vocabulary_combo[combination[x]]) > int(vocabulary_combo[combination_comp]):
                combination_comp = combination[x]


# определение победителя
def winner(print_win):
    global winer, low, combination_human, combination_comp, Kiker1_Human, Kiker2_Human, One_Pair_Human, \
        Two_Pairs_Human, Three_Of_A_Kind_Human, Strit_Human, Flash_Human, Full_House_Human, Four_Of_A_Kind_Human, \
        Strit_Flash_Human, Kiker1_Comp, Kiker2_Comp, One_Pair_Comp, Two_Pairs_Comp, Three_Of_A_Kind_Comp, \
        Strit_Comp, Flash_Comp, Full_House_Comp, Four_Of_A_Kind_Comp, Strit_Flash_Comp, fold

    if not fold:
        vocabulary_combo = {
            'high_kard': '1',
            'one_pair': '2',
            'two_pairs': '3',
            'three_of_a_kind': '4',
            'strit': '5',
            'flash': '6',
            'full_house': '7',
            'four_of_a_kind': '8',
            'strit_flash': '9',
            'royal_flash': '10'}

        if combination_human != combination_comp:
            if int(vocabulary_combo[combination_human]) > int(vocabulary_combo[combination_comp]):
                winer = 'human'
            else:
                winer = 'comp'

        elif combination_human == combination_comp:
            # одна пара
            if combination_human == 'one_pair':
                if int(One_Pair_Human) > int(One_Pair_Comp):
                    winer = 'human'
                elif int(One_Pair_Human) < int(One_Pair_Comp):
                    winer = 'comp'
                else:
                    winer = 'drow'

            # две пары
            if combination_human == 'two_pairs':
                for x in range(0, len(Two_Pairs_Human)):
                    if int(Two_Pairs_Human[x]) > int(Two_Pairs_Comp[x]):
                        winer = 'human'
                        break
                    elif int(Two_Pairs_Human[x]) < int(Two_Pairs_Comp[x]):
                        winer = 'comp'
                        break
                    else:
                        winer = 'drow'

            # сет
            if combination_human == 'three_of_a_kind':
                if int(Three_Of_A_Kind_Human) > int(Three_Of_A_Kind_Comp):
                    winer = 'human'
                elif int(Three_Of_A_Kind_Human) < int(Three_Of_A_Kind_Comp):
                    winer = 'comp'
                else:
                    winer = 'drow'

            # стрит
            if combination_human == 'strit':
                if int(Strit_Human) > int(Strit_Comp):
                    winer = 'human'
                elif int(Strit_Human) < int(Strit_Comp):
                    winer = 'comp'
                else:
                    winer = 'drow'

            # флеш
            if combination_human == 'flash':
                min_flash = Flash_Comp
                if Flash_Human < Flash_Comp:
                    min_flash = Flash_Human
                for x in range(0, len(min_flash)):
                    if int(Flash_Human[x]) > int(Flash_Comp[x]):
                        winer = 'human'
                        break
                    elif int(Flash_Human[x]) < int(Flash_Comp[x]):
                        winer = 'comp'
                        break
                    else:
                        winer = 'drow'

            # фулл хаус
            if combination_human == 'full_house':
                for x in range(0, len(Full_House_Human)):
                    if int(Full_House_Human[x]) > int(Full_House_Comp[x]):
                        winer = 'human'
                        break
                    elif int(Full_House_Human[x]) < int(Full_House_Comp[x]):
                        winer = 'comp'
                        break
                    else:
                        winer = 'drow'

            # каре
            if combination_human == 'four_of_a_kind':
                if int(Four_Of_A_Kind_Human) > int(Four_Of_A_Kind_Comp):
                    winer = 'human'
                elif int(Four_Of_A_Kind_Human) < int(Four_Of_A_Kind_Comp):
                    winer = 'comp'
                else:
                    winer = 'drow'

            # стрит флеш
            if combination_human == 'strit_flash':
                if int(Strit_Flash_Human[-1]) > int(Strit_Flash_Comp[-1]):
                    winer = 'human'
                elif int(Strit_Flash_Human[-1]) < int(Strit_Flash_Comp[-1]):
                    winer = 'comp'
                else:
                    winer = 'drow'

            # роял флеш
            if combination_human == 'royal_flash':
                winer = 'drow'

            # старшая карта / ничья
            if combination_human == 'high_kard' or winer == 'drow':
                if int(Kiker1_Human) > int(Kiker1_Comp):
                    winer = 'human'
                elif int(Kiker1_Human) < int(Kiker1_Comp):
                    winer = 'comp'
                else:
                    if int(Kiker2_Human) > int(Kiker2_Comp):
                        winer = 'human'
                    elif int(Kiker2_Human) < int(Kiker2_Comp):
                        winer = 'comp'
                    else:
                        winer = 'drow'

            # определение проигравшего
            if winer == 'human':
                low = 'comp'
            elif winer == 'comp':
                low = 'human'
            else:
                low = 'drow'

    vocabulary_jqka = {'11': 'J', '12': 'Q', '13': 'K', '14': 'A'}
    kard_value1_human = Kiker1_Human
    kard_value2_human = Kiker2_Human
    kard_value1_comp = Kiker1_Comp
    kard_value2_comp = Kiker2_Comp
    if 10 < int(Kiker1_Human) <= 14:
        kard_value1_human = vocabulary_jqka[Kiker1_Human]
    if 10 < int(Kiker2_Human) <= 14:
        kard_value2_human = vocabulary_jqka[Kiker2_Human]
    if 10 < int(Kiker1_Comp) <= 14:
        kard_value1_comp = vocabulary_jqka[Kiker1_Comp]
    if 10 < int(Kiker2_Comp) <= 14:
        kard_value2_comp = vocabulary_jqka[Kiker2_Comp]

    if not fold:
        if print_win == 'yes':
            print("\033[1m\033[32m", 'combination_human:       ' + combination_human + '''(Human's kards: %s,  %s)'''
                  % (kard_value1_human, kard_value2_human))
            if winer == 'human':
                print('                  / vs /             ' + "\033[3m\033[31m{}".format('Human is winner :)'))
            elif winer == 'comp':
                print('                  / vs /             ' + "\033[3m\033[31m{}".format('Comp is winner :('))
            else:
                print('                  / vs /             ' + "\033[3m\033[31m{}".format('Drow :|'))

            print("\033[1m\033[32m{}".format('combination_comp:        ') + combination_comp +
                  '''(Comp's kards: %s,  %s)''' % (kard_value1_comp, kard_value2_comp))
            print("\033[0m")

    if fold:
        if print_win == 'yes':
            if winer == 'human':
                print("\033[1m\033[32m{}".format('human:                   ') + 'continue game')
                print('                  / vs /             ' + "\033[3m\033[31m{}".format('Human is winner :)'))
                print("\033[1m\033[32m{}".format('comp:                   ') + 'pass')
            elif winer == 'comp':
                print("\033[1m\033[32m{}".format('human:                   ') + 'pass')
                print('                  / vs /             ' + "\033[3m\033[31m{}".format('Comp is winner :('))
                print("\033[1m\033[32m{}".format('comp:                   ') + 'continue game')
            print("\033[0m")


# ИИ
def bet_comp_function(round_poker):
    global combination_human, combination_comp, opponent_money, my_money, winer, low, whose_stack_is_first, bank, \
        bet_human, bet_comp, human, comp, comp_fold, bet_in_round

    kard1_human = human[0].split()
    kard2_human = human[1].split()
    kard1_comp = comp[0].split()
    kard2_comp = comp[1].split()

    for x in range(0, 4):
        compare = kard1_comp
        if x == 1:
            compare = kard2_comp
        elif x == 2:
            compare = kard1_human
        elif x == 3:
            compare = kard2_human
        if compare[0] == 'J':
            compare[0] = '11'
        if compare[0] == 'Q':
            compare[0] = '12'
        if compare[0] == 'K':
            compare[0] = '13'
        if compare[0] == 'A':
            compare[0] = '14'

    max_comp = kard1_comp[0]
    min_comp = kard2_comp[0]
    if int(max_comp) < int(kard2_comp[0]):
        max_comp = kard2_comp[0]
        min_comp = kard1_comp[0]
    max_human = kard1_human[0]
    min_human = kard2_comp[0]
    if int(max_human) < int(kard2_human[0]):
        max_human = kard2_human[0]
        min_human = kard1_comp[0]

    vocabulary_combo = {
        'high_kard': '1',
        'one_pair': '2',
        'two_pairs': '3',
        'three_of_a_kind': '4',
        'strit': '5',
        'flash': '6',
        'full_house': '7',
        'four_of_a_kind': '8',
        'strit_flash': '9',
        'royal_flash': '10'}

    time.sleep(1)

    if round_poker == 'префлоп':
        if bet_human < opponent_money:
            if (kard1_comp[1] == kard2_comp[1] or kard1_comp[0] == kard2_comp[0]) and \
                    (bet_comp == 20 or bet_comp == 10):
                bet_comp = bet_human + random.randint(15, 25)
                if int(max_comp) - int(min_comp) == 1:
                    bet_comp = bet_human + random.randint(35, 50)
            elif (kard1_comp[1] == kard2_comp[1] or kard1_comp[0] == kard2_comp[0]) and \
                    (bet_comp != 20 or bet_comp != 10):
                if int(max_comp) - int(min_comp) == 1:
                    bet_comp = bet_human + random.randint(15, 25)
                else:
                    if random.randint(0, 1) == 0:
                        bet_comp = bet_human + random.randint(10, 30)
                    else:
                        bet_comp = bet_human
            elif max_comp > max_human:
                if random.randint(0, 1) == 1:
                    bet_comp = bet_human + random.randint(5, 15)
                else:
                    bet_comp = bet_human
            elif int(max_comp) - int(min_comp) == 1:
                bet_comp = bet_human + random.randint(15, 25)
            elif bet_in_round == random.randint(2, 3) or bet_in_round == 4:
                bet_comp = bet_human
            else:
                bet_comp = bet_human
        if bet_comp < bet_human:
            bet_comp = opponent_money
        if bet_comp >= opponent_money:
            bet_comp = opponent_money
        if my_money - bet_human == 0:
            bet_comp = bet_human

    elif round_poker == 'флоп':
        if (combination_human == 'royal_flash' or combination_human == 'strit_flash'
            or combination_human == 'four_of_a_kind') or \
                (bet_human >= 350 and combination_comp == 'high_kard' and (bet_in_round == 1 or bet_in_round == 2)) or \
                (bet_human >= 500 and combination_comp == 'high_kard' and bet_in_round == random.randint(3, 4)) or \
                ((combination_comp == 'high_kard' or combination_comp == 'one_pair') and
                 bet_human >= 10000 and 15000 <= opponent_money <= 30000):
            comp_fold = True
        if not comp_fold:
            if int(vocabulary_combo[combination_comp]) == int(vocabulary_combo[combination_human]):
                bet_comp = bet_human + random.randint(0, 10)
            if int(vocabulary_combo[combination_comp]) == int(vocabulary_combo[combination_human]) and \
                    combination_comp == 'high_kard':
                bet_comp = bet_human + random.randint(5, 25)
            if int(min_comp) > int(min_human):
                bet_comp = bet_human + random.randint(10, 40)
            if int(max_comp) > int(max_human):
                bet_comp = bet_human + random.randint(40, 60)
            if int(max_comp) == int(min_comp):
                bet_comp = bet_human + random.randint(60, 100)
            if kard1_comp[1] == kard2_comp[1]:
                bet_comp = bet_human + random.randint(80, 110)
            if int(vocabulary_combo[combination_comp]) == int(vocabulary_combo[combination_human]) and \
                    combination_comp != 'high_kard':
                bet_comp = bet_human + random.randint(40, 100)
            if int(vocabulary_combo[combination_comp]) - int(vocabulary_combo[combination_human]) >= 2:
                bet_comp = random.randint(500, 1500)
            if random.randint(0, 10) == 5:
                bet_comp = random.randint(1500, 3500)
            if combination_comp == 'royal_flash' or combination_comp == 'strit_flash' or \
                    (combination_comp == 'high_kard' and opponent_money < 7000):
                bet_comp = opponent_money
            if bet_in_round == random.randint(2, 3) or bet_in_round == 4:
                bet_comp = bet_human
            if bet_comp < bet_human:
                bet_comp = bet_human
            if bet_comp > opponent_money:
                bet_comp = opponent_money
            if my_money - bet_human == 0:
                bet_comp = bet_human

    return bet_comp


# если пас
def if_fold(fold_object):
    global opponent_money, my_money, winer, low, whose_stack_is_first, bank, bet_human, bet_comp, fold, oll_bank

    fold = True
    bank = bet_human + bet_comp
    my_money -= bet_human
    opponent_money -= bet_comp
    bet_human = 0
    bet_comp = 0
    oll_bank += bank
    print()
    time.sleep(1)
    print('Банк: ' + str(oll_bank), end='     ')
    print('Мои деньги: ' + str(my_money), end='     ')
    print('Деньги компьютера: ' + str(opponent_money))
    print()
    bank = 0
    time.sleep(1.5)
    if fold_object == 'comp':
        winer = 'human'
        low = 'comp'
        my_money += oll_bank
    else:
        winer = 'comp'
        low = 'human'
        opponent_money += oll_bank
    oll_bank = 0


# печать всех денег
def print_bets_and_bank():
    global bet_human, bet_comp, bank, my_money, opponent_money, oll_bank

    print()
    bank = bet_human + bet_comp
    my_money -= bet_human
    opponent_money -= bet_comp
    bet_human = 0
    bet_comp = 0
    oll_bank += bank
    bank = 0
    time.sleep(1)
    print('Банк: ' + str(oll_bank), end='     ')
    print('Мои деньги: ' + str(my_money), end='     ')
    print('Деньги компьютера: ' + str(opponent_money))
    print()
    time.sleep(1.5)


# ставки одного раунда
def bets(round_poker):
    global combination_human, combination_comp, opponent_money, my_money, winer, low, whose_stack_is_first, bank, \
        bet_human, bet_comp, comp_fold, bet_in_round, games_played

    nachalo = False
    if round_poker == 'префлоп':
        if whose_stack_is_first == 'human':
            bet_human = 10 * (games_played // 10 + 1)
            bet_comp = 20 * (games_played // 10 + 1)
            time.sleep(1)
            print('Малый блайнд (Вы): ' + str(bet_human))
            print('Большой блайнд (компьютер): ' + str(bet_comp))
            time.sleep(1)
        else:
            bet_comp = 10 * (games_played // 10 + 1)
            bet_human = 20 * (games_played // 10 + 1)
            print('Малый блайнд (компьютер): ' + str(bet_comp))
            print('Большой блайнд (Вы): ' + str(bet_human))
            time.sleep(1.5)
    while True:
        # первая ставка
        if whose_stack_is_first == 'human':
            # ставка человека
            while True:
                bet_human_input = input('Ваша ставка: ')
                if bet_human_input.isnumeric() == True and bet_comp <= int(bet_human_input) <= my_money:
                    bet_human = int(bet_human_input)
                    break
                elif bet_human_input == 'пас':
                    if_fold('human')
                    return
                print('Введены неверные параметры!!!')
        else:
            time.sleep(0.75)
            # ставка компа
            if round_poker == 'префлоп':
                print('Ставка компьютера: ' + str(bet_comp_function('префлоп')))
            elif round_poker == 'флоп':
                bet_comp_function('флоп')
                if comp_fold:
                    print('Ставка компьютера: пас')
                    if_fold('comp')
                    return
                else:
                    if my_money - bet_human == 0:
                        bet_comp = bet_human
                    print('Ставка компьютера: ' + str(bet_comp_function('флоп')))

        if round_poker == 'флоп':
            if nachalo:
                if bet_human == bet_comp:
                    break
            nachalo = True
        else:
            if (bet_human == bet_comp) or (my_money - bet_human == 0) or (opponent_money - bet_comp == 0):
                break

        # вторая ставка
        if whose_stack_is_first == 'human':
            time.sleep(0.75)
            # ставка компа
            if round_poker == 'префлоп':
                print('Ставка компьютера: ' + str(bet_comp_function('префлоп')))
            elif round_poker == 'флоп':
                bet_comp_function('флоп')
                if comp_fold:
                    print('Ставка компьютера: пас')
                    if_fold('comp')
                    return
                else:
                    if my_money - bet_human == 0:
                        bet_comp = bet_human
                    print('Ставка компьютера: ' + str(bet_comp_function('флоп')))
        else:
            # ставка человека
            while True:
                bet_human_input = input('Ваша ставка: ')
                if bet_human_input.isnumeric() == True and bet_comp <= int(bet_human_input) <= my_money:
                    bet_human = int(bet_human_input)
                    break
                elif bet_human_input == 'пас':
                    if_fold('human')
                    return
                print('Введены неверные параметры!!!')
        if (bet_human == bet_comp) or (my_money - bet_human == 0) or (opponent_money - bet_comp == 0):
            break
        bet_in_round += 1

    print_bets_and_bank()
    bet_in_round = 1


# ОСНОВНАЯ ЧАСТЬ
whose_stack_is_first = 'comp'
my_money = 20000
opponent_money = 20000
game = 'да'
first_game = None
games_played = 0

print()
print("\033[3m\033[31m" + 'Мои деньги: ' + str(my_money), end='     ')
print('Деньги компьютера: ' + str(opponent_money) + "\033[0m")
while True:
    print()
    if first_game:
        while True:
            game = input('Хотите продолжить?   ')
            if game == 'нет' or game == 'да':
                break
            print('Введены неверные параметры!!!')
        if game == 'нет':
            break
        else:
            print()
    kards = ['2 буби', '3 буби', '4 буби', '5 буби', '6 буби', '7 буби', '8 буби', '9 буби', '10 буби', 'J буби',
             'Q буби', 'K буби', 'A буби',
             '2 пики', '3 пики', '4 пики', '5 пики', '6 пики', '7 пики', '8 пики', '9 пики', '10 пики', 'J пики',
             'Q пики', 'K пики', 'A пики',
             '2 черви', '3 черви', '4 черви', '5 черви', '6 черви', '7 черви', '8 черви', '9 черви', '10 черви',
             'J черви', 'Q черви', 'K черви', 'A черви',
             '2 крести', '3 крести', '4 крести', '5 крести', '6 крести', '7 крести', '8 крести', '9 крести',
             '10 крести', 'J крести', 'Q крести', 'K крести', 'A крести']
    random.shuffle(kards)

    human = []
    comp = []
    tabble = []

    if whose_stack_is_first == 'comp':
        whose_stack_is_first = 'human'
    else:
        whose_stack_is_first = 'comp'

    comp_fold = False
    fold = False
    bet_human = 0
    bet_comp = 0
    bank = 0
    oll_bank = 0

    winer = None
    low = None
    combination_human = 'high_kard'
    combination_comp = 'high_kard'

    # карты для сравнения комбо
    Kiker1_Human = '0'
    Kiker2_Human = '0'
    One_Pair_Human = '0'
    Two_Pairs_Human = []
    Three_Of_A_Kind_Human = '0'
    Strit_Human = '0'
    Flash_Human = []
    Full_House_Human = []
    Four_Of_A_Kind_Human = '0'
    Strit_Flash_Human = []

    Kiker1_Comp = '0'
    Kiker2_Comp = '0'
    One_Pair_Comp = '0'
    Two_Pairs_Comp = []
    Three_Of_A_Kind_Comp = '0'
    Strit_Comp = '0'
    Flash_Comp = []
    Full_House_Comp = []
    Four_Of_A_Kind_Comp = '0'
    Strit_Flash_Comp = []

    # ПРЕФЛОП
    bet_in_round = 1
    distribution_kards(1, 'human')
    distribution_kards(1, 'comp')
    distribution_kards(1, 'human')
    distribution_kards(1, 'comp')
    print_tabble(0)
    bets('префлоп')
    # ФЛОП
    distribution_kards(3, 'tabble')
    combo(3, 'human')
    combo(3, 'comp')
    winner('no')
    if not fold and (opponent_money != 0 and my_money != 0):
        time.sleep(2)
        print_tabble(3)
        bets('флоп')
    # ТЁРН
    distribution_kards(1, 'tabble')
    combo(4, 'human')
    combo(4, 'comp')
    winner('no')
    if not fold and (opponent_money != 0 and my_money != 0):
        time.sleep(3)
        print_tabble(4)
        bets('флоп')
    # РИВЕР
    distribution_kards(1, 'tabble')
    combo(5, 'human')
    combo(5, 'comp')
    winner('no')
    print_tabble(5)
    if not fold and (opponent_money != 0 and my_money != 0):
        time.sleep(3)
        bets('флоп')
    # ШОУДАУН
    time.sleep(3)
    winner('yes')
    print()
    if not fold:
        if winer == 'human':
            low = 'comp'
            my_money += oll_bank
        else:
            low = 'human'
            opponent_money += oll_bank
    print("\033[3m\033[31m" + 'Мои деньги: ' + str(my_money), end='     ')
    print('Деньги компьютера: ' + str(opponent_money) + "\033[0m")
    print()
    first_game = 1
    time.sleep(2)
    if opponent_money == 0:
        print('Игра окончена, выиграл человек :)')
        break
    elif my_money == 0:
        print('Игра окончена, выиграл компьютер :(')
        break
    games_played += 1
