# apps/users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """
    Форма для регистрации новых пользователей.
    Расширяет стандартную форму Django для обеспечения безопасности.
    Добавляет дополнительную валидацию полей и улучшенный пользовательский интерфейс.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Введите email',
            'autocomplete': 'email'  # Добавляем поддержку автозаполнения
        }),
        help_text='Введите действующий email адрес'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        error_messages = {
            'username': {
                'unique': 'Пользователь с таким именем уже существует.',
                'invalid': 'Имя пользователя может содержать только буквы, цифры и символы @/./+/-/_'
            }
        }

    def __init__(self, *args, **kwargs):
        """
        Инициализация формы с улучшенными стилями и плейсхолдерами.
        Добавляет подсказки для пользователя и улучшает доступность формы.
        """
        super().__init__(*args, **kwargs)

        # Улучшенная стилизация полей формы
        self.fields['username'].widget.attrs.update({
            'class': 'input input-bordered w-full',
            'placeholder': 'Введите имя пользователя',
            'autocomplete': 'username',
            'autofocus': True  # Автофокус на первом поле
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'input input-bordered w-full',
            'placeholder': 'Введите пароль',
            'autocomplete': 'new-password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'input input-bordered w-full',
            'placeholder': 'Подтвердите пароль',
            'autocomplete': 'new-password'
        })

        # Улучшенные сообщения об ошибках
        self.error_messages = {
            'password_mismatch': 'Введенные пароли не совпадают.',
            'password_too_short': 'Пароль должен содержать как минимум 8 символов.',
            'password_common': 'Этот пароль слишком простой.',
            'password_numeric': 'Пароль не может состоять только из цифр.'
        }

    def clean_email(self):
        """
        Расширенная проверка email на уникальность и корректность.
        Проверяет формат и доступность email адреса.
        """
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower()  # Приводим к нижнему регистру
            if User.objects.filter(email=email).exists():
                raise ValidationError(
                    'Пользователь с таким email уже существует. '
                    'Пожалуйста, используйте другой email адрес.'
                )
        return email

    def clean_username(self):
        """
        Дополнительная валидация имени пользователя.
        Проверяет длину и допустимые символы.
        """
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise ValidationError(
                'Имя пользователя должно содержать не менее 3 символов'
            )
        return username


class CustomUserChangeForm(UserChangeForm):
    """
    Форма для редактирования данных пользователя.
    Включает расширенную валидацию и обработку загрузки файлов.
    """
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'input input-bordered w-full h-32',
            'placeholder': 'Расскажите о себе',
            'rows': 4
        }),
        help_text='Кратко расскажите о себе (необязательно)'
    )

    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'hidden',
            'accept': 'image/*',
            'data-max-size': '5242880'  # 5MB в байтах
        }),
        help_text='Рекомендуемый размер: 300x300 пикселей. Максимальный размер: 5MB'
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'bio', 'avatar')
        error_messages = {
            'email': {
                'invalid': 'Пожалуйста, введите корректный email адрес.',
                'unique': 'Этот email уже используется другим пользователем.'
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Улучшенная стилизация полей
        for field in self.fields:
            if field not in ['bio', 'avatar']:
                self.fields[field].widget.attrs.update({
                    'class': 'input input-bordered w-full',
                    'autocomplete': field
                })

    def clean_avatar(self):
        """
        Проверка загружаемого аватара.
        Валидация размера и формата файла.
        """
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError(
                    'Размер файла не должен превышать 5MB'
                )
            if not avatar.content_type.startswith('image/'):
                raise ValidationError(
                    'Пожалуйста, загрузите файл изображения'
                )
        return avatar


class LoginForm(forms.Form):
    """
    Форма для входа пользователя с расширенной валидацией
    и улучшенным пользовательским интерфейсом.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Имя пользователя',
            'autocomplete': 'username',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Пароль',
            'autocomplete': 'current-password'
        })
    )

    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox'
        })
    )

    def clean(self):
        """
        Расширенная валидация формы входа.
        Проверяет наличие и корректность всех необходимых полей.
        """
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not username:
            raise ValidationError({
                'username': 'Пожалуйста, введите имя пользователя'
            })
        if not password:
            raise ValidationError({
                'password': 'Пожалуйста, введите пароль'
            })

        return cleaned_data