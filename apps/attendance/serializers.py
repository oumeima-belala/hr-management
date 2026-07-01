from rest_framework import serializers
from apps.employees.models import Employee
from .models import Attendance
from django.utils import timezone

class AttendanceListSerializer(serializers.ModelSerializer):

    employee = serializers.CharField(
        source="employee.full_name",
        read_only=True
    )

    class Meta:
        model = Attendance
        fields = ["id", "employee", "status", "check_in", "check_out", "worked_hours",]


class AttendanceDetailSerializer(serializers.ModelSerializer):

    employee = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = ["id", "employee", "status", "check_in", "check_out", "worked_hours",
                  "overtime_hours", "notes", "created_at", "updated_at",]

    def get_employee(self, obj):

        return {
            "id": obj.employee.id,
            "full_name": obj.employee.full_name,
            "email": obj.employee.user.email,
        }


class CreateAttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = ["employee", "check_in", "check_out", "status", "notes",]

    def validate_employee(self, employee):

        if employee.is_deleted:

            raise serializers.ValidationError(
                "This employee is inactive."
            )

        return employee

    def validate(self, attrs):

        employee = attrs.get("employee", getattr(self.instance, "employee", None))
        check_in = attrs.get("check_in", getattr(self.instance, "check_in", None))
        check_out = attrs.get("check_out", getattr(self.instance, "check_out", None))

        if check_out and check_out <= check_in:
            raise serializers.ValidationError({
                "check_out": "Check-out must be after check-in."
            })

        queryset = Attendance.objects.filter(
            employee=employee,
            is_deleted=False,
        )

        # Exclure l'objet actuel lors d'une mise à jour
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        # Empêcher plusieurs pointages ouverts
        if queryset.filter(check_out__isnull=True).exists():
            raise serializers.ValidationError(
                "This employee already has an active attendance."
            )

        # Vérifier les chevauchements
        if check_out:
            if queryset.filter(
                    check_in__lt=check_out,
                    check_out__gt=check_in,
            ).exists():
                raise serializers.ValidationError(
                    "This attendance overlaps an existing attendance."
                )

        return attrs


class UpdateAttendanceSerializer(
    CreateAttendanceSerializer
):
    pass


class AttendanceCountSerializer(serializers.Serializer):
    total = serializers.IntegerField()

    active = serializers.IntegerField()

    deleted = serializers.IntegerField()


class AttendanceStatusStatisticsSerializer(
    serializers.Serializer
):
    PRESENT = serializers.IntegerField()

    ABSENT = serializers.IntegerField()

    LATE = serializers.IntegerField()

    HALF_DAY = serializers.IntegerField()

    REMOTE = serializers.IntegerField()

    LEAVE = serializers.IntegerField()


class AttendanceStatisticsSerializer(
    serializers.Serializer
):

    attendances = AttendanceCountSerializer()

    status = AttendanceStatusStatisticsSerializer()


class CheckInSerializer(serializers.Serializer):

    employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.filter(is_deleted=False)
    )

    def validate_employee(self, employee):

        if Attendance.objects.filter(
            employee=employee,
            check_out__isnull=True,
            is_deleted=False,
        ).exists():

            raise serializers.ValidationError(
                "This employee already has an active attendance."
            )

        return employee


class CheckOutSerializer(serializers.Serializer):

    employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.filter(
            is_deleted=False
        )
    )

    def validate_employee(self, employee):

        attendance = Attendance.objects.filter(
            employee=employee,
            check_out__isnull=True,
            is_deleted=False,
        ).first()

        if not attendance:
            raise serializers.ValidationError(
                "No active attendance found for this employee."
            )

        return employee


class AttendanceDashboardSerializer(serializers.Serializer):

    employees = serializers.DictField()

    today = serializers.DictField()

    attendance_status = serializers.DictField()

