from django.db import models
from django.contrib.auth.models import User
from authentication.models import CustomUser
from django.utils import timezone
from django.db.models.signals import pre_save

from listings.utils import unique_slug_generator


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Job(models.Model):

    STATUS = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    EXPERIENCE_STATUS = (
        ('month', 'Month'),
        ('year', 'Year'),
    )

    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Any', 'Any'),
    )

    JOB_TYPE = (
        ('Part Time', 'Part Time'),
        ('Full Time', 'Full Time'),
        ('Freelance', 'Freelancer'),
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
        max_length=10, choices=STATUS, default='published')
    gender = models.CharField(choices=GENDER, max_length=30, null=True)
    tag_one = models.CharField(max_length=100, null=True, blank=True)
    tag_two = models.CharField(max_length=100, null=True, blank=True)
    tag_three = models.CharField(max_length=100, null=True, blank=True)
    tag_four = models.CharField(max_length=100, null=True, blank=True)
    tag_five = models.CharField(max_length=100, null=True, blank=True)
    company_logo = models.ImageField(blank=True, upload_to='media', null=True)
    salary_range_from = models.CharField(max_length=100)
    salary_range_to = models.CharField(max_length=100, null=True, blank=True)
    salary_currency = models.CharField(max_length=100)
    employment_status = models.CharField(choices=JOB_TYPE, max_length=10)
    company_name = models.CharField(max_length=255, default="anonymous")
    company_location = models.CharField(max_length=255, default="anonymous")
    experience = models.CharField(max_length=100)
    vacancies = models.CharField(max_length=100)
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


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.email


class ApplyJob(models.Model):
    APPLICANT_STATUS = (
        ('sent', 'Sent'),
        ('recieved', 'Recieved'),
        ('rejected', 'Rejected'),
        ('approved', 'Approved'),
    )
    job_author = models.ForeignKey(
        to=CustomUser, on_delete=models.CASCADE, related_name='list_author')
    applicant = models.ForeignKey(
        to=CustomUser, on_delete=models.CASCADE, related_name='job_applicant')
    first_name = models.CharField(max_length=50)
    job = models.ForeignKey(
        to=Job, on_delete=models.CASCADE, related_name='job_relatioship')
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    resume_file = models.FileField(null=True)
    resume_text = models.TextField(null=True)
    status = models.CharField(
        max_length=10, choices=APPLICANT_STATUS, default='sent')

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.email}'
