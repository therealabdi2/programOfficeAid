from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from announcements.api.serializers import AllAnnouncementSerializer, DetailAnnouncementSerializer
from announcements.models import Announcement
from announcements.permissions import IsAuthorOrReadOnly


class AllAnnouncementsAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Announcement.objects.all()
    serializer_class = AllAnnouncementSerializer


class DetailAnnouncementsAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Announcement.objects.all()
    serializer_class = DetailAnnouncementSerializer
