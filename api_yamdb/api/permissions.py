from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and request.user.is_administrator)


class AuthorModeratorAdminAndReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_administrator
        )


class SuperUserOrAdminOnly(permissions.BasePermission):
    """Права администартора."""
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_administrator
                     or request.user.is_superuser))
