from core.permissions import BaseRolePermission
from apps.users.models import UserRole


class AttendancePermission(BaseRolePermission):

    allowed_roles = {

        "GET": [
            UserRole.HR,
            UserRole.ACCOUNTANT,
            UserRole.WORKSHOP_MANAGER,
        ],

        "POST": [
            UserRole.HR,
            UserRole.WORKSHOP_MANAGER,
        ],

        "PUT": [
            UserRole.HR,
            UserRole.WORKSHOP_MANAGER,
        ],

        "PATCH": [
            UserRole.HR,
            UserRole.WORKSHOP_MANAGER,
        ],

        "DELETE": [],
    }