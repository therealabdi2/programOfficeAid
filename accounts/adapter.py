import re

from allauth.account.adapter import DefaultAccountAdapter
from django.forms import ValidationError

EMAIL_REGEX = r"(^[\w]+[\w.%+-]*@iiu\.edu\.pk$)"


class ValidateEmailAdapter(DefaultAccountAdapter):
    def clean_email(self, email):
        if email and not re.match(EMAIL_REGEX, email):
            raise ValidationError('Please enter a valid IIUI email address')
        return email
