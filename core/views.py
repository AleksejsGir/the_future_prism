# core/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.html import strip_tags
from django_filters.views import FilterView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.news.models import News, Category
from apps.news.filters import NewsFilter  # Подключаем фильтр

def home(request):
    """
    Главная страница. Перенаправляет на список новостей.
    """
    return redirect('news_list')  # Исправленный редирект

class NewsListView(FilterView):
    """
    Представление списка новостей с фильтрацией через django-filter.
    """
    model = News
    template_name = 'news_list.html'
    filterset_class = NewsFilter

    def get_queryset(self):
        """
        Фильтруем и сортируем новости по дате публикации (новые сверху).
        """
        queryset = super().get_queryset().order_by('-published_date')
        return queryset

    def get_context_data(self, **kwargs):
        """
        Добавляем категории и пагинацию в контекст шаблона.
        """
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all().order_by('name')
        context['categories'] = categories

        # Пагинация
        page = self.request.GET.get('page', 1)
        paginator = Paginator(context['object_list'], 9)  # 9 новостей на страницу

        try:
            context['news_list'] = paginator.page(page)
        except PageNotAnInteger:
            context['news_list'] = paginator.page(1)
        except EmptyPage:
            context['news_list'] = paginator.page(paginator.num_pages)

        return context

def news_detail(request, news_id):
    """
    Отображает детальную страницу новости.
    """
    news_item = get_object_or_404(News, id=news_id)

    # Увеличиваем счетчик просмотров
    news_item.view_count += 1
    news_item.save(update_fields=['view_count'])

    # Получаем похожие новости той же категории (исключая текущую)
    similar_news = News.objects.filter(category=news_item.category) \
                       .exclude(id=news_id) \
                       .order_by('-published_date')[:3]

    # Подготавливаем контент для предпросмотра в похожих новостях
    for news in similar_news:
        news.preview_content = strip_tags(news.content)

    return render(request, 'news_detail.html', {
        'news': news_item,
        'similar_news': similar_news
    })
