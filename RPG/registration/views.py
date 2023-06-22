
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import Registration
import random
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return render(request, 'registration/register.html', {'error': 'Пароли не совпадают'})

        # Генерируем 4-значный код активации
        activation_code = str(random.randint(1000, 9999))

        # Создаем нового пользователя
        user = User(username=username, email=email, is_active=False)

        # Сохраняем пользователя с хешированным паролем
        user.set_password(password)
        user.save()

        # Создаем запись регистрации
        registration = Registration(user=user, activation_code=activation_code)
        registration.save()

        # Отправляем код активации на почту пользователя
        send_mail(
            'Код активации',
            f'Ваш код активации: {activation_code}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return redirect('activate')

    return render(request, 'registration/register.html')


def activate(request):
    if request.method == 'POST':
        activation_code = request.POST['activation_code']

        # Проверяем, есть ли код активации в базе данных
        try:
            registration = Registration.objects.get(activation_code=activation_code, is_activated=False)
        except Registration.DoesNotExist:
            return redirect('activate')

        # Активируем пользователя
        user = registration.user
        user.is_active = True
        user.save()

        # Помечаем регистрацию как завершенную
        registration.is_activated = True
        registration.save()

        return redirect('success')

    return render(request, 'registration/activate.html')

def success(request):
    return render(request, 'registration/success.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Проверяем учетные данные пользователя
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Учетные данные верны, выполняем вход пользователя
            login(request, user)
            return redirect('/news')  # Замените 'home' на URL вашей домашней страницы
        else:
            # Учетные данные неверны, отображаем сообщение об ошибке
            return render(request, 'registration/login.html', {'error': 'Неверное имя пользователя или пароль'})

    return render(request, 'registration/login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/news')  # Замените 'home' на URL вашей домашней страницы

    return render(request, 'registration/logout.html')