# Generated by Django 4.0.3 on 2022-03-13 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0017_course_offered_in_semester_session_session_year_and_more'),
        ('accounts', '0015_remove_studentprofile_course'),
        ('submissions', '0002_delete_joiningform'),
    ]

    operations = [
        migrations.CreateModel(
            name='JoiningForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending', help_text="Change status to 'Accepted' if Student is eligible or 'Rejected' if not", max_length=12)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('form_name', models.CharField(default='Joining Form', editable=False, max_length=30)),
                ('semester', models.PositiveSmallIntegerField(default=1)),
                ('course', models.ManyToManyField(blank=True, to='courses.course')),
                ('session', models.ForeignKey(help_text='Click above to get Session Info', on_delete=django.db.models.deletion.CASCADE, to='courses.session')),
                ('student', models.ForeignKey(help_text='Click above to get Student Info', on_delete=django.db.models.deletion.CASCADE, related_name='forms', to='accounts.studentprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
