from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.pagination import DefaultPagination

from .filters import DepartmentFilter
from .models import Department
from .permissions import DepartmentPermission
from .serializers import (
    DepartmentListSerializer,
    DepartmentDetailSerializer,
    CreateDepartmentSerializer,
    UpdateDepartmentSerializer,
    DepartmentStatisticsSerializer,
)
from .services import DepartmentService
from .swagger import (
    department_list_docs,
    department_create_docs,
    department_detail_docs,
    department_update_docs,
    department_delete_docs,
    department_restore_docs,
    department_statistics_docs,
)


class DepartmentListCreateView(ListCreateAPIView):

    permission_classes = [
        IsAuthenticated,
        DepartmentPermission,
    ]

    pagination_class = DefaultPagination

    queryset = Department.objects.filter(
        is_deleted=False
    )

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = DepartmentFilter

    search_fields = [
        "name",
        "description",
    ]

    ordering_fields = [
        "name",
        "created_at",
    ]

    ordering = [
        "name",
    ]

    def get_serializer_class(self):

        if self.request.method == "POST":
            return CreateDepartmentSerializer

        return DepartmentListSerializer

    # HTTP METHODS
    @department_list_docs()
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @department_create_docs()
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # INTERNAL METHODS
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        department = DepartmentService.create(
            serializer.validated_data
        )

        return Response(
            DepartmentDetailSerializer(
                department
            ).data,
            status=status.HTTP_201_CREATED,
        )


class DepartmentDetailView(
    RetrieveUpdateDestroyAPIView
):

    permission_classes = [
        IsAuthenticated,
        DepartmentPermission,
    ]

    queryset = Department.objects.filter(
        is_deleted=False
    )

    # HTTP METHODS
    @department_detail_docs()
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @department_update_docs()
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @department_update_docs()
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @department_delete_docs()
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    # INTERNAL METHODS
    def get_serializer_class(self):

        if self.request.method in [
            "PUT",
            "PATCH",
        ]:
            return UpdateDepartmentSerializer

        return DepartmentDetailSerializer

    def update(self, request, *args, **kwargs):

        department = self.get_object()

        serializer = self.get_serializer(
            department,
            data=request.data,
            partial=request.method == "PATCH",
        )

        serializer.is_valid(
            raise_exception=True
        )

        DepartmentService.update(
            department,
            serializer.validated_data
        )

        return Response(
            DepartmentDetailSerializer(
                department
            ).data
        )

    def destroy(self, request, *args, **kwargs):

        department = self.get_object()

        DepartmentService.soft_delete(
            department
        )

        return Response(
            {
                "message": "Department deleted successfully."
            }
        )


class RestoreDepartmentView(APIView):

    permission_classes = [
        IsAuthenticated,
        DepartmentPermission,
    ]

    @department_restore_docs()
    def patch(self, request, pk):

        department = DepartmentService.get_deleted(pk)

        if not department:

            return Response(
                {
                    "detail": "Department not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        department = DepartmentService.restore(
            department
        )

        return Response(
            DepartmentDetailSerializer(
                department
            ).data
        )


class DepartmentStatisticsView(APIView):

    permission_classes = [
        IsAuthenticated,
        DepartmentPermission,
    ]

    @department_statistics_docs()
    def get(self, request):

        data = DepartmentService.get_statistics()

        serializer = DepartmentStatisticsSerializer(
            instance=data
        )

        return Response(
            serializer.data
        )