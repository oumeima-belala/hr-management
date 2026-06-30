from core.permissions import BaseRolePermission
from apps.users.models import UserRole


class DepartmentPermission(BaseRolePermission):

    allowed_roles = {

        "GET": [
            UserRole.HR,
            UserRole.ACCOUNTANT,
            UserRole.WORKSHOP_MANAGER,
        ],

        "POST": [
            UserRole.HR,
        ],

        "PUT": [
            UserRole.HR,
        ],

        "PATCH": [
            UserRole.HR,
        ],

        "DELETE": [],
    }