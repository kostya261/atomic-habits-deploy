from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Разрешение, позволяющее доступ только владельцу объекта.
    """

    def has_object_permission(self, request, view, obj):
        # Проверяем, является ли пользователь владельцем привычки
        return obj.user == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее полный доступ владельцу,
    а остальным - только чтение.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешаем безопасные методы (GET, HEAD, OPTIONS) всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Для остальных методов проверяем владельца
        return obj.user == request.user


class IsPublicOrOwner(permissions.BasePermission):
    """
    Разрешение, позволяющее доступ к публичным привычкам всем,
    а к приватным - только владельцу.
    """

    def has_object_permission(self, request, view, obj):
        # Если привычка публичная - доступ всем
        if obj.is_public:
            return True

        # Если приватная - только владельцу
        return obj.user == request.user
