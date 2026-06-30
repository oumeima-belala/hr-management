from django.db.models import Count, Q

from core.services import BaseService

from .models import Department


class DepartmentService(BaseService):

    model = Department

    @staticmethod
    def get_statistics():

        statistics = Department.objects.aggregate(

            total=Count("id"),

            active=Count(
                "id",
                filter=Q(is_deleted=False)
            ),

            deleted=Count(
                "id",
                filter=Q(is_deleted=True)
            ),
        )

        return {
            "departments": statistics
        }