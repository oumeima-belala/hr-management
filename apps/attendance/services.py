from decimal import Decimal
from django.db import transaction
from django.db.models import Count, Q
from core.services import BaseService
from .models import Attendance, AttendanceStatus
from apps.employees.models import Employee
from django.utils import timezone

class AttendanceService(BaseService):

    model = Attendance

    @staticmethod
    def calculate_hours(check_in, check_out):

        if not check_out:
            return Decimal("0.00"), Decimal("0.00")

        duration = check_out - check_in

        worked_hours = Decimal(
            str(round(duration.total_seconds() / 3600, 2))
        )

        return worked_hours, Decimal("0.00")


    @classmethod
    @transaction.atomic
    def create_attendance(cls, validated_data):

        check_in = validated_data["check_in"]
        check_out = validated_data.get("check_out")

        worked_hours, overtime = cls.calculate_hours(
            check_in,
            check_out,
        )

        attendance = cls.model.objects.create(

            **validated_data,

            worked_hours=worked_hours,

            overtime_hours=overtime,
        )

        return attendance


    @classmethod
    @transaction.atomic
    def update_attendance(
        cls,
        attendance,
        validated_data,
    ):

        for field, value in validated_data.items():
            setattr(
                attendance,
                field,
                value,
            )

        attendance.worked_hours, attendance.overtime_hours = (
            cls.calculate_hours(
                attendance.check_in,
                attendance.check_out,
            )
        )

        attendance.save()

        return attendance

    @staticmethod
    def get_statistics():

        attendance_statistics = Attendance.objects.aggregate(

            total=Count("id"),

            active=Count(
                "id",
                filter=Q(is_deleted=False),
            ),

            deleted=Count(
                "id",
                filter=Q(is_deleted=True),
            ),
        )

        status_statistics = Attendance.objects.aggregate(

            PRESENT=Count(
                "id",
                filter=Q(
                    status=AttendanceStatus.PRESENT,
                    is_deleted=False,
                ),
            ),

            ABSENT=Count(
                "id",
                filter=Q(
                    status=AttendanceStatus.ABSENT,
                    is_deleted=False,
                ),
            ),

            LATE=Count(
                "id",
                filter=Q(
                    status=AttendanceStatus.LATE,
                    is_deleted=False,
                ),
            ),

            HALF_DAY=Count(
                "id",
                filter=Q(
                    status=AttendanceStatus.HALF_DAY,
                    is_deleted=False,
                ),
            ),

            REMOTE=Count(
                "id",
                filter=Q(
                    status=AttendanceStatus.REMOTE,
                    is_deleted=False,
                ),
            ),

            LEAVE=Count(
                "id",
                filter=Q(
                    status=AttendanceStatus.LEAVE,
                    is_deleted=False,
                ),
            ),
        )

        return {
            "attendances": attendance_statistics,
            "status": status_statistics,
        }

    @classmethod
    @transaction.atomic
    def check_in(cls, employee):

        attendance = cls.model.objects.create(
            employee=employee,
            check_in=timezone.now(),
            status=AttendanceStatus.PRESENT,
        )

        return attendance


@classmethod
@transaction.atomic
def check_out(cls, employee):

    attendance = cls.model.objects.get(
        employee=employee,
        check_out__isnull=True,
        is_deleted=False,
    )

    attendance.check_out = timezone.now()

    (
        attendance.worked_hours,
        attendance.overtime_hours,
    ) = cls.calculate_hours(
        attendance.check_in,
        attendance.check_out,
    )

    attendance.save()

    return attendance


@staticmethod
def get_dashboard():

    today = timezone.localdate()

    total_employees = Employee.objects.filter(
        is_deleted=False
    ).count()

    checked_in_today = Attendance.objects.filter(
        is_deleted=False,
        check_in__date=today,
    ).count()

    checked_out_today = Attendance.objects.filter(
        is_deleted=False,
        check_out__date=today,
    ).count()

    currently_working = Attendance.objects.filter(
        is_deleted=False,
        check_in__date=today,
        check_out__isnull=True,
    ).count()

    status_counts = Attendance.objects.filter(
        is_deleted=False,
        check_in__date=today,
    ).aggregate(

        present=Count(
            "id",
            filter=Q(status=AttendanceStatus.PRESENT),
        ),

        late=Count(
            "id",
            filter=Q(status=AttendanceStatus.LATE),
        ),

        half_day=Count(
            "id",
            filter=Q(status=AttendanceStatus.HALF_DAY),
        ),

        remote=Count(
            "id",
            filter=Q(status=AttendanceStatus.REMOTE),
        ),

        leave=Count(
            "id",
            filter=Q(status=AttendanceStatus.LEAVE),
        ),
    )

    return {

        "employees": {
            "total": total_employees,
        },

        "today": {

            "checked_in": checked_in_today,

            "checked_out": checked_out_today,

            "currently_working": currently_working,

            "absent": max(
                total_employees - checked_in_today,
                0,
            ),
        },

        "attendance_status": status_counts,
    }

