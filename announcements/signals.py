import os

from django.core import mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from announcements.models import Announcement, AnnouncementSubscribers


@receiver(post_save, sender=Announcement)
def send_mail_to_subs(sender, instance, created, **kwargs):
    if not created:
        return

    emails = AnnouncementSubscribers.objects.values_list('email', flat=True)
    subject = 'New Announcement!'
    html_message = render_to_string('account/email/newsletter.html',
                                    {
                                        'title': instance.title,
                                        'description': instance.description,
                                    })
    plain_message = strip_tags(html_message)
    from_email = os.environ.get('EMAIL_HOST_USER')

    for email in emails:
        to = email
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
