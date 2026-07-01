from django.urls import path

from .views import (
    AttendanceListCreateView,
    AttendanceDetailView,
    RestoreAttendanceView,
    AttendanceStatisticsView,
    CheckInView, CheckOutView,
    AttendanceDashboardView
)

urlpatterns = [
    path("", AttendanceListCreateView.as_view(), name="attendance-list-create",),
    path("<int:pk>/", AttendanceDetailView.as_view(), name="attendance-detail",),
    path("<int:pk>/restore/", RestoreAttendanceView.as_view(), name="attendance-restore"),
    path("statistics/", AttendanceStatisticsView.as_view(), name="attendance-statistics"),
    path("check-in/", CheckInView.as_view(), name="attendance-check-in"),
    path("check-out/", CheckOutView.as_view(), name="attendance-check-out"),
    path("dashboard/", AttendanceDashboardView.as_view(), name="attendance-dashboard"),
]