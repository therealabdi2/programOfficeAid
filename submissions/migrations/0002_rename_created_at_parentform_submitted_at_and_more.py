# Generated by Django 4.0.3 on 2022-03-13 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parentform',
            old_name='created_at',
            new_name='submitted_at',
        ),
        migrations.AlterField(
            model_name='joiningform',
            name='semester',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
