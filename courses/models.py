from datetime import timedelta

from django.core.exceptions import ValidationError
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
    course_programme = models.ManyToManyField('accounts.Programme')
    course_prerequisite = models.ForeignKey("self", blank=True, related_name="prerequisite_course",
                                            on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.course_code} {self.course_name}"


def get_joining_deadline():
    return timezone.now() + timedelta(days=20)


def get_session_end():
    return timezone.now() + timedelta(days=120)


class Session(models.Model):
    session_name = models.CharField(max_length=20,
                                    help_text="Please use the following format: <em>SPR-2022</em>.")

    session_start_date = models.DateField(help_text="Please use the following format: <em>YYYY-MM-DD</em>.",
                                          default=timezone.now)

    session_end_date = models.DateField(help_text="Please use the following format: <em>YYYY-MM-DD</em>.",
                                        default=get_session_end)

    programme = models.ForeignKey('accounts.Programme', on_delete=models.CASCADE,
                                  help_text="Select the programme for which the session is being created.")
    batch = models.OneToOneField('accounts.Batch', on_delete=models.CASCADE,
                                 help_text="Select the batch for which this session is being created.")
    joining_date = models.DateField(help_text="Set the start of course joining.", default=timezone.now)
    joining_deadline = models.DateField(help_text="Set the deadline of course joining for this session.",
                                        default=get_joining_deadline)
    courses_offered = models.ManyToManyField(Course, related_name="courses")

    def clean(self):
        super().clean()
        if not (self.session_start_date <= self.session_end_date):
            raise ValidationError('Invalid start and end session datetime')
        if not (self.joining_date <= self.joining_deadline):
            raise ValidationError('Invalid start and end joining datetime')

    def __str__(self):
        return self.session_name

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     Session.objects.all().update(joining_date=self.joining_date, joining_end_date=self.joining_end_date)
