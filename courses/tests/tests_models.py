import datetime

from django.test import TestCase
from django.utils import timezone

from courses.models import Session


class SessionModelTests(TestCase):
    def test_if_session_dates_were_published_correctly(self):
        """
        returns True for session whose session_start_date comes before than
        session_end_date
        """
        time_start = timezone.now()
        time_end = timezone.now() + datetime.timedelta(days=1)
        session = Session(session_start_date=time_start, session_end_date=time_end)

        # check if session_start_date is less than session_end_date
        self.assertIs(session.valid_session_date(), True)

    # check if joining date is less than joining deadline
    def test_if_joining_date_is_less_than_joining_deadline(self):
        """
        returns True for session whose joining_date comes before than
        joining_deadline
        """
        time_start = timezone.now()
        time_end = timezone.now() + datetime.timedelta(days=1)
        joining = Session(joining_date=time_start, joining_deadline=time_end)

        # check if joining_date is less than joining_deadline
        self.assertIs(joining.valid_joining_date(), True)

