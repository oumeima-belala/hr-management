from rest_framework import serializers
from .models import Employee


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