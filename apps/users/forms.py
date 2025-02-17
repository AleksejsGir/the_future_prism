# apps/users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


# Заметки для дальнейшей разработки:
# 1. Формы наследуются от встроенных форм Django для безопасности
# 2. Все поля имеют валидацию и стилизацию
# 3. Используются кастомные методы очистки для дополнительных проверок

class CustomUserCreationForm(UserCreationForm):
    """
    Форма для регистрации новых пользователей.
    Расширяет стандартную форму Django для обеспечения безопасности.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Введите email'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        """
        Инициализация формы с добавлением стилей и плейсхолдеров
        для соответствия дизайну сайта.
        """
        super().__init__(*args, **kwargs)

        # Стилизация полей формы
        self.fields['username'].widget.attrs.update({
            'class': 'input input-bordered w-full',
            'placeholder': 'Введите имя пользователя'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'input input-bordered w-full',
            'placeholder': 'Введите пароль'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'input input-bordered w-full',
            'placeholder': 'Подтвердите пароль'
        })

    def clean_email(self):
        """
        Проверка уникальности email.
        Вызывается автоматически при валидации формы.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует')
        return email


class CustomUserChangeForm(UserChangeForm):
    """
    Форма для редактирования данных пользователя.
    Используется в личном кабинете.
    """
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'input input-bordered w-full h-32',
            'placeholder': 'Расскажите о себе'
        })
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'bio')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Стилизация полей
        for field in self.fields:
            if field != 'bio':
                self.fields[field].widget.attrs.update({
                    'class': 'input input-bordered w-full'
                })


class LoginForm(forms.Form):
    """
    Форма для входа пользователя.
    Использует встроенную систему аутентификации Django.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Имя пользователя'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Пароль'
        })
    )

    def clean(self):
        """
        Дополнительная валидация формы.
        Проверяет наличие обязательных полей.
        """
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not username or not password:
            raise ValidationError('Пожалуйста, заполните все поля')

        return cleaned_data