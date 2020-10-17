from rest_framework import serializers
from job_listing.models import Job


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id', 
            'title', 
            'category', 
            'description', 
            'author', 
            'dateline', 
            'company_name',
            'company_location', 
            'published', 
            'status', 
            'tag_one', 
            'tag_two', 
            'tag_three', 
            'tag_four', 
            'tag_five', 
            'company_logo',
            'salary_range_from',
            'salary_range_to',
            'salary_currency',
            'employment_status',
            'company_name',
            'company_location',
            'experience',
            'vacancies',
            'experience_status'
        )
        model = Job

