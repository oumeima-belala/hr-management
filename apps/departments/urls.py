from django.urls import path

from .views import (
    DepartmentListCreateView,
    DepartmentDetailView,
    RestoreDepartmentView,
    DepartmentStatisticsView,
)

urlpatterns = [
    path("", DepartmentListCreateView.as_view(), name="department-list-create",),
    path("statistics/", DepartmentStatisticsView.as_view(), name="department-statistics",),
    path("<int:pk>/restore/", RestoreDepartmentView.as_view(), name="department-restore",),
    path("<int:pk>/", DepartmentDetailView.as_view(), name="department-detail",),
]