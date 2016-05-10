from django.db import models

from django.conf import settings


class ImageUpload(models.Model):
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 related_name='image_uploads')
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.name
