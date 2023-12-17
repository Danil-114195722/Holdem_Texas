from django.urls import path

from . import views


app_name = 'game'

urlpatterns = [
    path('start_new/', views.new_game, name='new_game'),
    path('play_now/', views.main_game, name='main_game'),
]
