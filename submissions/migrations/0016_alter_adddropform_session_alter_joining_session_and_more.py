# Generated by Django 4.0.3 on 2022-08-06 16:20

import courses.models
import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_alter_session_session_name'),
        ('submissions', '0015_alter_petition_expired_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adddropform',
            name='session',
            field=models.ForeignKey(default=courses.models.Session.get_latest_session, on_delete=django.db.models.deletion.CASCADE, to='courses.session'),
        ),
        migrations.AlterField(
            model_name='joining',
            name='session',
            field=models.ForeignKey(default=courses.models.Session.get_latest_session, on_delete=django.db.models.deletion.CASCADE, to='courses.session'),
        ),
        migrations.AlterField(
            model_name='petition',
            name='expired_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 21, 16, 20, 19, 29587, tzinfo=utc), help_text='Set the date and time when the petition will expire'),
        ),
        migrations.AlterField(
            model_name='petition',
            name='session',
            field=models.ForeignKey(default=courses.models.Session.get_latest_session, on_delete=django.db.models.deletion.CASCADE, to='courses.session'),
        ),
    ]