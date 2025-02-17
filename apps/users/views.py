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
from .utils import save_avatar


# Заметки для дальнейшей разработки:
# 1. Разделяем API и веб-представления для чистоты кода
# 2. Используем декораторы для защиты маршрутов
# 3. Добавляем информативные сообщения для пользователя
# 4. Обрабатываем все возможные ошибки
# 5. Добавлена обработка загрузки аватаров и других файлов


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
    Обрабатывает как обычные данные формы, так и загрузку аватара.
    """
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # Проверяем, загружен ли новый аватар
            avatar_file = request.FILES.get('avatar')
            if avatar_file:
                try:
                    # Используем утилиту для обработки и сохранения аватара
                    save_avatar(request.user, avatar_file)
                    messages.success(request, 'Аватар успешно обновлен!')
                except Exception as e:
                    messages.error(request, f'Ошибка при загрузке аватара: {str(e)}')
                    return render(request, 'registration/profile.html', {'form': form})

            # Сохраняем остальные данные формы
            user = form.save(commit=False)

            # Проверяем изменение email
            if user.email != request.user.email:
                # В будущем здесь можно добавить подтверждение email
                pass

            user.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)

    context = {
        'form': form,
        'title': 'Профиль пользователя',
        'user_since': request.user.date_joined,
        'avatar_url': request.user.get_avatar_url(),
    }

    return render(request, 'registration/profile.html', context)


@login_required
def edit_profile(request):
    """
    Отдельное представление для редактирования профиля.
    Позволяет разделить отображение и редактирование данных.
    """
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # Обработка аватара
            avatar_file = request.FILES.get('avatar')
            if avatar_file:
                try:
                    save_avatar(request.user, avatar_file)
                    messages.success(request, 'Аватар успешно обновлен!')
                except Exception as e:
                    messages.error(request, f'Ошибка при загрузке аватара: {str(e)}')
                    return render(request, 'registration/edit_profile.html', {'form': form})

            form.save()
            messages.success(request, 'Изменения сохранены!')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'registration/edit_profile.html', {'form': form})


@login_required
def delete_avatar(request):
    """
    Представление для удаления текущего аватара пользователя.
    Требует подтверждения через POST-запрос для безопасности.
    """
    if request.method == 'POST':
        user = request.user
        if user.avatar:
            # Удаляем файл аватара
            user.avatar.delete(save=False)
            user.avatar = None
            user.save()
            messages.success(request, 'Аватар успешно удален')
        else:
            messages.info(request, 'У вас нет загруженного аватара')
    return redirect('profile')