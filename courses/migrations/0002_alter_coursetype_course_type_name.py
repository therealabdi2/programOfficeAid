# Generated by Django 4.0.3 on 2022-03-05 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursetype',
            name='course_type_name',
            field=models.CharField(max_length=80),
        ),
    ]
