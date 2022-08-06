from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Account
from announcements.models import Announcement


class APITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        author = Account.objects.create(
            first_name='foo',
            last_name='bar',
            email='foobar@iiu.edu.pk',
            password='testpass123',
        )
        cls.announcement = Announcement.objects.create(
            title="University Closed",
            subtitle="Due to the prevailing pandemic university will remain closed till further notice",
            author=author,
        )

    def test_api_listview(self):
        response = self.client.get(reverse("announcements:api_all_announcements"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Announcement.objects.count(), 1)
        self.assertContains(response, self.announcement)
