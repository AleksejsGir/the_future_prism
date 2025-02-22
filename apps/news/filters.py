import django_filters
from .models import News

class NewsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    content = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.NumberFilter(field_name='category__id')
    published_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = News
        fields = ['title', 'content', 'category', 'published_date']
