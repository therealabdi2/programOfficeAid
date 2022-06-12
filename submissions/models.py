import os

from django.core import mail
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from twilio.rest import Client

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
    semester = models.PositiveSmallIntegerField(default=1, choices=list(zip(range(1, 10), range(1, 10))),
                                                validators=[
                                                    MaxValueValidator(9),
                                                    MinValueValidator(1)
                                                ])
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='session', default=get_latest_session)
    course = models.ManyToManyField(Course, related_name='courses')
    fee_slip = models.ImageField(upload_to='forms/',
                                 help_text="<strong>Note:</strong> Your form might get rejected if your fee slip is "
                                           "not attached",
                                 blank=True, null=True)

    # send sms to student through twilio if form is rejected or accepted
    def send_sms(self):
        # set up twilio
        if self.form_status != 'Pending':
            account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
            auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
            client = Client(account_sid, auth_token)

            # get student's phone number
            student_phone = self.student.phone_number
            # send sms
            if self.form_status == 'Accepted':
                message = client.messages.create(
                    body="Your form has been accepted and are successfully enrolled in the courses selected.",
                    from_=os.environ.get('TWILIO_NUMBER'),
                    to=student_phone
                )
            elif self.form_status == 'Rejected':
                message = client.messages.create(
                    body="Your form has been rejected. Reason(s): {}".format(self.reason),
                    from_=os.environ.get('TWILIO_NUMBER'),
                    to=student_phone
                )
        return

    def send_email(self):
        # send email to student if form is rejected or accepted
        if self.form_status != 'Pending':
            if self.form_status == 'Rejected':

                subject = 'Joining form rejected'
                html_message = render_to_string('account/email/joining_rejected_email.html',
                                                {'reason': self.reason, })
                plain_message = strip_tags(html_message)
                from_email = os.environ.get('EMAIL_HOST_USER')
                to = self.student.student.email
                mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

            elif self.form_status == 'Accepted':
                student_courses = self.course.values_list('course_name', flat=True)
                subject = 'Joining form accepted'
                html_message = render_to_string('account/email/joining_accepted_email.html',
                                                {'student_courses': student_courses})
                plain_message = strip_tags(html_message)
                from_email = os.environ.get('EMAIL_HOST_USER')
                to = self.student.student.email
                mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
            return
        return

    def save(self, *args, **kwargs):
        # self.send_sms()
        # self.send_email()
        super().save(*args, **kwargs)

    def is_rejected(self):
        if self.form_status == 'Rejected':
            return True
        return False

    def is_pending(self):
        if self.form_status == 'Pending':
            return True
        return False

    def __str__(self):
        return f"{self.student}'s joining form"
