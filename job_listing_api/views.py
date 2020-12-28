from rest_framework import generics, views
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Count

from .pagination import JobPageNumberPagination, JobApplicationsPageNumberPagination, EmployeeJobApplicationsPageNumberPagination
from job_listing.models import Job, ApplyJob, Category
from .serializers import (JobSerializer, ApplyJobSerializer, UserAppliedJobSerializer,
                          GetUserApplicationsSerializer, JobCategorySerializer, GetFilteredJobsSerializer)


# OPTION 1
# TODO: change this -> only logged in users should add jobs
class JobListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = JobSerializer
    queryset = Job.objects.all()

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user, status='published')


class LatestJobsView(generics.ListAPIView):
    queryset = Job.objects.filter(
        status='published').order_by('-published')[:4]
    serializer_class = JobSerializer


class JobCategoriesView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = JobCategorySerializer


class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


def is_valid_queryparam(param):
    return param != '' and param is not None

# job filter view starts from here


def jobs_filter(request):
    qs = Job.objects.filter(status='published').annotate(
        application_count=Count('job_relatioship'))
    title_contains_query = request.GET.get('title')
    title_contains_type = request.GET.get('type')

    if is_valid_queryparam(title_contains_query):
        qs = qs.filter(title__icontains=title_contains_query)

    elif is_valid_queryparam(title_contains_type):
        qs = qs.filter(employment_status__icontains=title_contains_type)
    return qs


class JobFilterView(generics.ListAPIView):
    serializer_class = GetFilteredJobsSerializer
    pagination_class = JobPageNumberPagination

    def get_queryset(self):
        qs = jobs_filter(self.request)
        return qs


# admin job requests view starts from here

def admin_user_jobs_filter(request):
    qs = Job.objects.filter(author=request.user).annotate(
        application_count=Count('job_relatioship')).order_by('-published')
    title_contains_query = request.GET.get('title')

    if is_valid_queryparam(title_contains_query):
        qs = qs.filter(title__icontains=title_contains_query)

    return qs


class AdminUserJobView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = GetFilteredJobsSerializer
    pagination_class = JobApplicationsPageNumberPagination

    def get_queryset(self):
        qs = admin_user_jobs_filter(self.request)
        return qs


class EmployerStatsView(views.APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None):
        posted_jobs_count = Job.objects.filter(
            author=self.request.user).count()
        job_applications_count = ApplyJob.objects.filter(
            job__author=self.request.user).count()
        return Response({'posted_jobs_count': posted_jobs_count, 'job_applications_count': job_applications_count})


class ApplyJobView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ApplyJobSerializer
    queryset = ApplyJob.objects.all()

    def perform_create(self, serializer):
        return serializer.save(applicant=self.request.user)


class EmployeeAppliedJobView(views.APIView):
    serializer_class = UserAppliedJobSerializer

    def post(self, request, format=None):
        serializer = UserAppliedJobSerializer(data=request.data)
        if serializer.is_valid():
            job_id = serializer.data.get("job")
            applicant_id = serializer.data.get("applicant")
            userJob = ApplyJob.objects.filter(
                job=job_id, applicant=applicant_id)
            user_email = [user.email for user in userJob]
            return Response(user_email, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetEmployeeApplicationsView(generics.ListCreateAPIView):
    pagination_class = EmployeeJobApplicationsPageNumberPagination
    serializer_class = GetUserApplicationsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        return ApplyJob.objects.filter(applicant=self.request.user).order_by('-application_created_at')


class GetJobApplicationsView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GetUserApplicationsSerializer

    def get_queryset(self):
        request_contains_id = self.request.GET.get('id')
        if is_valid_queryparam(request_contains_id):
            print(request_contains_id)

        qs = queryset = ApplyJob.objects.filter(
            job=request_contains_id).order_by('-application_created_at')
        return qs
