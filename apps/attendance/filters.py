import django_filters

from .models import Attendance


class AttendanceFilter(django_filters.FilterSet):

    employee = django_filters.NumberFilter(
        field_name="employee_id"
    )

    status = django_filters.ChoiceFilter(
        choices=Attendance._meta.get_field("status").choices
    )

    is_deleted = django_filters.BooleanFilter()

    check_in_after = django_filters.DateTimeFilter(
        field_name="check_in",
        lookup_expr="gte"
    )

    check_in_before = django_filters.DateTimeFilter(
        field_name="check_in",
        lookup_expr="lte"
    )

    class Meta:
        model = Attendance

        fields = [
            "employee",
            "status",
            "is_deleted",
            "check_in_after",
            "check_in_before",
        ]