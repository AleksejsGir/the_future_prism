# apps/users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import generics, status
from rest_framework.response import Response
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm, LoginForm
from .serializers import UserRegistrationSerializer


# Заметки для дальнейшей разработки:
# 1. Разделяем API и веб-представления для чистоты кода
# 2. Используем декораторы для защиты маршрутов
# 3. Добавляем информативные сообщения для пользователя
# 4. Обрабатываем все возможные ошибки

# API Представления
class UserRegistrationView(generics.CreateAPIView):
    """API для регистрации пользователей через REST."""
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        """
        Создание нового пользователя через API.
        Возвращает статус 201 при успешном создании.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Веб-представления
def user_login(request):
    """
    Обработка входа пользователя через веб-форму.
    Использует кастомную форму LoginForm для валидации.
    """
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.username}!')
                # Получаем next параметр или переходим на профиль
                next_page = request.GET.get('next', 'profile')
                return redirect(next_page)
            else:
                messages.error(request, 'Неверные учетные данные')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


def register_view(request):
    """
    Обработка регистрации пользователя через веб-форму.
    Использует CustomUserCreationForm для валидации и создания пользователя.
    """
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна! Добро пожаловать!')
            return redirect('profile')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    """
    Отображение и редактирование профиля пользователя.
    Требует аутентификации (декоратор login_required).
    """
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)

    context = {
        'form': form,
        # Добавляем дополнительный контекст для шаблона
        'title': 'Профиль пользователя',
        'user_since': request.user.date_joined
    }

    return render(request, 'registration/profile.html', context)


@login_required
def edit_profile(request):
    """
    Отдельное представление для редактирования профиля.
    Позволяет разделить отображение и редактирование данных.
    """
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Изменения сохранены!')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'registration/edit_profile.html', {'form': form})