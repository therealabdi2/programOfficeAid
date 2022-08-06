from rest_framework import generics

from announcements.api.serializers import AllAnnouncementSerializer
from announcements.models import Announcement


class AllAnnouncementsAPIView(generics.ListCreateAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AllAnnouncementSerializer
