from django.urls import path

from . import views


app_name = 'game'

urlpatterns = [
    path('', views.new_game, name='new_game'),
]
