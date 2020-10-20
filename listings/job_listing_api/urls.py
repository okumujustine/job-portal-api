
from django.urls import path
from .views import JobListView, JobDetailView, JobFilterView, LatestJobsView, ApplyJobView, UserAppliedJobView

app_name = "job_listing_api"


urlpatterns = [
    path('', JobListView.as_view(), name='listcreate'),
    path('<int:pk>/', JobDetailView.as_view(), name='detailcreate'),
    path('filter/', JobFilterView.as_view(), name='job-filter'),
    path('latest/', LatestJobsView.as_view(), name='latest-jobs'),
    path('apply/', ApplyJobView.as_view(), name="apply-jobs"),
    path('userapplied/', UserAppliedJobView.as_view(), name="user-applied"),
]
