# Generated by Django 4.0.3 on 2022-05-08 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_remove_session_batch_remove_session_courses_offered_and_more'),
        ('submissions', '0002_remove_joiningform_form_name_joiningform_fee_slip_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joiningform',
            name='course',
            field=models.ManyToManyField(related_name='courses', to='courses.course'),
        ),
        migrations.AlterField(
            model_name='joiningform',
            name='fee_slip',
            field=models.ImageField(blank=True, help_text='<strong>Note:</strong> Your form might get rejected if your fee slip is not attached', null=True, upload_to='forms/'),
        ),
    ]