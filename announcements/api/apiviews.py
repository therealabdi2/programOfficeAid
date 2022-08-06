from rest_framework import generics

from announcements.api.serializers import AllAnnouncementSerializer, DetailAnnouncementSerializer
from announcements.models import Announcement


class AllAnnouncementsAPIView(generics.ListCreateAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AllAnnouncementSerializer


class DetailAnnouncementsAPIView(generics.RetrieveAPIView):
    queryset = Announcement.objects.all()
    serializer_class = DetailAnnouncementSerializer
