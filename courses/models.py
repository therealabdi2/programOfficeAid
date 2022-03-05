from django.db import models


# Create your models here.


class CourseCategory(models.Model):
    course_category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.course_category_name


class CourseType(models.Model):
    course_type_name = models.CharField(max_length=30)
    course_type_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.course_type_name


class Course(models.Model):
    course_name = models.CharField(max_length=50)
    course_code = models.CharField(max_length=7)
    course_details = models.TextField(blank=True)
    course_credit = models.IntegerField(default=3)
    course_type = models.ForeignKey(CourseType, on_delete=models.CASCADE)
    course_programme = models.ManyToManyField('accounts.Programme')
    course_prerequisite = models.ManyToManyField("self", blank=True, symmetrical=False,
                                                 related_name="prerequisite_course")

    def __str__(self):
        return self.course_name
