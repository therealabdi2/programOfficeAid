# Generated by Django 4.0.3 on 2022-03-05 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_remove_course_course_prerequisite_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_prerequisite',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prerequisite_course', to='courses.course'),
        ),
    ]
