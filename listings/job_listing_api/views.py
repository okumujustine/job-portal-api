from rest_framework import generics, views
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from job_listing.models import Job
from .serializers import JobSerializer, ApplyJobSerializer


# OPTION 1
# TODO: change this -> only logged in users should add jobs
class JobList(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class LatestJobs(generics.ListAPIView):
    queryset = Job.objects.all().order_by('-published')[:4]
    serializer_class = JobSerializer


class JobDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


def is_valid_queryparam(param):
    return param != '' and param is not None


def filter(request):
    qs = Job.objects.all()
    title_contains_query = request.GET.get('title')
    title_contains_type = request.GET.get('type')

    if is_valid_queryparam(title_contains_query):
        qs = qs.filter(title__icontains=title_contains_query)

    elif is_valid_queryparam(title_contains_type):
        qs = qs.filter(employment_status__icontains=title_contains_type)
    return qs


class JobFilterView(generics.ListAPIView):
    serializer_class = JobSerializer

    def get_queryset(self):
        qs = filter(self.request)
        return qs


class ApplyJob(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ApplyJobSerializer

    def perform_create(self, serializer):
        return serializer.save(applicant=self.request.user)


# class ApplyJob(views.APIView):
#     permission_classes = [IsAuthenticated, ]
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, *args, **kwargs):
#         file_serializer = ApplyJobSerializer(data=request.data)
#         if file_serializer.is_valid():
#             file_serializer.save()
#             return Response(file_serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
