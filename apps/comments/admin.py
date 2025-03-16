# apps/comments/admin.py
from django.contrib import admin
from .models import Comment, CommentReaction
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'news', 'author', 'created_at', 'is_approved', 'like_count', 'dislike_count')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('content',)

    # Обновляем названия полей для перевода
    fieldsets = (
        (_('Comment Information'), {
            'fields': ('news', 'author', 'parent', 'content', 'is_approved')
        }),
        (_('Statistics'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at',)

    # Добавляем действия с переводом
    actions = ['approve_comments', 'reject_comments']

    def approve_comments(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, _('%(count)d comments have been approved.') % {'count': updated})

    approve_comments.short_description = _('Approve selected comments')

    def reject_comments(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, _('%(count)d comments have been rejected.') % {'count': updated})

    reject_comments.short_description = _('Reject selected comments')


@admin.register(CommentReaction)
class CommentReactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'user', 'like_type', 'created_at')
    list_filter = ('like_type', 'created_at')
    search_fields = ('user__username', 'comment__content')

    # Обновляем названия полей для перевода
    fieldsets = (
        (_('Reaction Information'), {
            'fields': ('comment', 'user', 'like_type')
        }),
        (_('Statistics'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at',)