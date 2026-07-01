from core.swagger import *

from .serializers import (
    EmployeeListSerializer,
    EmployeeDetailSerializer,
    CreateEmployeeSerializer,
    UpdateEmployeeSerializer,
    EmployeeStatisticsSerializer,
)


def employee_list_docs():
    return list_docs(
        tag="Employees",
        serializer=EmployeeListSerializer,
        description="""
        Retrieve the list of all active employees.

        Supports:
        - Pagination
        - Search
        - Filtering
        - Ordering
        """,
    )


def employee_create_docs():
    return create_docs(
        tag="Employees",
        request_serializer=CreateEmployeeSerializer,
        response_serializer=EmployeeDetailSerializer,
        description="""
        Create a new employee.

        The employee account is created automatically and linked to the employee profile.
        """,
    )


def employee_detail_docs():
    return detail_docs(
        tag="Employees",
        serializer=EmployeeDetailSerializer,
        description="""
        Retrieve detailed information about a specific employee.
        """,
    )


def employee_update_docs():
    return update_docs(
        tag="Employees",
        request_serializer=UpdateEmployeeSerializer,
        response_serializer=EmployeeDetailSerializer,
        description="""
        Update an existing employee's information.
        """,
    )


def employee_delete_docs():
    return delete_docs(
        tag="Employees",
        description="""
        Soft delete an employee.

        The employee record remains in the database and can be restored later.
        The associated user account is automatically deactivated.
        """,
    )


def employee_restore_docs():
    return restore_docs(
        tag="Employees",
        serializer=EmployeeDetailSerializer,
        description="""
        Restore a previously deleted employee.

        The associated user account is automatically reactivated.
        """,
    )


def employee_statistics_docs():
    return statistics_docs(
        tag="Employees",
        serializer=EmployeeStatisticsSerializer,
        description="""
        Retrieve employee statistics.

        Includes:
        - Total employees
        - Active employees
        - Deleted employees
        - Gender distribution
        - Family status distribution
        """,
    )