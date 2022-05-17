import datetime
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


# Create your models here.
class CourseCategory(models.Model):
    course_category_name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Course Categories'

    def __str__(self):
        return self.course_category_name


class CourseType(models.Model):
    course_type_name = models.CharField(max_length=80)
    course_type_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    required_credits = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.course_type_name


class Course(models.Model):
    course_name = models.CharField(max_length=50, unique=True)
    course_code = models.CharField(max_length=15, unique=True)
    course_details = models.TextField(blank=True, null=True)
    course_credit = models.IntegerField(default=3)
    course_type = models.ForeignKey(CourseType, on_delete=models.CASCADE)
    course_programme = models.ManyToManyField('accounts.Programme',
                                              help_text='Select the programme(s) this course belongs to')

    course_prerequisite = models.ForeignKey("self", blank=True, related_name="prerequisite_course",
                                            on_delete=models.CASCADE, null=True,
                                            help_text="Select the prerequisite of the course")

    offered_in_semester = models.PositiveSmallIntegerField(default=1, blank=True, null=True,
                                                           help_text="Designates the semester in which the course is "
                                                                     "offered")

    def __str__(self):
        return f"{self.course_code} {self.course_name}"


def get_joining_deadline():
    return timezone.now() + timedelta(days=25)


def get_session_end():
    return timezone.now() + timedelta(days=120)


class Session(models.Model):
    SESSION_CHOICES = (
        ('Fall', 'Fall'),
        ('Spr', 'Spring'),
        ('Summer', 'Summer'),
    )

    session_name = models.CharField(max_length=20, choices=SESSION_CHOICES,
                                    help_text="Please use the following format: <em>SPR-2022</em>.", default='Fall')

    session_start_date = models.DateField(help_text="Please use the following format: <em>YYYY-MM-DD</em>.",
                                          default=timezone.now)

    session_year = models.PositiveSmallIntegerField(default=timezone.now().year, validators=[
        RegexValidator(
            regex="^20[1-9][0-9]$",
            message='Please enter a valid year'
        ),
    ], help_text="Please use the following format: <em>20XX</em>.")

    session_end_date = models.DateField(help_text="Please use the following format: <em>YYYY-MM-DD</em>.",
                                        default=get_session_end)

    joining_deadline = models.DateField(default=get_joining_deadline,
                                        help_text="Please use the following format: <em>YYYY-MM-DD</em>.")

    def is_deadline(self):
        return self.joining_deadline <= datetime.datetime.today().date()

    # tests to validate dates
    def valid_session_date(self):
        return self.session_start_date <= timezone.now() <= self.session_end_date

    def clean(self):
        super().clean()
        if not (self.session_start_date <= self.session_end_date):
            raise ValidationError('Invalid start and end session datetime')

    def __str__(self):
        return f"{self.session_name} {self.session_year}"
