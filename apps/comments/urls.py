# apps/comments/urls.py
from django.urls import path
from apps.comments import views

urlpatterns = [
    path('news/<int:news_id>/comments/', views.comment_list, name='comment_list'),
    path('news/<int:news_id>/comments/add/', views.add_comment, name='add_comment'),
    path('comments/<int:comment_id>/delete/', views.delete_comment_view, name='delete_comment'),
    # Новый маршрут для лайков/дизлайков
    path('comments/<int:comment_id>/reaction/', views.toggle_reaction, name='toggle_comment_reaction'),
]