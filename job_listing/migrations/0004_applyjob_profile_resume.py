# Generated by Django 3.1.1 on 2020-10-28 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_listing', '0003_auto_20201028_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='applyjob',
            name='profile_resume',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
