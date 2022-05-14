from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from courses.models import Course, Session


class ParentForm(models.Model):
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

    reason = models.TextField(blank=True, null=True, help_text="Mention reason if rejected")

    class Meta:
        abstract = True


def get_latest_session():
    return Session.objects.latest('session_start_date')


class Joining(ParentForm):
    semester = models.PositiveSmallIntegerField(default=1, validators=[
        MaxValueValidator(14),
        MinValueValidator(1)
    ])
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='session', default=get_latest_session)
    course = models.ManyToManyField(Course, related_name='courses')
    fee_slip = models.ImageField(upload_to='forms/',
                                 help_text="<strong>Note:</strong> Your form might get rejected if your fee slip is "
                                           "not attached",
                                 blank=True, null=True)

    def __str__(self):
        return f"{self.student}'s joining form"
