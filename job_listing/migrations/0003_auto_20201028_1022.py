# Generated by Django 3.1.1 on 2020-10-28 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_listing', '0002_auto_20201027_0751'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='work_duration',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='employment_status',
            field=models.CharField(choices=[('Part Time', 'Part Time'), ('Full Time', 'Full Time'), ('Freelance', 'Freelancer'), ('Internship', 'Internship'), ('Contract', 'Contract')], max_length=10),
        ),
    ]
