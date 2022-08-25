# Generated by Django 4.0.3 on 2022-08-15 15:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0018_alter_petition_expired_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petition',
            name='expired_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 30, 15, 14, 26, 6144, tzinfo=utc), help_text='Set the date and time when the petition will expire'),
        ),
    ]