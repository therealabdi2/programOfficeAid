# Generated by Django 4.0.3 on 2022-03-05 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0003_rename_user_studentprofile_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_category_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='CourseType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_type_name', models.CharField(max_length=30)),
                ('course_type_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.coursecategory')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=50)),
                ('course_code', models.CharField(max_length=7)),
                ('course_details', models.TextField(blank=True)),
                ('course_credit', models.IntegerField(default=3)),
                ('course_prerequisite', models.ManyToManyField(blank=True, related_name='prerequisite_course', to='courses.course')),
                ('course_programme', models.ManyToManyField(to='accounts.programme')),
                ('course_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.coursetype')),
            ],
        ),
    ]