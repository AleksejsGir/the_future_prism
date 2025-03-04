# apps/news/translation.py
from modeltranslation.translator import register, TranslationOptions
from .models import Category, News

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')  # Поля категории для перевода

@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'content', 'short_description')  # Поля новости для перевода