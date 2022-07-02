# Generated by Django 4.0.3 on 2022-07-01 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_studentprofile_phone_number'),
        ('courses', '0002_remove_session_batch_remove_session_courses_offered_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfferedCourses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.PositiveSmallIntegerField(blank=True, default=1, help_text='Designates the semester in which the courses are offered', null=True)),
                ('course', models.ManyToManyField(help_text='Select the course(s) to be offered', to='courses.course')),
                ('programme', models.ManyToManyField(help_text='Select the programme(s) the course(s) belong to', to='accounts.programme')),
            ],
        ),
    ]
