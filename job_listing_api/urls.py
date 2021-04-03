
from django.urls import path
from .views import (JobListView, JobDetailView, JobFilterView, LatestJobsView, ApplyJobView, EmployeeAppliedJobView,
                    GetEmployeeApplicationsView, JobCategoriesView, AdminUserJobView, GetJobApplicationsView, EmployerStatsView)

app_name = "job_listing_api"


urlpatterns = [
    path('create/', JobListView.as_view(), name='listcreate'),
    path('categories/', JobCategoriesView.as_view(), name='job-categories'),
    path('<int:pk>/', JobDetailView.as_view(), name='detailcreate'),
    path('filter/', JobFilterView.as_view(), name='job-filter'),
    path('latest/', LatestJobsView.as_view(), name='latest-jobs'),
    path('apply/', ApplyJobView.as_view(), name="apply-jobs"),
    path('userapplied/', EmployeeAppliedJobView.as_view(), name="user-applied"),
    path('admin/userjobs/', AdminUserJobView.as_view(), name="admin-user-jobs"),
    path('employers/stats/', EmployerStatsView.as_view(), name="employers-stats"),
    path('userapplications/', GetEmployeeApplicationsView.as_view(),
         name="get-user-applications"),
    path('jobapplications/', GetJobApplicationsView.as_view(),
         name="get-job-applications"),
]
