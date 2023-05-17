from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions


class AuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
    """Разрешение доступа автору, админу, модератору."""
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.role == 'moderator'
            or request.user.role == 'admin'
            or obj.author == request.user
        )


class IsAuthorOrAndAdmin(BasePermission):
    """Разрешение доступа авторизированному админу."""
    def has_permission(self, request, view, obj):
        return (request.user.role == 'admin' or request.user.is_superuser
                or request.user != obj.user)


class IsAuthIsAdminPermission(BasePermission):
    """Разрешение доступа авторизированному админу."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.role == 'admin' or request.user.is_superuser)
        )


class AdminOrReadOnly(permissions.BasePermission):
    """Разрешение доступа админу или чтение."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.role == 'admin'
        return False
