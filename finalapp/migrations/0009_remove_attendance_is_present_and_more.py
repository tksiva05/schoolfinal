# Generated by Django 4.2.7 on 2024-01-05 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finalapp', '0008_remove_studentadmission_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='is_present',
        ),
        migrations.AlterField(
            model_name='attendance',
            name='present_status',
            field=models.CharField(choices=[('Present', 'Present'), ('Absent', 'Absent')], max_length=10),
        ),
    ]
