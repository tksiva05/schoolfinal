# Generated by Django 5.0 on 2024-01-02 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finalapp', '0007_studentadmission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentadmission',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='studentadmission',
            name='is_approved',
        ),
        migrations.RemoveField(
            model_name='studentadmission',
            name='rejection_reason',
        ),
    ]
