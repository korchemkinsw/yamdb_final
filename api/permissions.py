from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAdminUser)


class IsAdminUserOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin


class IsAuthorModeratorAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        return (
            obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
