from django.db import models

from apps.employees.models import Employee


class AttendanceStatus(models.TextChoices):
    PRESENT = "PRESENT", "Present"
    ABSENT = "ABSENT", "Absent"
    LATE = "LATE", "Late"
    HALF_DAY = "HALF_DAY", "Half Day"
    REMOTE = "REMOTE", "Remote"
    LEAVE = "LEAVE", "Leave"


class Attendance(models.Model):

    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="attendances",
    )

    check_in = models.DateTimeField()

    check_out = models.DateTimeField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=AttendanceStatus.choices,
        default=AttendanceStatus.PRESENT,
    )

    worked_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    overtime_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    notes = models.TextField(
        blank=True,
    )

    is_deleted = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = ["-check_in"]

        verbose_name = "Attendance"

        verbose_name_plural = "Attendances"

        indexes = [
            models.Index(fields=["employee"]),
            models.Index(fields=["check_in"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return (
            f"{self.employee.full_name} - "
            f"{self.check_in:%Y-%m-%d %H:%M}"
        )