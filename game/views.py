from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def new_game(request):

    if not request.GET:
        data = {
            'general_game_index': '1',  # генерим
            'move': 'human'  # из БД
        }

        return render(request, 'game/new_game.html', context=data)

    params = request.GET
    print(params)

    data = {
        'general_game_index': '1',  # из БД или get-параметров
        'human_cards': [],
        'comp_cards': [],
        'table_cards': [],
        'human_bet': 0,
        'comp_bet': 0,
        'bank': 0,
        'move': 'human',
        'round': 0,
    }

    return render(request, 'game/new_game.html', context=data)
