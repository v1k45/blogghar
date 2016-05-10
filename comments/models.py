from django.db import models
from django.conf import settings

from blog.models import Post


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='comments')
    comment = models.TextField(max_length=500)
    post = models.ForeignKey(Post, related_name='comments')

    is_removed = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
