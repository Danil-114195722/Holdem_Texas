from os import remove as remove_file

from django.conf import settings
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlencode

from .forms import ProfileForm
from .models import Profile
from new_auth.models import DEFAULT_PROFILE_PHOTO


@login_required
def profile_page(request):
    user_info = get_user_model().objects.get(email=request.user.email)
    profile_info = Profile.objects.get(user=user_info.id)

    data = {
        'user': user_info,
        'profile': profile_info,
        'admin_url': settings.ADMIN_URL if user_info.is_staff else None,
        'status': '',
    }

    # здесь нужно как-то обнулять параметры GET-запроса после одного использования
    if request.GET:
        data['status'] = request.GET.get('status')

    return render(request, 'user_profile/profile.html', context=data)


@login_required
def profile_edit(request):
    cur_profile = Profile.objects.get(user=request.user.id)
    # фото до его замены
    cur_photo = cur_profile.photo

    if request.method != 'POST':
        form = ProfileForm(instance=cur_profile)

    else:
        # Обработка заполненной формы.
        form = ProfileForm(data=request.POST, files=request.FILES, instance=cur_profile)
        if form.is_valid():
            # поле "фото" в форме ('' - если не менялось, None - если фото заменили)
            photo_field = form.data.get('photo')
            # если фото очищали, то 'photo-clear' = 'on'
            photo_clear = request.POST.get('photo-clear')
            # если было заменено фото
            if cur_photo != DEFAULT_PROFILE_PHOTO and (photo_field != '' or photo_clear == 'on'):
                old_photo_path = str(settings.BASE_DIR) + cur_photo.url
                try:
                    remove_file(path=old_photo_path)
                except FileNotFoundError:
                    print('File not found!')

            form.save()
            # перенаправление на страницу профиля с указанием статуса
            params = {'status': 'profile_edit'}
            return redirect(f"{reverse('user_profile:profile_page')}?{urlencode(params)}")

    # Вывести пустую или недействительную форму.
    data = {
        'form': form,
    }

    return render(request, 'user_profile/profile_edit.html', context=data)


@login_required
def change_passwd(request):
    if request.method != 'POST':
        form = PasswordChangeForm(request.user)

    else:
        # Обработка заполненной формы.
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            # перенаправление на страницу профиля с указанием статуса
            params = {'status': 'change_password'}
            return redirect(f"{reverse('user_profile:profile_page')}?{urlencode(params)}")

    # Вывести пустую или недействительную форму.
    data = {
        'form': form,
    }

    return render(request, 'user_profile/change_password.html', context=data)
