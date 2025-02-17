# apps/users/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser
from .serializers import UserRegistrationSerializer

# API Views
class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Web Views
# apps/users/views.py
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Добавляем проверку на пустые поля
        if not username or not password:
            messages.error(request, 'Пожалуйста, заполните все поля')
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            # Оставляем редирект на home, как в оригинальном коде
            return redirect('home')
        else:
            # Используем messages вместо контекста с error
            messages.error(request, 'Неверные учетные данные')
            return render(request, 'login.html')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        context = {
            'username': username,
            'email': email
        }

        # Валидация
        if not all([username, email, password1, password2]):
            context['error'] = "Пожалуйста, заполните все поля"
            return render(request, 'register.html', context)

        if password1 != password2:
            context['error'] = "Пароли не совпадают"
            return render(request, 'register.html', context)

        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('profile')
        except Exception as e:
            context['error'] = "Ошибка при регистрации. Попробуйте позже."
            return render(request, 'register.html', context)

    return render(request, 'register.html')

@login_required
def profile(request):
    return render(request, 'profile.html')