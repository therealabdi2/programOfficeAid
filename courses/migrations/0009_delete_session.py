# Generated by Django 4.0.3 on 2022-03-05 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_alter_coursecategory_options_session'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Session',
        ),
    ]