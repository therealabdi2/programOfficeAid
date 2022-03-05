from django.db import models


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


class Session(models.Model):
    session_name = models.CharField(max_length=20,
                                    help_text="Please use the following format: <em>SPR-2022</em>.")
    session_start_date = models.DateField(help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    session_end_date = models.DateField(help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    programme = models.ForeignKey('accounts.Programme', on_delete=models.CASCADE)
    batch = models.OneToOneField('accounts.Batch', on_delete=models.CASCADE)
    courses_offered = models.ManyToManyField(Course, related_name="courses")

    def __str__(self):
        return self.session_name
