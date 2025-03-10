# core/views.py
from django.shortcuts import render, redirect

def home(request):
    """
    Главная страница. Перенаправляет на список новостей.
    """
    return redirect('news_list')


def about_view(request):
    """
    Отображает страницу "О проекте".
    """
    return render(request, 'about.html', {
        'title': 'О проекте'
    })


def contact_view(request):
    """
    Отображает страницу "Контакты".
    """
    return render(request, 'contact.html', {
        'title': 'Контакты'
    })