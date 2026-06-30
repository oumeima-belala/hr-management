from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)

from .serializers import (
    CreateEmployeeSerializer,
    EmployeeDetailSerializer,
    EmployeeListSerializer,
    EmployeeStatisticsSerializer,
    UpdateEmployeeSerializer,
)


def employee_list_docs():

    return extend_schema(
        tags=["Employees"],

        summary="List employees",

        description="""
Retrieve a paginated list of employees.

This endpoint supports:

- Pagination
- Search
- Ordering
- Filtering
""",

        parameters=[

            OpenApiParameter(
                name="page",
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Page number.",
            ),

            OpenApiParameter(
                name="page_size",
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Number of employees per page.",
            ),

            OpenApiParameter(
                name="search",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Search by first name, last name, email, phone number or social security number.",
            ),

            OpenApiParameter(
                name="ordering",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Ordering field.",
            ),

            OpenApiParameter(
                name="gender",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
            ),

            OpenApiParameter(
                name="family_status",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
            ),

            OpenApiParameter(
                name="role",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
            ),

            OpenApiParameter(
                name="is_active",
                type=bool,
                location=OpenApiParameter.QUERY,
                required=False,
            ),

        ],

        responses={
            200: EmployeeDetailSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided."),
            403: OpenApiResponse(description="Permission denied."),
        },
    )



def employee_create_docs():

    return extend_schema(
        tags=["Employees"],
        summary="Create employee",
        description="Create a new employee and its associated user account.",
        request=CreateEmployeeSerializer,
        responses={
            201: EmployeeDetailSerializer,
            400: OpenApiResponse(description="Validation error."),
            401: OpenApiResponse(description="Authentication required."),
            403: OpenApiResponse(description="Permission denied."),
        },
    )


def employee_detail_docs():

    return extend_schema(
        tags=["Employees"],
        summary="Retrieve employee",
        description="Retrieve employee details by ID.",
        responses={
            200: EmployeeDetailSerializer,
            404: OpenApiResponse(description="Employee not found."),
        },
    )


def employee_update_docs():

    return extend_schema(
        tags=["Employees"],
        summary="Update employee",
        description="Update an existing employee.",
        request=UpdateEmployeeSerializer,
        responses={
            200: EmployeeDetailSerializer,
            400: OpenApiResponse(description="Validation error."),
            404: OpenApiResponse(description="Employee not found."),
        },
    )


def employee_delete_docs():

    return extend_schema(
        tags=["Employees"],
        summary="Delete employee",
        description="Soft delete an employee.",
        responses={
            200: OpenApiResponse(
                description="Employee deleted successfully."
            ),
            404: OpenApiResponse(
                description="Employee not found."
            ),
        },
    )



def employee_restore_docs():

    return extend_schema(
        tags=["Employees"],
        summary="Restore employee",
        description="Restore a previously deleted employee.",
        responses={
            200: EmployeeDetailSerializer,
            404: OpenApiResponse(
                description="Employee not found."
            ),
        },
    )


def employee_statistics_docs():

    return extend_schema(
        tags=["Employees"],
        summary="Employees statistics",
        description="Retrieve dashboard statistics about employees.",
        responses={
            200: EmployeeStatisticsSerializer,
        },
    )