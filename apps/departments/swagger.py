from core.swagger import *

from .serializers import (
    DepartmentListSerializer,
    DepartmentDetailSerializer,
    CreateDepartmentSerializer,
    UpdateDepartmentSerializer,
    DepartmentStatisticsSerializer,
)


def department_list_docs():
    return list_docs(
        tag="Departments",
        serializer=DepartmentListSerializer,
        description="""
        Retrieve the list of all active departments.

        Supports:
        - Pagination
        - Search
        - Filtering
        - Ordering
        """,
    )


def department_create_docs():
    return create_docs(
        tag="Departments",
        request_serializer=CreateDepartmentSerializer,
        response_serializer=DepartmentDetailSerializer,
        description="""
        Create a new department.
        """,
    )


def department_detail_docs():
    return detail_docs(
        tag="Departments",
        serializer=DepartmentDetailSerializer,
        description="""
        Retrieve detailed information about a specific department.
        """,
    )


def department_update_docs():
    return update_docs(
        tag="Departments",
        request_serializer=UpdateDepartmentSerializer,
        response_serializer=DepartmentDetailSerializer,
        description="""
        Update an existing department.
        """,
    )


def department_delete_docs():
    return delete_docs(
        tag="Departments",
        description="""
        Soft delete a department.

        The department remains stored in the database and can be restored later.
        """,
    )


def department_restore_docs():
    return restore_docs(
        tag="Departments",
        serializer=DepartmentDetailSerializer,
        description="""
        Restore a previously deleted department.
        """,
    )


def department_statistics_docs():
    return statistics_docs(
        tag="Departments",
        serializer=DepartmentStatisticsSerializer,
        description="""
        Retrieve department statistics.

        Includes:
        - Total departments
        - Active departments
        - Deleted departments
        """,
    )