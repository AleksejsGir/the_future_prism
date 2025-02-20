# core/views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.news.models import News, Category


def home(request):
    return news_list(request)


def news_list(request):
    # Получаем параметры запроса
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category')
    page = request.GET.get('page', 1)

    # Получаем все новости, сортируем по дате
    news_queryset = News.objects.all().order_by('-published_date')

    # Применяем фильтр поиска
    if search_query:
        news_queryset = news_queryset.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )

    # Применяем фильтр по категории
    if category_id:
        news_queryset = news_queryset.filter(category__id=category_id)

    # Пагинация
    paginator = Paginator(news_queryset, 9)  # По 9 новостей на страницу
    try:
        news_list = paginator.page(page)
    except PageNotAnInteger:
        news_list = paginator.page(1)
    except EmptyPage:
        news_list = paginator.page(paginator.num_pages)

    # Получаем все категории
    categories = Category.objects.all().order_by('name')

    # Контекст для шаблона
    context = {
        'news_list': news_list,
        'categories': categories,
        'search_query': search_query,
    }

    return render(request, 'news_list.html', context)


def news_detail(request, news_id):
    # Получаем новость по ID или возвращаем 404
    news_item = get_object_or_404(News, id=news_id)

    # Увеличиваем счетчик просмотров
    news_item.view_count += 1
    news_item.save(update_fields=['view_count'])

    # Получаем похожие новости той же категории (исключая текущую)
    similar_news = News.objects.filter(category=news_item.category) \
                       .exclude(id=news_id) \
                       .order_by('-published_date')[:3]

    return render(request, 'news_detail.html', {
        'news': news_item,
        'similar_news': similar_news
    })