# core/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from apps.news.models import News, Category


def home(request):
    # Перенаправляем на news_list
    return news_list(request)


def news_list(request):
    # Получаем параметр поиска из GET-запроса
    search_query = request.GET.get('search', '')

    # Базовый QuerySet новостей, отсортированный по дате публикации
    news_list = News.objects.all().order_by('-published_date')

    # Если есть поисковый запрос, фильтруем новости
    if search_query:
        news_list = news_list.filter(
            Q(title__icontains=search_query) |  # Поиск по заголовку
            Q(content__icontains=search_query)  # Поиск по содержимому
        )

    # Получаем список категорий
    categories = Category.objects.all().order_by('name')

    # Фильтрация по категории
    category_id = request.GET.get('category')
    if category_id:
        news_list = news_list.filter(category__id=category_id)

    # Формируем контекст для шаблона
    context = {
        'news_list': news_list,
        'categories': categories,
        'search_query': search_query,
    }

    return render(request, 'news_list.html', context)


def news_detail(request, news_id):
    # Получаем конкретную новость или возвращаем 404
    news_item = get_object_or_404(News, id=news_id)
    return render(request, 'news_detail.html', {'news': news_item})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Аутентификация пользователя
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = "Неверные учетные данные"
            return render(request, 'login.html', {'error': error})
    return render(request, 'login.html')


@login_required  # Добавляем декоратор для защиты профиля
def profile(request):
    return render(request, 'profile.html')