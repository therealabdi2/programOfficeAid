from rest_framework import serializers

from announcements.models import Announcement


class AllAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ('id', 'title', 'description', 'author', 'created_at', 'updated_at', 'liked')
        ordering = ['-created_at']


class DetailAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ('title', 'description', 'author', 'created_at', 'updated_at', 'liked')
        ordering = ['-created_at']
