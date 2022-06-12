from django.contrib.auth import get_user_model
from django.db import models


class Announcement(models.Model):
    title = models.CharField(max_length=100, help_text="Enter announcement title")
    description = models.TextField(help_text="Enter announcement description")
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

    class Meta:
        ordering = ['-timestamp']
