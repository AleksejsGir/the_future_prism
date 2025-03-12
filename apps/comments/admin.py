# apps/comments/admin.py
from django.contrib import admin
from .models import Comment, CommentReaction

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'news', 'author', 'created_at', 'is_approved', 'like_count', 'dislike_count')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('content',)

@admin.register(CommentReaction)
class CommentReactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'user', 'like_type', 'created_at')
    list_filter = ('like_type', 'created_at')
    search_fields = ('user__username', 'comment__content')