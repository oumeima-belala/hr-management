from django.contrib import admin

from .models import Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "is_deleted",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
    )

    list_filter = (
        "is_deleted",
    )

    ordering = (
        "name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Department Information",
            {
                "fields": (
                    "name",
                    "description",
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