from rest_framework import serializers
from .models import User
from apps.employees.serializers import EmployeeProfileSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "role",)


class UserProfileSerializer(serializers.ModelSerializer):

    employee = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "email", "role", "is_active", "employee",)

    def get_employee(self, obj):
        try:
            return EmployeeProfileSerializer(
                obj.employee,
                context=self.context
            ).data
        except Exception:
            return None