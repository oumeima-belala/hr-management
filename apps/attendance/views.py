from rest_framework import status, filters
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from core.pagination import DefaultPagination

from .models import Attendance
from .serializers import (
    AttendanceListSerializer,
    AttendanceDetailSerializer,
    CreateAttendanceSerializer,
    UpdateAttendanceSerializer,
    AttendanceStatisticsSerializer,
    CheckInSerializer,
    CheckOutSerializer,
    AttendanceDashboardSerializer,
)
from .services import AttendanceService
from .permissions import AttendancePermission
from .filters import AttendanceFilter

from .swagger import (
    attendance_list_docs,
    attendance_create_docs,
    attendance_detail_docs,
    attendance_update_docs,
    attendance_delete_docs,
    attendance_restore_docs,
    attendance_statistics_docs,
    attendance_check_in_docs,
    attendance_check_out_docs,
    attendance_dashboard_docs,
)


class AttendanceListCreateView(ListCreateAPIView):

    permission_classes = [
        IsAuthenticated,
        AttendancePermission,
    ]

    pagination_class = DefaultPagination

    queryset = Attendance.objects.select_related(
        "employee",
        "employee__user",
    ).filter(
        is_deleted=False
    )

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = AttendanceFilter

    search_fields = [
        "employee__first_name",
        "employee__last_name",
        "employee__user__email",
    ]

    ordering_fields = [
        "check_in",
        "worked_hours",
        "created_at",
    ]

    ordering = [
        "-check_in",
    ]

    def get_serializer_class(self):

        if self.request.method == "POST":
            return CreateAttendanceSerializer

        return AttendanceListSerializer

    @attendance_list_docs()
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @attendance_create_docs()
    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        attendance = AttendanceService.create_attendance(
            serializer.validated_data
        )

        return Response(
            AttendanceDetailSerializer(
                attendance
            ).data,
            status=status.HTTP_201_CREATED,
        )


class AttendanceDetailView(
    RetrieveUpdateDestroyAPIView
):

    permission_classes = [
        IsAuthenticated,
        AttendancePermission,
    ]

    queryset = Attendance.objects.select_related(
        "employee",
        "employee__user",
    ).filter(
        is_deleted=False
    )

    def get_serializer_class(self):

        if self.request.method in [
            "PUT",
            "PATCH",
        ]:
            return UpdateAttendanceSerializer

        return AttendanceDetailSerializer

    @attendance_detail_docs()
    def get(self, request, *args, **kwargs):
        return self.retrieve(
            request,
            *args,
            **kwargs
        )

    @attendance_update_docs()
    def put(self, request, *args, **kwargs):
        return self.update(
            request,
            *args,
            **kwargs
        )

    @attendance_update_docs()
    def patch(self, request, *args, **kwargs):
        return self.update(
            request,
            *args,
            **kwargs
        )

    def update(self, request, *args, **kwargs):

        attendance = self.get_object()

        serializer = self.get_serializer(
            attendance,
            data=request.data,
            partial=request.method == "PATCH",
        )

        serializer.is_valid(
            raise_exception=True
        )

        attendance = AttendanceService.update_attendance(
            attendance,
            serializer.validated_data,
        )

        return Response(
            AttendanceDetailSerializer(
                attendance
            ).data
        )

    @attendance_delete_docs()
    def delete(self, request, *args, **kwargs):
        return self.destroy(
            request,
            *args,
            **kwargs
        )

    def destroy(self, request, *args, **kwargs):

        attendance = self.get_object()

        AttendanceService.soft_delete(
            attendance
        )

        return Response(
            {
                "message":
                    "Attendance deleted successfully."
            }
        )


class RestoreAttendanceView(APIView):

    permission_classes = [
        IsAuthenticated,
        AttendancePermission,
    ]

    @attendance_restore_docs()
    def patch(self, request, pk):

        attendance = AttendanceService.get_deleted(
            pk
        )

        if not attendance:
            return Response(
                {
                    "detail":
                        "Attendance not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        attendance = AttendanceService.restore(
            attendance
        )

        return Response(
            AttendanceDetailSerializer(
                attendance
            ).data
        )


class AttendanceStatisticsView(APIView):

    permission_classes = [
        IsAuthenticated,
        AttendancePermission,
    ]

    @attendance_statistics_docs()
    def get(self, request):

        data = AttendanceService.get_statistics()

        serializer = AttendanceStatisticsSerializer(
            data
        )

        return Response(
            serializer.data
        )


class CheckInView(APIView):

    permission_classes = [
        IsAuthenticated,
        AttendancePermission,
    ]

    @attendance_check_in_docs()
    def post(self, request):

        serializer = CheckInSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        attendance = AttendanceService.check_in(
            serializer.validated_data["employee"]
        )

        return Response(
            AttendanceDetailSerializer(
                attendance
            ).data,
            status=status.HTTP_201_CREATED,
        )


class CheckOutView(APIView):

    permission_classes = [
        IsAuthenticated,
        AttendancePermission,
    ]

    @attendance_check_out_docs()
    def patch(self, request):

        serializer = CheckOutSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        attendance = AttendanceService.check_out(
            serializer.validated_data["employee"]
        )

        return Response(
            AttendanceDetailSerializer(
                attendance
            ).data
        )


class AttendanceDashboardView(APIView):

    permission_classes = [
        IsAuthenticated,
        AttendancePermission,
    ]

    @attendance_dashboard_docs()
    def get(self, request):

        data = AttendanceService.get_dashboard()

        serializer = AttendanceDashboardSerializer(data)

        return Response(serializer.data)