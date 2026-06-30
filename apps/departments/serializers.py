from rest_framework import serializers
from .models import Department

class DepartmentListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ("id", "name",)


class DepartmentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ("id", "name", "description", "created_at", "updated_at",)


class CreateDepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ("name", "description",)


class UpdateDepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ("name", "description",)


class DepartmentCountSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    active = serializers.IntegerField()
    deleted = serializers.IntegerField()


class DepartmentStatisticsSerializer(serializers.Serializer):
    departments = DepartmentCountSerializer()