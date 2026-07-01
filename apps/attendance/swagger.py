from core.swagger import (
    list_docs,
    create_docs,
    detail_docs,
    update_docs,
    delete_docs,
    restore_docs,
    statistics_docs,
)

from .serializers import (
    AttendanceListSerializer,
    AttendanceDetailSerializer,
    CreateAttendanceSerializer,
    UpdateAttendanceSerializer,
    AttendanceStatisticsSerializer,
    CheckInSerializer,
    CheckOutSerializer,
    AttendanceDashboardSerializer,
)


def attendance_list_docs():
    return list_docs(
        tag="Attendances",
        serializer=AttendanceListSerializer,
        description="""
        Retrieve the list of all active attendance records.

        Supports:
        - Pagination
        - Search
        - Filtering
        - Ordering
        """,
    )


def attendance_create_docs():
    return create_docs(
        tag="Attendances",
        request_serializer=CreateAttendanceSerializer,
        response_serializer=AttendanceDetailSerializer,
        description="""
        Create a new attendance record.

        Worked hours are calculated automatically by the system.
        """,
    )


def attendance_detail_docs():
    return detail_docs(
        tag="Attendances",
        serializer=AttendanceDetailSerializer,
        description="""
        Retrieve the details of a specific attendance record.
        """,
    )


def attendance_update_docs():
    return update_docs(
        tag="Attendances",
        request_serializer=UpdateAttendanceSerializer,
        response_serializer=AttendanceDetailSerializer,
        description="""
        Update an existing attendance record.

        Worked hours are recalculated automatically after every update.
        """,
    )


def attendance_delete_docs():
    return delete_docs(
        tag="Attendances",
        description="""
        Soft delete an attendance record.

        The attendance remains stored in the database and can be restored later.
        """,
    )


def attendance_restore_docs():
    return restore_docs(
        tag="Attendances",
        serializer=AttendanceDetailSerializer,
        description="""
        Restore a previously deleted attendance record.
        """,
    )


def attendance_statistics_docs():
    return statistics_docs(
        tag="Attendances",
        serializer=AttendanceStatisticsSerializer,
        description="""
        Retrieve attendance statistics.

        Includes:
        - Total attendances
        - Active attendances
        - Deleted attendances
        - Attendance count by status
        """,
    )


from core.swagger import create_docs


def attendance_check_in_docs():
    return create_docs(
        tag="Attendances",
        request_serializer=CheckInSerializer,
        response_serializer=AttendanceDetailSerializer,
        description="""
        Check in an employee.

        The system automatically records the current date and time as the check-in time.
        """,
    )


def attendance_check_out_docs():

    return create_docs(

        tag="Attendances",

        request_serializer=CheckOutSerializer,

        response_serializer=AttendanceDetailSerializer,

        description="""
        Check out an employee.

        The system automatically records the current date and time,
        calculates the worked hours and closes the attendance.
        """,
    )


def attendance_dashboard_docs():

    return statistics_docs(

        tag="Attendances",

        serializer=AttendanceDashboardSerializer,

        description="""
        Retrieve the attendance dashboard.

        Includes:
        - Total employees
        - Today's check-ins
        - Today's check-outs
        - Employees currently working
        - Today's absences
        - Attendance status distribution
        """,
    )