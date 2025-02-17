# core/views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from apps.news.models import News, Category


def home(request):
    return news_list(request)


def news_list(request):
    search_query = request.GET.get('search', '')
    news_list = News.objects.all().order_by('-published_date')

    if search_query:
        news_list = news_list.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )

    categories = Category.objects.all().order_by('name')
    category_id = request.GET.get('category')

    if category_id:
        news_list = news_list.filter(category__id=category_id)

    context = {
        'news_list': news_list,
        'categories': categories,
        'search_query': search_query,
    }

    return render(request, 'news_list.html', context)


def news_detail(request, news_id):
    news_item = get_object_or_404(News, id=news_id)
    return render(request, 'news_detail.html', {'news': news_item})