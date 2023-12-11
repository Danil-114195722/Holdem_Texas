from django.urls import path

from . import views


app_name = 'user_profile'

urlpatterns = [
    # страница профиля и редактирования профиля
    path('', views.profile_page, name='profile_page'),
    path('edit_profile/', views.profile_edit, name='profile_edit'),
    path('change_password/', views.change_passwd, name='change_password'),
]
