# apps/users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm, LoginForm
from .services import save_avatar


def user_login(request):
    """
    Обработка входа пользователя через веб-форму.
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
    return render(request, 'users/login.html', context)


def register_view(request):
    """
    Обработка регистрации пользователя через веб-форму.
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

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    """
    Отображение профиля пользователя.
    """
    context = {
        'title': _('Профиль пользователя'),
        'user_since': request.user.date_joined,
        'avatar_url': request.user.get_avatar_url(),
    }
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request):
    """
    Редактирование профиля пользователя.
    """
    if request.method == 'POST':
        # Создаем форму без файлов, чтобы избежать двойной обработки аватара
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            # Сначала сохраняем данные профиля без аватара
            user = form.save(commit=False)

            # Обработка аватара через сервисный слой
            avatar_file = request.FILES.get('avatar')
            if avatar_file:
                try:
                    save_avatar(user, avatar_file)
                    messages.success(request, _('Профиль и аватар успешно обновлены!'))
                except ValidationError as e:
                    messages.error(request, str(e))
                    return render(request, 'users/edit_profile.html', {'form': form})
            else:
                # Если аватар не загружен, просто сохраняем профиль
                user.save()
                messages.success(request, _('Профиль успешно обновлен!'))

            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
@require_http_methods(["POST"])
def delete_avatar(request):
    """
    Удаление аватара пользователя через веб-интерфейс.
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
    Изменение пароля пользователя через веб-интерфейс.
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

    return render(request, 'users/password_change.html', {'form': form})


@login_required
def user_comments(request):
    """
    Отображение всех комментариев пользователя.
    """
    # Получаем все комментарии пользователя, отсортированные по дате (сначала новые)
    comments = request.user.comments.all().order_by('-created_at')

    context = {
        'comments': comments,
        'active_tab': 'comments',  # Для подсветки активного пункта меню
        'title': _('Мои комментарии'),
    }
    return render(request, 'users/user_comments.html', context)