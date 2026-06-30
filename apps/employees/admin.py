from django.contrib import admin

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "full_name",
        "user_email",
        "user_role",
        "phone_number",
        "gender",
        "family_status",
        "is_deleted",
        "created_at",
    )

    search_fields = (
        "first_name",
        "last_name",
        "user__email",
        "phone_number",
        "social_security_number",
    )

    list_filter = (
        "gender",
        "family_status",
        "user__role",
        "is_deleted",
    )

    ordering = (
        "last_name",
        "first_name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "age",
    )

    list_select_related = (
        "user",
    )

    fieldsets = (
        (
            "Personal Information",
            {
                "fields": (
                    "user",
                    "first_name",
                    "last_name",
                    "birth_date",
                    "age",
                    "gender",
                    "family_status",
                    "photo",
                )
            },
        ),
        (
            "Contact",
            {
                "fields": (
                    "address",
                    "phone_number",
                    "social_security_number",
                )
            },
        ),
        (
            "System",
            {
                "fields": (
                    "is_deleted",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    @admin.display(description="Email")
    def user_email(self, obj):
        return obj.user.email

    @admin.display(description="Role")
    def user_role(self, obj):
        return obj.user.role