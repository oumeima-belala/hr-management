from django.urls import path
from .views import EmployeeListCreateView, EmployeeDetailView, RestoreEmployeeView, EmployeeStatisticsView

urlpatterns = [
    path("", EmployeeListCreateView.as_view(), name="employee-list-create"),
    path("statistics/", EmployeeStatisticsView.as_view(), name="employee-statistics"),
    path("<int:pk>/restore", RestoreEmployeeView.as_view(), name="employee-restore"),
    path("<int:pk>/", EmployeeDetailView.as_view(), name="employee-detail"),
]