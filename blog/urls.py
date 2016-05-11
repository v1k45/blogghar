from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^@(?P<username>[\w-]+)/blog/$', views.blog_detail, name='user_blog'),
    url(r'^@(?P<username>[\w-]+)/blog/(?P<slug>[\w-]+)/$', views.post_detail, name='post_detail'),

    url(r'^tags/(?P<tag>[\w-]+)/$', views.tagged_posts_list, name='tagged_posts_list'),

    url(r'^blog/start/$', views.blog_create, name='blog_create'),
    url(r'^blog/update/$', views.blog_update, name='blog_update'),

    url(r'^blog/comments/$', views.blog_comments, name='blog_comments'),

    url(r'^write/$', views.post_create, name='post_create'),
    url(r'^update/(?P<slug>[\w-]+)/$', views.post_update, name='post_update'),  # noqa

    url(r'^tags/$', views.tag_autocomplete, name='tag_autocomplete'),
    url(r'^posts/$', views.user_posts, name='user_posts'),
]
