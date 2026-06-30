from rest_framework.permissions import BasePermission, SAFE_METHODS

from apps.users.models import UserRole


class BaseRolePermission(BasePermission):
    """
    Generic role-based permission.
    Child classes only define allowed_roles.
    """

    allowed_roles = {
        "GET": [],
        "POST": [],
        "PUT": [],
        "PATCH": [],
        "DELETE": [],
    }

    def has_permission(self, request, view):

        user = request.user

        if not user.is_authenticated:
            return False

        # Admin always has full access
        if user.role == UserRole.ADMIN:
            return True

        if self.has_custom_permission(request, view):
            return True

        method = request.method

        # GET, HEAD, OPTIONS
        if method in SAFE_METHODS:
            method = "GET"

        allowed = self.allowed_roles.get(method, [])

        return user.role in allowed

    def has_custom_permission(self, request, view):
        return False