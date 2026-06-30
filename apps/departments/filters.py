import django_filters
from .models import Department


class DepartmentFilter(django_filters.FilterSet):

    is_deleted = django_filters.BooleanFilter()

    class Meta:
        model = Department
        fields = ["is_deleted",]