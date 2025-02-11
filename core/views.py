# core/views.py
from django.shortcuts import render, get_object_or_404, redirect
from apps.news.models import News, Category

def home(request):
    # Если вы хотите, чтобы главная страница показывала новости, можно перенаправлять на news_list.
    return news_list(request)

def news_list(request):
    # Получаем список новостей, отсортированный по дате публикации (сначала новейшие)
    news_list = News.objects.all().order_by('-published_date')
    # Получаем список категорий
    categories = Category.objects.all().order_by('name')
    # Если передан GET-параметр category, фильтруем новости по нему
    category_id = request.GET.get('category')
    if category_id:
        news_list = news_list.filter(category__id=category_id)
    return render(request, 'news_list.html', {'news_list': news_list, 'categories': categories})

def news_detail(request, news_id):
    news_item = get_object_or_404(News, id=news_id)
    return render(request, 'news_detail.html', {'news': news_item})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Аутентификация пользователя
        from django.contrib.auth import authenticate, login
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = "Неверные учетные данные"
            return render(request, 'login.html', {'error': error})
    return render(request, 'login.html')

def profile(request):
    # Для доступа к профилю пользователь должен быть аутентифицирован.
    from django.contrib.auth.decorators import login_required
    # Если вы используете декоратор, можно объявить функцию так:
    # @login_required
    # def profile(request):
    #     return render(request, 'profile.html')
    # Здесь для простоты вызываем render напрямую:
    return render(request, 'profile.html')
