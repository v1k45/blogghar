from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^@(?P<username>[\w-]+)/blog/$', views.blog_detail, name='user_blog'),
    url(r'^blog-home/start/$', views.blog_create, name='blog_create'),
    url(r'^blog-home/update/$', views.blog_update, name='blog_update'),
    url(r'^blog-home/write/$', views.post_create, name='post_create'),
    url(r'^blog-home/update/(?P<slug>[\w-]+)/$', views.post_update, name='post_update'),  # noqa
    url(r'^blog-home/tags/$', views.tag_autocomplete, name='tag_autocomplete'),
    url(r'^blog-home/posts/$', views.user_posts, name='user_posts'),
]
