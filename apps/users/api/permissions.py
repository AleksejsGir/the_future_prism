# apps/users/api/permissions.py
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее только владельцам объекта редактировать его.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешения на чтение всегда разрешены для любых запросов GET, HEAD или OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешения на запись только для владельца
        return obj == request.user