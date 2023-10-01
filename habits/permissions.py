from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Проверяет к своей ли привычке пытается запросить доступ авторизованный пользователь
    """
    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        return False
