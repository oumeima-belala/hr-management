from django.db import transaction
from apps.users.models import User, UserRole
from django.db.models import Count, Q
from .models import Employee, Gender, FamilyStatus

class EmployeeService:
    @staticmethod
    @transaction.atomic
    def create_employee(validated_data):
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        role = validated_data.pop("role")

        user = User.objects.create_user(
            email=email,
            password=password,
            role=role,
        )

        employee = Employee.objects.create(
            user=user,
            **validated_data
        )

        return employee


    @staticmethod
    def list_employees():
        """
        Retourne tous les employés non supprimés.
        """
        return (
            Employee.objects
            .select_related("user")
            .filter(is_deleted=False)
        )


    @staticmethod
    def get_employee(employee_id):
        """
        Retourne un employé à partir de son identifiant.
        """

        return (
            Employee.objects
            .select_related("user")
            .filter(
                id=employee_id,
                is_deleted=False
            )
            .first()
        )


    @staticmethod
    @transaction.atomic
    def update_employee(employee, validated_data):
        role = validated_data.pop("role", None)
        if role is not None:
            employee.user.role = role
            employee.user.save()

        for field, value in validated_data.items():
            setattr(employee, field, value)

        employee.save()

        return employee

    @staticmethod
    @transaction.atomic
    def delete_employee(employee):

        print("Avant :", employee.is_deleted)

        employee.is_deleted = True
        employee.user.is_active = False

        employee.user.save()
        employee.save()

        employee.refresh_from_db()

        print("Après :", employee.is_deleted)
        print("User actif :", employee.user.is_active)

        return employee


    @staticmethod
    def get_deleted_employee(employee_id):

        return (
            Employee.objects
            .select_related("user")
            .filter(
                id=employee_id,
                is_deleted=True
            )
            .first()
        )


    @staticmethod
    @transaction.atomic
    def restore_employee(employee):
        employee.is_deleted = False

        employee.user.is_active = True

        employee.user.save()

        employee.save()

        return employee


    @staticmethod
    def employee_statistics():

        queryset = Employee.objects.filter(
            is_deleted=False
        )

        return {

            "total_employees": queryset.count(),

            "male": queryset.filter(
                gender="MALE"
            ).count(),

            "female": queryset.filter(
                gender="FEMALE"
            ).count(),

            "active_users": User.objects.filter(
                is_active=True
            ).count(),
        }

    @staticmethod
    def get_statistics():
        employees = Employee.objects.select_related("user")

        employee_stats = employees.aggregate(
            total=Count("id"),
            active=Count(
                "id",
                filter=Q(is_deleted=False, user__is_active=True),
            ),
            deleted=Count(
                "id",
                filter=Q(is_deleted=True),
            ),
            male=Count(
                "id",
                filter=Q(
                    gender=Gender.MALE,
                    is_deleted=False,
                ),
            ),
            female=Count(
                "id",
                filter=Q(
                    gender=Gender.FEMALE,
                    is_deleted=False,
                ),
            ),
            single=Count(
                "id",
                filter=Q(
                    family_status=FamilyStatus.SINGLE,
                    is_deleted=False,
                ),
            ),
            married=Count(
                "id",
                filter=Q(
                    family_status=FamilyStatus.MARRIED,
                    is_deleted=False,
                ),
            ),
            divorced=Count(
                "id",
                filter=Q(
                    family_status=FamilyStatus.DIVORCED,
                    is_deleted=False,
                ),
            ),
            widowed=Count(
                "id",
                filter=Q(
                    family_status=FamilyStatus.WIDOWED,
                    is_deleted=False,
                ),
            ),
        )

        role_stats = (
            employees.filter(is_deleted=False)
            .values("user__role")
            .annotate(total=Count("id"))
        )

        roles = {
            role: 0
            for role, _ in UserRole.choices
        }

        for item in role_stats:
            roles[item["user__role"]] = item["total"]

        return {
            "employees": {
                "total": employee_stats["total"],
                "active": employee_stats["active"],
                "deleted": employee_stats["deleted"],
            },
            "gender": {
                "male": employee_stats["male"],
                "female": employee_stats["female"],
            },
            "family_status": {
                "single": employee_stats["single"],
                "married": employee_stats["married"],
                "divorced": employee_stats["divorced"],
                "widowed": employee_stats["widowed"],
            },
            "roles": roles,
        }