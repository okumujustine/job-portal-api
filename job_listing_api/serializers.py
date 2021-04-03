from rest_framework import serializers
from job_listing.models import Job, ApplyJob, Category


class GetFilteredJobsSerializer(serializers.ModelSerializer):

    application_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "dateline",
            "description",
            "slug",
            "published",
            "status",
            "gender",
            "tag_one",
            "tag_two",
            "tag_three",
            "tag_four",
            "tag_five",
            "company_logo",
            "salary_range_from",
            "salary_range_to",
            "salary_currency",
            "employment_status",
            "company_name",
            "company_location",
            "experience",
            "vacancies",
            "experience_status",
            "author",
            "category",
            "application_count",
            "work_duration"
        ]


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
                  'last_name', 'email', 'job', 'profile_resume')


class UserAppliedJobSerializer(serializers.Serializer):
    job = serializers.IntegerField()
    applicant = serializers.IntegerField()


class GetUserApplicationsSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)

    class Meta():
        model = ApplyJob
        fields = [
            'id',
            'applicant',
            'first_name',
            'job',
            'last_name',
            'email',
            'resume_file',
            'resume_text',
            'profile_resume',
            'status',
            'application_created_at',
            'application_updated',
        ]
