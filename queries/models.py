from django.contrib.auth import get_user_model
from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.

class QueryPost(models.Model):
    title = models.CharField(max_length=100, help_text="What's on your mind?")
    body = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='query_posts')
    slug = models.SlugField(default="", blank=True,
                            null=False, unique=True)
    liked = models.ManyToManyField(get_user_model(), related_name='liked_posts', blank=True, default=None)

    def __str__(self):
        return self.title + " | " + self.author

    def num_like(self):
        return self.liked.count()

    def num_comment(self):
        return self.query_comments.count()


class QueryComment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField(max_length=300)
    post = models.ForeignKey(QueryPost, on_delete=models.CASCADE, related_name="query_comments",
                             help_text="The post on which this comment exists")
    liked = models.ManyToManyField(get_user_model(), related_name='liked_post_comments', blank=True, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return self.post.title + " - " + self.text[0:10] + ".... - " + self.user.full_name()

    def num_like(self):
        return self.liked.count()
