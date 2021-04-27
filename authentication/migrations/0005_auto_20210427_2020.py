# Generated by Django 3.1.7 on 2021-04-27 20:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20210427_2012'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AddField(
            model_name='profile',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='profile',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]