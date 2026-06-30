import django_filters

from apps.users.models import UserRole
from .models import Employee, Gender, FamilyStatus


class EmployeeFilter(django_filters.FilterSet):

    gender = django_filters.ChoiceFilter(
        field_name="gender",
        choices=Gender.choices,
    )

    family_status = django_filters.ChoiceFilter(
        field_name="family_status",
        choices=FamilyStatus.choices,
    )

    role = django_filters.ChoiceFilter(
        field_name="user__role",
        choices=UserRole.choices,
    )

    is_active = django_filters.BooleanFilter(
        field_name="user__is_active",
    )

    class Meta:
        model = Employee

        fields = (
            "gender",
            "family_status",
            "role",
            "is_active",
        )