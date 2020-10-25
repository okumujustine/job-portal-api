from rest_framework import serializers
from job_listing.models import Job, ApplyJob, Category


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"
        extra_kwargs = {'author': {'required': False}}


class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Category


class ApplyJobSerializer(serializers.ModelSerializer):
    class Meta():
        model = ApplyJob
        fields = ('resume_file', 'first_name',
                  'last_name', 'email', 'job')


class UserAppliedJobSerializer(serializers.Serializer):
    job = serializers.IntegerField()
    applicant = serializers.IntegerField()


class GetUserApplicationsSerializer(serializers.ModelSerializer):
    class Meta():
        model = ApplyJob
        fields = "__all__"
