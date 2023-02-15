"""Классы контроля разрешений на взаимодействие пользователя с данными."""
from rest_framework import permissions


class IsAuthorizedOrReadOnlyPermission(permissions.BasePermission):
    """
    Класс разршения на взаимодействия пользователя с данными.
    Все пользователи могут совершать следующие запросы:
    -GET
    -HEAD
    -OPTIONS
    Только автор может изменять свои записи.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """
        Метод определяет доступ к данным если запросы из числа безопасных.
        Если запрос иной, то пользователь является автором.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user == obj.author


class AuthorOr401Permission(permissions.BasePermission):
    """Класс для разрешения доступа к данным только для автора."""

    def has_permission(self, request, view):
        """Метод предоставляет доступ если пользователь является автором."""

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Метод позволяет только автору иметь доступ к объекту.
        """
        return request.user == obj.user
