from rest_framework.permissions import BasePermission, SAFE_METHODS
from apps.users.models import UserRole

class EmployeePermission(BasePermission):
    def has_permission(self, request, view):

        user = request.user

        if not user.is_authenticated:
            return False

        if user.role == UserRole.ADMIN:
            return True

        if request.method in SAFE_METHODS:
            return user.role in [
                UserRole.HR,
                UserRole.ACCOUNTANT,
                UserRole.WORKSHOP_MANAGER,
            ]

        if request.method == "POST":
            return user.role == UserRole.HR

        # Restauration
        if (
            request.method == "PATCH"
            and view.__class__.__name__ == "RestoreEmployeeView"
        ):
            return False  # seul ADMIN, déjà traité plus haut

        # Modification
        if request.method in ("PUT", "PATCH"):
            return user.role == UserRole.HR

        if request.method == "PATCH":

            if view.__class__.__name__ == "RestoreEmployeeView":
                return user.role == UserRole.ADMIN

            return user.role in [
                UserRole.ADMIN,
                UserRole.HR,
            ]

        if request.method == "DELETE":
            return False

        return False