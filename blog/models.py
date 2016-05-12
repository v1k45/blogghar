from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse_lazy

from autoslug import AutoSlugField
from simplemde.fields import SimpleMdeField


class Blog(models.Model):

    title = models.CharField(max_length=100)
    tag_line = models.CharField(max_length=50)
    short_description = models.TextField(max_length=255)

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    # one to one because an author can only have one blog (as of now)
    author = models.OneToOneField(settings.AUTH_USER_MODEL)

    is_public = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        target = reverse_lazy('blog:user_blog', args=[self.author.username])
        return target


class PostQueryset(models.QuerySet):
    """
    QuerySet class for Post model. Works like a manager.
    Useful for method chaining.
    """
    def published(self):
        return self.filter(status='p')

    def draft(self):
        return self.filter(status='d')


class Post(models.Model):

    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
    )

    blog = models.ForeignKey(Blog, related_name='posts')

    title = models.CharField(max_length=150)
    summary = models.CharField(max_length=255, blank=True)
    content = SimpleMdeField()

    slug = AutoSlugField(populate_from='title', unique_with=['blog'],
                         editable=True)

    cover = models.ImageField(blank=True, upload_to='uploads/%Y/%m/%d/')

    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts')

    status = models.CharField(choices=STATUS_CHOICES, max_length=1,
                              default='d')

    objects = PostQueryset.as_manager()

    def __str__(self):
        return self.title

    def is_published(self):
        return self.status == 'p'

    def is_draft(self):
        return self.status == 'd'

    def get_absolute_url(self):
        target = reverse_lazy('blog:post_detail',
                              args=[self.author.username, self.slug])
        return target

    class Meta(object):
        ordering = ('-created', )


class Tag(models.Model):
    name = models.CharField(max_length=30)
    slug = AutoSlugField(populate_from='name', editable=True, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        target = reverse_lazy('blog:tagged_posts_list', args=[self.slug])
        return target
