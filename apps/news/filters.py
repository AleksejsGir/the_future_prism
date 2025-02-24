# apps/news/filters.py
import django_filters
from .models import News

class NewsFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='multi_field_search')
    category = django_filters.NumberFilter(field_name='category__id')
    published_date = django_filters.DateFromToRangeFilter()

    def multi_field_search(self, queryset, name, value):
        """
        Метод для поиска по заголовку и содержимому
        """
        if value:
            return queryset.filter(
                title__icontains=value) | queryset.filter(content__icontains=value
            )
        return queryset

    class Meta:
        model = News
        fields = ['search', 'category', 'published_date']