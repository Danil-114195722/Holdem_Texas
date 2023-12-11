from django.urls import path, include
from . import views


app_name = 'new_auth'

urlpatterns = [
    # главная (домашняя) страница
    path('', views.homepage, name='homepage'),

    # страницы восстановления пароля
    path('password_reset/', views.password_reset, name='password_reset'),

    # страницы регистрации, входа и выхода
    path('', include('django.contrib.auth.urls')),
    path('sign_up/', views.sign_up, name='sign_up'),
]
