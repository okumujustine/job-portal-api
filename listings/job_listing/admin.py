from django.contrib import admin
from .models import Job, Category, ApplyJob, Contact

# Register your models here.

admin.site.register(Job)
admin.site.register(Category)
admin.site.register(ApplyJob)
admin.site.register(Contact)
