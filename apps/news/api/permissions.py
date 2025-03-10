# apps/news/api/permissions.py
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее только администраторам создавать и изменять объекты.
    Обычные пользователи могут только просматривать.
    """

    def has_permission(self, request, view):
        # Разрешения на чтение разрешены для любых запросов GET, HEAD или OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешения на запись только для администраторов
        return request.user and request.user.is_staff