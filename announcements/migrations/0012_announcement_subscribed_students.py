# Generated by Django 4.0.3 on 2022-07-20 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_studentprofile_phone_number'),
        ('announcements', '0011_remove_sendsms_batch_sendsms_batch'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='subscribed_students',
            field=models.ManyToManyField(blank=True, default=None, related_name='subscribed_announcements', to='accounts.studentprofile'),
        ),
    ]
