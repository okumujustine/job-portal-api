
from django.urls import path
from .views import JobList, JobDetail, JobFilterView, LatestJobs, ApplyJob

app_name = "job_listing_api"


urlpatterns = [
    path('', JobList.as_view(), name='listcreate'),
    path('<int:pk>/', JobDetail.as_view(), name='detailcreate'),
    path('filter/', JobFilterView.as_view(), name='job-filter'),
    path('latest/', LatestJobs.as_view(), name='latest-jobs'),
    path('apply/', ApplyJob.as_view(), name="apply-jobs"),
]
