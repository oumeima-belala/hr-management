from rest_framework import serializers
from .models import Employee
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from apps.users.models import User, UserRole


class EmployeeProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ("id", "full_name", "address", "phone_number","gender", "social_security_number",
                  "family_status", "birth_date", "age", "photo",)

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_photo(self, obj):
        request = self.context.get("request")
        if obj.photo:
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url

        return None

class EmployeeListSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        source="user.email",
        read_only=True
    )
    role = serializers.CharField(
        source="user.role",
        read_only=True
    )
    is_active = serializers.BooleanField(
        source="user.is_active",
        read_only=True
    )

    class Meta:
        model = Employee
        fields = ["id", "full_name", "email", "role", "phone_number", "photo", "is_active",]


class EmployeeDetailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    role = serializers.CharField(source="user.role", read_only=True)
    is_active = serializers.BooleanField(source="user.is_active", read_only=True)

    class Meta:
        model = Employee
        fields = ["id", "email", "role", "is_active", "first_name", "last_name", "full_name", "address",
                  "phone_number", "social_security_number", "gender", "family_status", "birth_date", "age",
                  "photo", "created_at", "updated_at", "hired_at"]


class CreateEmployeeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(choices=UserRole.choices)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    address = serializers.CharField()
    phone_number = serializers.CharField()
    social_security_number = serializers.CharField()
    gender = serializers.ChoiceField(choices=Employee._meta.get_field("gender").choices)
    family_status = serializers.ChoiceField(choices=Employee._meta.get_field("family_status").choices)
    birth_date = serializers.DateField()
    photo = serializers.ImageField(required=False, allow_null=True)

    def validate_email(self, value):
        value = value.lower().strip()

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Cet email est déjà utilisé."
            )
        return value

    def validate_social_security_number(self, value):
        if Employee.objects.filter(
            social_security_number=value
        ).exists():
            raise serializers.ValidationError(
                "Ce numéro de sécurité sociale existe déjà."
            )
        return value

    def validate_password(self, value):
        validate_password(value)
        return value


class UpdateEmployeeSerializer(serializers.Serializer):
    role = serializers.ChoiceField(
        choices=UserRole.choices,
        required=False
    )
    first_name = serializers.CharField(
        required=False
    )
    last_name = serializers.CharField(
        required=False
    )
    address = serializers.CharField(
        required=False
    )
    phone_number = serializers.CharField(
        required=False
    )
    social_security_number = serializers.CharField(
        required=False
    )
    gender = serializers.ChoiceField(
        choices=Employee._meta.get_field("gender").choices,
        required=False
    )
    family_status = serializers.ChoiceField(
        choices=Employee._meta.get_field("family_status").choices,
        required=False
    )
    birth_date = serializers.DateField(
        required=False
    )
    photo = serializers.ImageField(
        required=False,
        allow_null=True
    )


class EmployeeCountSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    active = serializers.IntegerField()
    deleted = serializers.IntegerField()


class GenderStatisticsSerializer(serializers.Serializer):
    male = serializers.IntegerField()
    female = serializers.IntegerField()


class FamilyStatusStatisticsSerializer(serializers.Serializer):
    single = serializers.IntegerField()
    married = serializers.IntegerField()
    divorced = serializers.IntegerField()
    widowed = serializers.IntegerField()


class RoleStatisticsSerializer(serializers.Serializer):
    ADMIN = serializers.IntegerField()
    HR = serializers.IntegerField()
    ACCOUNTANT = serializers.IntegerField()
    WORKSHOP_MANAGER = serializers.IntegerField()
    ASSISTANT = serializers.IntegerField()


class EmployeeStatisticsSerializer(serializers.Serializer):
    employees = EmployeeCountSerializer()
    gender = GenderStatisticsSerializer()
    family_status = FamilyStatusStatisticsSerializer()
    roles = RoleStatisticsSerializer()