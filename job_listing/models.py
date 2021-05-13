from django.db import models
from django.contrib.auth.models import User
from authentication.models import CustomUser, Profile
from django.utils import timezone
from django.db.models.signals import pre_save

from listings.utils import unique_slug_generator
from authentication.models import MainModel


class Category(MainModel, models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Job(MainModel, models.Model):

    STATUS = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    EXPERIENCE_STATUS = (
        ('month', 'Month'),
        ('year', 'Year')
    )

    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Any', 'Any')
    )

    JOB_TYPE = (
        ('Part Time', 'Part Time'),
        ('Full Time', 'Full Time'),
        ('Freelance', 'Freelancer'),
        ('Internship', 'Internship'),
        ('Contract', 'Contract')
    )

    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=250)
    dateline = models.DateField()
    description = models.TextField()
    slug = models.SlugField(max_length=250, null=True, blank=True)
    published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        to=CustomUser, on_delete=models.CASCADE, related_name='job_author')
    status = models.CharField(
        max_length=10, choices=STATUS, default='draft')
    gender = models.CharField(choices=GENDER, max_length=30, null=True)
    tag_one = models.CharField(max_length=100, null=True, blank=True)
    tag_two = models.CharField(max_length=100, null=True, blank=True)
    tag_three = models.CharField(max_length=100, null=True, blank=True)
    tag_four = models.CharField(max_length=100, null=True, blank=True)
    tag_five = models.CharField(max_length=100, null=True, blank=True)
    company_logo = models.ImageField(blank=True, upload_to='media', null=True)
    profile_company_logo = models.CharField(
        max_length=100, null=True, blank=True)
    salary_range_from = models.CharField(max_length=100)
    salary_range_to = models.CharField(max_length=100, null=True, blank=True)
    salary_currency = models.CharField(max_length=100)
    employment_status = models.CharField(choices=JOB_TYPE, max_length=10)
    company_name = models.CharField(max_length=255, default="anonymous")
    company_location = models.CharField(max_length=255, default="anonymous")
    experience = models.CharField(max_length=100)
    vacancies = models.CharField(max_length=100)
    work_duration = models.CharField(max_length=100, null=True, blank=True)
    application_link = models.URLField(max_length=200, null=True, blank=True)
    experience_status = models.CharField(
        choices=EXPERIENCE_STATUS, max_length=100)

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_generator, sender=Job)


class ApplyJob(MainModel, models.Model):
    APPLICANT_STATUS = (
        ('sent', 'Sent'),
        ('recieved', 'Recieved'),
        ('rejected', 'Rejected'),
        ('approved', 'Approved')
    )
    applicant = models.ForeignKey(
        to=CustomUser, on_delete=models.CASCADE, related_name='job_applicant')
    first_name = models.CharField(max_length=50)
    job = models.ForeignKey(
        to=Job, on_delete=models.CASCADE, related_name='job_relatioship')
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    resume_file = models.FileField(null=True, blank=True)
    resume_text = models.TextField(null=True, blank=True)
    profile_text_resume = models.CharField(
        max_length=50, null=True, blank=True)
    profile_resume = models.CharField(max_length=255, null=True, blank=True)
    # employee_profile_resume = models.ForeignKey(
    #     to=Profile, on_delete=models.CASCADE, related_name='profile_applicant')
    status = models.CharField(
        max_length=10, choices=APPLICANT_STATUS, default='sent')
    application_created_at = models.DateTimeField(default=timezone.now)
    application_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.email} applied for {self.job.title}'
