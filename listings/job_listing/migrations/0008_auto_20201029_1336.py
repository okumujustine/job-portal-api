# Generated by Django 3.1.1 on 2020-10-29 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_listing', '0007_delete_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='profile_company_logo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]