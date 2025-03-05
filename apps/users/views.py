# apps/users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext as _
from rest_framework import generics, status
from rest_framework.response import Response
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm, LoginForm
from .serializers import UserRegistrationSerializer
from .utils import save_avatar


class UserRegistrationView(generics.CreateAPIView):
    """API для регистрации пользователей через REST."""
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        """Создание нового пользователя через API."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def user_login(request):
    """
    Обработка входа пользователя через веб-форму.

    Процесс:
    1. Проверяем, не авторизован ли уже пользователь
    2. Обрабатываем POST-запрос с данными формы
    3. Аутентифицируем пользователя
    4. Перенаправляем на нужную страницу
    """
    # Если пользователь уже авторизован, перенаправляем на профиль
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Если аутентификация успешна
                if user.is_active:
                    login(request, user)
                    messages.success(
                        request,
                        _('Добро пожаловать, {0}!').format(user.username)
                    )
                    # Безопасная обработка параметра next
                    next_page = request.GET.get('next')
                    if next_page and next_page.startswith('/'):
                        return HttpResponseRedirect(next_page)
                    return redirect('profile')
                else:
                    messages.error(
                        request,
                        _('Ваш аккаунт деактивирован')
                    )
            else:
                messages.error(
                    request,
                    _('Неверное имя пользователя или пароль')
                )
    else:
        form = LoginForm()

    # Добавляем расширенный контекст для шаблона
    context = {
        'form': form,
        'title': _('Вход в систему'),
        'next': request.GET.get('next', ''),
    }
    return render(request, 'registration/login.html', context)


def register_view(request):
    """
    Обработка регистрации пользователя через веб-форму.

    Процесс:
    1. Проверяем, не авторизован ли уже пользователь
    2. Обрабатываем POST-запрос с данными формы
    3. Создаем нового пользователя
    4. Автоматически логиним пользователя
    """
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(
                    request,
                    _('Регистрация успешна! Добро пожаловать!')
                )
                return redirect('profile')
            except Exception as e:
                messages.error(
                    request,
                    _('Ошибка при регистрации: {0}').format(str(e))
                )
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    """
    Отображение профиля пользователя.
    Защищено декоратором login_required.
    """
    context = {
        'title': _('Профиль пользователя'),
        'user_since': request.user.date_joined,
        'avatar_url': request.user.get_avatar_url(),
    }
    return render(request, 'registration/profile.html', context)


@login_required
def edit_profile(request):
    """
    Редактирование профиля пользователя.

    Процесс:
    1. Обработка формы с данными профиля
    2. Обработка загрузки аватара
    3. Сохранение изменений
    """
    if request.method == 'POST':
        # Создаем форму без файлов, чтобы избежать двойной обработки аватара
        form = CustomUserChangeForm(
            request.POST,
            instance=request.user
        )
        if form.is_valid():
            # Сначала сохраняем данные профиля без аватара
            user = form.save(commit=False)

            # Обработка аватара
            avatar_file = request.FILES.get('avatar')
            if avatar_file:
                try:
                    save_avatar(user, avatar_file)
                    messages.success(request, _('Профиль и аватар успешно обновлены!'))
                except Exception as e:
                    messages.error(
                        request,
                        _('Ошибка при загрузке аватара: {0}').format(str(e))
                    )
                    # Сохраняем остальные изменения, даже если аватар не загрузился
                    user.save()
                    return render(
                        request,
                        'registration/edit_profile.html',
                        {'form': form}
                    )
            else:
                # Если аватар не загружен, просто сохраняем профиль
                user.save()
                messages.success(request, _('Профиль успешно обновлен!'))

            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(
        request,
        'registration/edit_profile.html',
        {'form': form}
    )


@login_required
@require_http_methods(["POST"])
def delete_avatar(request):
    """
    Удаление аватара пользователя.
    Требует POST-запрос для безопасности.
    """
    user = request.user
    if user.avatar:
        try:
            # Удаляем файл аватара
            user.avatar.delete(save=False)
            user.avatar = None
            user.save()
            messages.success(request, _('Аватар успешно удален'))
        except Exception as e:
            messages.error(
                request,
                _('Ошибка при удалении аватара: {0}').format(str(e))
            )
    else:
        messages.info(request, _('У вас нет загруженного аватара'))

    return redirect('profile')


@login_required
def change_password(request):
    """
    Изменение пароля пользователя.

    Процесс:
    1. Проверка текущего пароля
    2. Создание и проверка нового пароля
    3. Сохранение нового пароля
    4. Обновление сессии пользователя
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Обновляем сессию, чтобы пользователь не выходил из системы
            update_session_auth_hash(request, user)
            messages.success(request, _('Ваш пароль успешно изменен!'))
            return redirect('profile')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'registration/password_change.html', {'form': form})