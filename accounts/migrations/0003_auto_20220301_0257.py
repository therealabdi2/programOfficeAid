# Generated by Django 3.2.8 on 2022-02-28 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20220301_0203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='department_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='programme',
            name='degree_name',
            field=models.CharField(max_length=50),
        ),
    ]
