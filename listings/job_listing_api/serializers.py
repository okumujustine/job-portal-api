from rest_framework import serializers
from job_listing.models import Job, ApplyJob


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Job


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
