from rest_framework import status
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView,)
from rest_framework.response import Response
from core.pagination import DefaultPagination
from .models import Employee
from .serializers import (EmployeeListSerializer, EmployeeDetailSerializer, CreateEmployeeSerializer,
                          UpdateEmployeeSerializer, EmployeeStatisticsSerializer)
from .services import EmployeeService
from .permissions import EmployeePermission
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import EmployeeFilter
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .swagger import (employee_list_docs, employee_create_docs, employee_detail_docs, employee_update_docs,
                      employee_delete_docs, employee_restore_docs, employee_statistics_docs)

class EmployeeListCreateView(ListCreateAPIView):

    permission_classes = [IsAuthenticated, EmployeePermission,]
    pagination_class = DefaultPagination
    queryset = Employee.objects.select_related("user").filter(is_deleted=False)

    filter_backends = [ DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,]
    filterset_class = EmployeeFilter
    search_fields = ["first_name", "last_name", "phone_number", "social_security_number", "user__email",]

    ordering_fields = ["created_at", "last_name", "first_name",]
    ordering = ["last_name",]

    @employee_create_docs()
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateEmployeeSerializer

        return EmployeeListSerializer

    @employee_list_docs()
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        employee = EmployeeService.create_employee(
            serializer.validated_data
        )

        response_serializer = EmployeeDetailSerializer(employee)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )



class EmployeeDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, EmployeePermission,]
    queryset = Employee.objects.select_related("user").filter(is_deleted=False)

    @employee_detail_docs()
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @employee_update_docs()
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @employee_update_docs()
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @employee_delete_docs()
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return UpdateEmployeeSerializer

        return EmployeeDetailSerializer

    def update(self, request, *args, **kwargs):
        employee = self.get_object()

        serializer = self.get_serializer(
            employee,
            data=request.data,
            partial=request.method == "PATCH",
        )

        serializer.is_valid(raise_exception=True)

        employee = EmployeeService.update(
            employee,
            serializer.validated_data
        )

        return Response(
            EmployeeDetailSerializer(employee).data
        )

    def destroy(self, request, *args, **kwargs):
        employee = self.get_object()

        EmployeeService.soft_delete(employee)

        return Response(
            {
                "message": "Employee deleted successfully."
            },
            status=status.HTTP_200_OK
        )



class RestoreEmployeeView(APIView):

    permission_classes = [IsAuthenticated, EmployeePermission,]

    @employee_restore_docs()
    def patch(self, request, pk):
        employee = EmployeeService.get_deleted(pk)

        if not employee:
            return Response(
                {
                    "detail": "Employee not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        employee = EmployeeService.restore(
            employee
        )

        serializer = EmployeeDetailSerializer(
            employee
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class EmployeeStatisticsView(APIView):

    permission_classes = [IsAuthenticated, EmployeePermission,]

    @employee_statistics_docs()
    def get(self, request):
        data = EmployeeService.get_statistics()

        serializer = EmployeeStatisticsSerializer(instance=data)

        return Response(serializer.data)