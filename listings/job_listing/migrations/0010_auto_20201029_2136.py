# Generated by Django 3.1.1 on 2020-10-29 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_listing', '0009_auto_20201029_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applyjob',
            name='profile_resume',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
