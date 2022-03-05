# Generated by Django 4.0.3 on 2022-03-05 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_alter_coursetype_course_type_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='course_prerequisite',
        ),
        migrations.AddField(
            model_name='course',
            name='course_prerequisite',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prerequisite_course', to='courses.course'),
        ),
    ]