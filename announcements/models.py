import os

from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models
from twilio.rest import Client

from accounts.models import Batch, StudentProfile


class AnnouncementSubscribers(models.Model):
    email = models.EmailField(unique=True)
    date_subscribed = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Announcement Subscribers"


class Announcement(models.Model):
    title = models.CharField(max_length=100, help_text="Enter announcement title")
    description = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='announcements')
    slug = models.SlugField(default="", blank=True,
                            null=False, unique=True)
    liked = models.ManyToManyField(get_user_model(), related_name='liked_announcements', blank=True, default=None)

    def __str__(self):
        return self.title

    def num_like(self):
        return self.liked.count()

    def num_comment(self):
        return self.comments.count()


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField(max_length=300)
    post = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name="comments",
                             help_text="The post on which this comment exists")
    liked = models.ManyToManyField(get_user_model(), related_name='liked_comments', blank=True, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return self.post.title + " - " + self.text[0:10] + ".... - " + self.user.full_name()

    def num_like(self):
        return self.liked.count()


# send sms to all or selected batches
class SendSMS(models.Model):
    batch = models.ManyToManyField(Batch, blank=True, default=None)
    message = models.TextField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[0:10] + ".... - "

    def send_sms(self):
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        client = Client(account_sid, auth_token)

        # get all students phone number in the batches selected
        students_phone_numbers = StudentProfile.objects.filter(batch__in=self.batch.all()).values_list('phone_number',
                                                                                                       flat=True)

        for phone_number in students_phone_numbers:
            print(phone_number)

            client.messages.create(
                body=self.message,
                from_=os.environ.get('TWILIO_NUMBER'),
                to=phone_number
            )

    # send sms before saving
    def save(self, *args, **kwargs):
        self.send_sms()
        super().save(*args, **kwargs)
