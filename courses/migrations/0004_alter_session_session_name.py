# Generated by Django 4.0.3 on 2022-07-02 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_offeredcourses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='session_name',
            field=models.CharField(choices=[('Fall', 'Fall'), ('Spr', 'Spring'), ('Summer', 'Summer')], default='Fall', max_length=20),
        ),
    ]
