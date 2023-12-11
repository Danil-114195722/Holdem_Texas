from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlencode

from user_profile.models import Profile
from .forms import RegisterForm, EmailForm


class ResetPasswordException(Exception):
    pass


def homepage(request):
    # здесь нужно как-то обнулять параметры GET-запроса после одного использования
    if request.GET:
        data = {'error': request.GET.get('error')}
        return render(request, 'registration/index.html', context=data)

    return render(request, 'registration/index.html')


def sign_up(request):
    """Регистрирует нового пользователя."""

    if request.method != 'POST':
        form = RegisterForm()

    else:
        # Обработка заполненной формы.
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()

            # Выполнение входа и перенаправление на домашнюю страницу.
            login(request, user=new_user)
            return redirect('new_auth:homepage')

    # Вывести пустую или недействительную форму.
    data = {
        'form': form,
    }

    return render(request, 'registration/sign_up.html', context=data)


def password_reset(request):
    # ошибка, если введённая почта не привязана ни к одному юзеру
    user_error = False

    if request.method != 'POST':
        password_reset_form = EmailForm()

    # Обработка заполненной формы.
    else:
        try:
            password_reset_form = EmailForm(data=request.POST)
            if not password_reset_form.is_valid():
                raise ResetPasswordException

            else:
                email = password_reset_form.cleaned_data['email']

                # по введённой почте достаём юзера и его профиль
                try:
                    user = get_user_model().objects.get(email=email)
                    profile = Profile.objects.get(user=user.id)
                except ObjectDoesNotExist:
                    raise ResetPasswordException

                # определяем динамическое содержимое письма
                subject = 'Запрошен сброс пароля'
                context = {
                    'email': user.email,
                    'domain': '127.0.0.1:8000',
                    'site_name': 'Texas Holdem',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),  # шифруем id юзера
                    'user': profile.nickname,
                    'token': default_token_generator.make_token(user),  # генерируем токен для юзера
                    'protocol': 'http',
                }
                html_msg = render_to_string(
                    'registration/password_reset_email_message.html',
                    context=context
                )

                # отправка письма
                try:
                    print(settings.EMAIL_HOST_USER)
                    print(user.email)

                    send_mail(
                        subject=subject,
                        message='ссылка',
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[user.email],
                        html_message=html_msg,
                    )
                    # для проверки обработки ошибки
                    # print(len(4))
                except Exception as error:
                    print(error)
                    # перенаправление на домашнюю страницу с указанием ошибки отправки почты
                    params = {'error': 'send_email_error'}
                    return redirect(f"{reverse('new_auth:homepage')}?{urlencode(params)}")

                return redirect('new_auth:password_reset_done')

        # исключение при неверной почте
        except ResetPasswordException:
            user_error = True

    # Вывести пустую или недействительную форму.
    data = {
        'form': password_reset_form,
        'user_error': user_error,
    }

    return render(request, 'registration/password_reset_form.html', context=data)
