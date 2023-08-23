from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticatedOrReadOnly


class IsSuperUserOrReadOnly(BasePermission):
    """
    The request must authenticated as a user, and for non-superusers is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            (request.user.is_authenticated and request.method in SAFE_METHODS) or
            (request.user and
             request.user.is_authenticated and
             request.user.is_superuser)
        )


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
