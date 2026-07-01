from django.contrib import admin

from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = (
        "employee",
        "status",
        "check_in",
        "check_out",
        "worked_hours",
        "overtime_hours",
        "is_deleted",
    )

    list_filter = (
        "status",
        "is_deleted",
        "check_in",
    )

    search_fields = (
        "employee__first_name",
        "employee__last_name",
        "employee__user__email",
    )

    ordering = (
        "-check_in",
    )

    readonly_fields = (
        "worked_hours",
        "overtime_hours",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "employee",
    )