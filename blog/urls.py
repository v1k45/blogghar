from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.HomeTemplateView.as_view(), name='home'),
    url(r'^@(?P<username>[\w-]+)/blog/$', views.BlogDetail.as_view(), name='user_blog'),  # noqa
    url(r'^@(?P<username>[\w-]+)/blog/(?P<slug>[\w-]+)/$',
        views.PostDetailView.as_view(), name='post_detail'),

    url(r'^tags/$', views.TagAutoComplete.as_view(), name='tag_autocomplete'),
    url(r'^tags/(?P<tag>[\w-]+)/$', views.TagggedPostsList.as_view(),
        name='tagged_posts_list'),

    url(r'^blog/start/$', views.BlogCreateView.as_view(), name='blog_create'),
    url(r'^blog/update/$', views.BlogUpdateView.as_view(), name='blog_update'),

    url(r'^blog/comments/$', views.BlogComments.as_view(), name='blog_comments'),  # noqa

    url(r'^write/$', views.PostCreateView.as_view(), name='post_create'),
    url(r'^update/(?P<slug>[\w-]+)/$', views.PostUpdateView.as_view(), name='post_update'),  # noqa
    url(r'^delete/(?P<slug>[\w-]+)/$', views.PostDeleteView.as_view(), name='post_delete'),  # noqa

    url(r'^posts/$', views.UserPostsList.as_view(), name='user_posts'),
]
