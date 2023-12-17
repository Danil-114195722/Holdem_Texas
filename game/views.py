from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlencode

from .models import GameProfile

from game.components.poker_game import Game


NEW_GAME_TEMPLATE = 'game/new_game.html'
MAIN_GAME_TEMPLATE = 'game/main_game.html'
LOGIN_URL = 'new_auth/templates/registration/login.html'


# получение всех возможных банкроллов
def get_bankrolls(bankrolls_list: list, cur_bankroll: int):
    if cur_bankroll == 100:
        return bankrolls_list
    # уменьшаем банкролл на 1 порядок
    new_bankroll = cur_bankroll // 10
    bankrolls_list.append(new_bankroll)
    # рекурсия
    return get_bankrolls(bankrolls_list=bankrolls_list, cur_bankroll=new_bankroll)


@login_required
def new_game(request):
    # первый заход на ссылку
    if not request.GET:
        # информация о текущем юзере
        user_info = get_user_model().objects.get(email=request.user.email)
        user_game_profile = GameProfile.objects.get(user=user_info.id)

        # деньги текущего юзера
        user_money = user_game_profile.money
        # определение банкроллов для выбора юзером
        bankrolls = get_bankrolls(
            bankrolls_list=[],
            cur_bankroll=int(f'1{"0" * len(str(user_money))}')
        )
        print(bankrolls)
        return render(request, NEW_GAME_TEMPLATE, context={'bankrolls': bankrolls})

    get_data = request.GET

    # получаем в радио-инпутах при старте новой игры
    game_bankroll = get_data.get('bankroll_for_game')
    main_game_obj = Game(start_player_money=game_bankroll)
    params = {
        'game_obj': main_game_obj,
        'general_game_index': '1',  # генерим
        'move': main_game_obj.first_stack,  # из БД
        'round': '0',
    }
    # перенаправление на страницу игры
    return redirect(f"{reverse('game:main_game')}?{urlencode(params)}")


@login_required
def main_game(request):
    get_data = request.GET

    match get_data.get('round'):
        # переход на префлоп
        case '0':
            print('WAS NEW_GAME')
            game_obj = get_data.get('game_obj')
            print([game_obj])
            game_obj.preflop_round()
            params = {
                'game_obj': get_data.get('game_obj'),
                'general_game_index': get_data.get('general_game_index'),
                'move': 'comp' if (get_data.get('move') == 'human') else 'human',
                'round': '1',
            }
        # переход на флоп
        case '1':
            print('WAS PREFLOP')
            params = {}
        # переход на тёрн
        case '2':
            print('WAS FLOP')
            params = {}
        # переход на ривер
        case '3':
            print('WAS TERN')
            params = {}
        # переход на шоудаун
        case '4':
            print('WAS RIVER')
            params = {}
        # переход на следующую игру
        case '5':
            print('WAS SHOWDOWN')
            params = {}

    return render(request, MAIN_GAME_TEMPLATE, context=params)
