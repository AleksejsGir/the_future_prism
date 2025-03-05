# apps/users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """
    Форма регистрации новых пользователей.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': _('Введите email'),
            'autocomplete': 'email'
        }),
        help_text=_('Введите действующий email адрес')
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        """
        Проверка email на уникальность.
        """
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower()
            if User.objects.filter(email=email).exists():
                raise ValidationError(_('Пользователь с таким email уже существует.'))
        return email


class CustomUserChangeForm(UserChangeForm):
    """
    Форма для редактирования данных пользователя.
    """
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'input input-bordered w-full h-32',
            'placeholder': _('Расскажите о себе'),
            'rows': 4
        }),
        help_text=_('Кратко расскажите о себе (необязательно)')
    )

    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'hidden',
            'accept': 'image/*',
            'data-max-size': '5242880'
        }),
        help_text=_('Максимальный размер: 5MB')
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'bio', 'avatar')

    def __init__(self, *args, **kwargs):
        """
        Удаляем стандартное поле пароля и его подсказки.
        """
        super().__init__(*args, **kwargs)
        # Удаляем поле пароля
        if 'password' in self.fields:
            del self.fields['password']

    def clean_avatar(self):
        """
        Проверка загружаемого аватара.
        """
        avatar = self.cleaned_data.get('avatar')
        if avatar and avatar.size > 5 * 1024 * 1024:
            raise ValidationError(_('Размер файла не должен превышать 5MB'))
        return avatar


class LoginForm(forms.Form):
    """
    Форма для входа в систему.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': _('Имя пользователя'),
            'autocomplete': 'username',
            'autofocus': True
        }),
        label=_("Имя пользователя")
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': _('Пароль'),
            'autocomplete': 'current-password'
        }),
        label=_("Пароль")
    )

    remember_me = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox'
        }),
        label=_("Запомнить меня")
    )

    def clean(self):
        """
        Проверка корректности введенных данных.
        """
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not username:
            raise ValidationError({'username': _('Введите имя пользователя')})

        if not password:
            raise ValidationError({'password': _('Введите пароль')})

        return cleaned_data

# <!-- :
# 1. Удалено стандартное поле пароля в форме изменения профиля
# 2. Сохранена существующая логика форм
# 3. Проверить корректность работы форм после изменений
# -->