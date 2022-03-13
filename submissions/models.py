from django.db import models
# Create your models here.
from polymorphic.models import PolymorphicModel

from courses.models import Course, Session


class ParentForm(PolymorphicModel):
    STATUS = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )

    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE, related_name='forms',
                                help_text="Click above to get Student Info")
    form_status = models.CharField(max_length=12, choices=STATUS, default='Pending',
                                   help_text="Change status to 'Accepted' if Student is eligible or 'Rejected' if not")
    submitted_at = models.DateTimeField(auto_now_add=True, )


class JoiningForm(ParentForm):
    form_name = models.CharField(max_length=30, default='Joining Form', editable=False)
    semester = models.PositiveSmallIntegerField(default=1)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    course = models.ManyToManyField(Course, blank=True)

    def __str__(self):
        return f"{self.form_name}"
