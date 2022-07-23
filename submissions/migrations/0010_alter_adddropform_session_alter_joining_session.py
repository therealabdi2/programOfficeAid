# Generated by Django 4.0.3 on 2022-07-23 13:55

from django.db import migrations, models
import django.db.models.deletion
import submissions.models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_alter_session_session_name'),
        ('submissions', '0009_alter_joining_student_adddropform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adddropform',
            name='session',
            field=models.ForeignKey(default=submissions.models.get_latest_session, on_delete=django.db.models.deletion.CASCADE, to='courses.session'),
        ),
        migrations.AlterField(
            model_name='joining',
            name='session',
            field=models.ForeignKey(default=submissions.models.get_latest_session, on_delete=django.db.models.deletion.CASCADE, to='courses.session'),
        ),
    ]
